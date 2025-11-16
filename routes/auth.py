from flask import Blueprint, request
from datetime import datetime, timedelta
from models.user import db, User, TokenBlacklist
from models.agent_profile import AgentProfile
from utils.response import success_response, error_response
from utils.validators import (
    validate_email, validate_password, validate_name,
    hash_password, check_password, ValidationError
)
from utils.jwt_handler import generate_token, token_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register new user
    
    Request body:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "SecurePass123",
        "role": "owner" (optional, default: "owner")
    }
    """
    try:
        data = request.get_json()
        
        # Validasi input
        if not data:
            return error_response(
                message='Request body tidak boleh kosong',
                error='INVALID_REQUEST',
                status_code=400
            )
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        role = data.get('role', 'owner').lower()
        
        # Validate required fields
        if not name or not email or not password:
            return error_response(
                message='Field name, email, dan password wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # Validate role
        valid_roles = ['owner', 'kasir']
        if role not in valid_roles:
            return error_response(
                message=f'Role harus salah satu dari: {", ".join(valid_roles)}',
                error='INVALID_ROLE',
                status_code=400
            )
        
        # For kasir role, owner_id is required (single-agent mode)
        owner_id = None
        if role == 'kasir':
            owner_id = data.get('owner_id')
            if not owner_id:
                return error_response(
                    message='Untuk role kasir, owner_id wajib diisi',
                    error='MISSING_OWNER_ID',
                    status_code=400
                )
            
            # Verify owner exists and has agent
            owner = User.query.get(owner_id)
            if not owner or owner.role != 'owner':
                return error_response(
                    message='Owner tidak ditemukan',
                    error='INVALID_OWNER',
                    status_code=400
                )
            
            # Get owner's agent (single-agent mode)
            owner_agent = AgentProfile.query.filter_by(user_id=owner_id).first()
            if not owner_agent:
                return error_response(
                    message='Owner belum memiliki agent profile',
                    error='OWNER_NO_AGENT',
                    status_code=400
                )
        
        # Validate name
        try:
            validate_name(name)
        except ValidationError as e:
            return error_response(
                message=str(e),
                error='INVALID_NAME',
                status_code=400
            )
        
        # Validate email
        try:
            validate_email(email)
        except ValidationError as e:
            return error_response(
                message=str(e),
                error='INVALID_EMAIL',
                status_code=400
            )
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return error_response(
                message='Email sudah terdaftar',
                error='EMAIL_ALREADY_EXISTS',
                status_code=409
            )
        
        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            return error_response(
                message=str(e),
                error='WEAK_PASSWORD',
                status_code=400
            )
        
        # Create new user
        hashed_password = hash_password(password)
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            status='active'
        )
        
        # Assign agent for kasir (single-agent mode)
        if role == 'kasir' and owner_agent:
            new_user.agent_profile_id = owner_agent.id
        
        db.session.add(new_user)
        db.session.flush()  # Get user ID before commit
        
        # Auto-create agent profile for owner (single-agent mode)
        if role == 'owner':
            agent_name = f"{name} Agent"
            new_agent = AgentProfile(
                user_id=new_user.id,
                owner_id=new_user.id,
                agent_name=agent_name,
                address=None,
                phone=None,
                total_balance=0.00
            )
            db.session.add(new_agent)
            db.session.flush()  # Get agent ID
            
            # Assign agent to user
            new_user.agent_profile_id = new_agent.id
        
        db.session.commit()
        
        return success_response(
            data=new_user.to_dict(),
            message='User berhasil didaftarkan',
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat registrasi',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user dan dapatkan JWT token
    
    Request body:
    {
        "email": "john@example.com",
        "password": "SecurePass123"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response(
                message='Request body tidak boleh kosong',
                error='INVALID_REQUEST',
                status_code=400
            )
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return error_response(
                message='Email dan password wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # Check user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            return error_response(
                message='Email atau password salah',
                error='INVALID_CREDENTIALS',
                status_code=401
            )
        
        # Check password
        if not check_password(user.password, password):
            return error_response(
                message='Email atau password salah',
                error='INVALID_CREDENTIALS',
                status_code=401
            )
        
        # Check user status
        if user.status != 'active':
            return error_response(
                message='User tidak aktif',
                error='USER_INACTIVE',
                status_code=403
            )
        
        # Generate token
        token = generate_token(user.id, user.email)
        
        return success_response(
            data={
                'user': user.to_dict(),
                'token': token
            },
            message='Login berhasil',
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat login',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@auth_bp.route('/users', methods=['GET'])
@token_required
def get_all_users():
    """
    Get all users data
    
    Headers:
    Authorization: Bearer <token>
    
    Query parameters:
    - role: filter by role (owner, kasir)
    - status: filter by status (active, inactive)
    - page: page number (default: 1)
    - per_page: items per page (default: 50)
    """
    try:
        # Get current user
        current_user = User.query.get(request.user_id)
        if not current_user:
            return error_response(
                message='User tidak ditemukan',
                error='USER_NOT_FOUND',
                status_code=404
            )
        
        # Get query parameters
        role_filter = request.args.get('role')
        status_filter = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        # Build query
        query = User.query
        
        # Apply filters
        if role_filter:
            query = query.filter(User.role == role_filter.lower())
        
        if status_filter:
            query = query.filter(User.status == status_filter.lower())
        
        # Paginate
        users = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Convert to dict and include agent info
        users_data = []
        for user in users.items:
            user_dict = user.to_dict()
            
            # Add agent profile info if exists
            if user.agent_profile_id:
                agent = AgentProfile.query.get(user.agent_profile_id)
                if agent:
                    user_dict['agent_profile'] = {
                        'id': agent.id,
                        'agent_name': agent.agent_name,
                        'address': agent.address,
                        'phone': agent.phone,
                        'total_balance': agent.total_balance
                    }
            
            users_data.append(user_dict)
        
        return success_response(
            data={
                'users': users_data,
                'pagination': {
                    'page': users.page,
                    'per_page': users.per_page,
                    'total_pages': users.pages,
                    'total_items': users.total,
                    'has_next': users.has_next,
                    'has_prev': users.has_prev
                }
            },
            message='Data users berhasil diambil',
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data users',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Logout user dan blacklist token
    
    Headers:
    Authorization: Bearer <token>
    """
    try:
        # Get token from header
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return error_response(
                    message='Format Authorization header salah',
                    error='INVALID_HEADER_FORMAT',
                    status_code=400
                )
        
        if not token:
            return error_response(
                message='Token diperlukan',
                error='MISSING_TOKEN',
                status_code=400
            )
        
        # Get current user
        current_user = User.query.get(request.user_id)
        if not current_user:
            return error_response(
                message='User tidak ditemukan',
                error='USER_NOT_FOUND',
                status_code=404
            )
        
        # Decode token to get expiration time
        from utils.jwt_handler import verify_token
        try:
            payload = verify_token(token)
            expires_at = datetime.fromtimestamp(payload['exp'])
        except ValueError:
            # If token is invalid, still allow logout
            expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Check if token already blacklisted
        existing_blacklist = TokenBlacklist.query.filter_by(token=token).first()
        if existing_blacklist:
            return error_response(
                message='Token sudah logout sebelumnya',
                error='TOKEN_ALREADY_BLACKLISTED',
                status_code=400
            )
        
        # Add token to blacklist
        blacklist_entry = TokenBlacklist(
            token=token,
            user_id=current_user.id,
            expires_at=expires_at
        )
        
        db.session.add(blacklist_entry)
        db.session.commit()
        
        return success_response(
            data={
                'user_id': current_user.id,
                'email': current_user.email,
                'logout_time': datetime.utcnow().isoformat()
            },
            message='Logout berhasil',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat logout',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """Update user (Owner only)"""
    try:
        current_user_id = request.user_id
        
        # Check if current user is owner
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'owner':
            return error_response(
                message='Hanya owner yang dapat mengubah user',
                error='FORBIDDEN',
                status_code=403
            )
        
        user = User.query.get(user_id)
        
        if not user:
            return error_response(
                message='User tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        data = request.get_json()
        
        if not data:
            return error_response(
                message='Request body tidak boleh kosong',
                error='INVALID_REQUEST',
                status_code=400
            )
        
        # Update fields
        if 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                return error_response(
                    message='Name tidak boleh kosong',
                    error='INVALID_INPUT',
                    status_code=400
                )
            try:
                from utils.validators import validate_name
                validate_name(name)
            except ValidationError as e:
                return error_response(
                    message=str(e),
                    error='INVALID_NAME',
                    status_code=400
                )
            user.name = name
        
        if 'email' in data:
            email = data.get('email', '').strip().lower()
            if not email:
                return error_response(
                    message='Email tidak boleh kosong',
                    error='INVALID_INPUT',
                    status_code=400
                )
            try:
                from utils.validators import validate_email
                validate_email(email)
            except ValidationError as e:
                return error_response(
                    message=str(e),
                    error='INVALID_EMAIL',
                    status_code=400
                )
            # Check duplicate email
            existing = User.query.filter_by(email=email).filter(User.id != user_id).first()
            if existing:
                return error_response(
                    message='Email sudah digunakan',
                    error='EMAIL_ALREADY_EXISTS',
                    status_code=409
                )
            user.email = email
        
        if 'password' in data:
            password = data.get('password', '')
            if password:
                try:
                    from utils.validators import validate_password
                    validate_password(password)
                except ValidationError as e:
                    return error_response(
                        message=str(e),
                        error='WEAK_PASSWORD',
                        status_code=400
                    )
                from utils.validators import hash_password
                user.password = hash_password(password)
        
        if 'role' in data:
            role = data.get('role', '').lower()
            valid_roles = ['owner', 'kasir']
            if role not in valid_roles:
                return error_response(
                    message=f'Role harus salah satu dari: {", ".join(valid_roles)}',
                    error='INVALID_ROLE',
                    status_code=400
                )
            user.role = role
        
        if 'status' in data:
            status = data.get('status', '').lower()
            valid_statuses = ['active', 'inactive']
            if status not in valid_statuses:
                return error_response(
                    message=f'Status harus salah satu dari: {", ".join(valid_statuses)}',
                    error='INVALID_STATUS',
                    status_code=400
                )
            user.status = status
        
        db.session.commit()
        
        return success_response(
            data=user.to_dict(),
            message='User berhasil diubah',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mengubah user',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """Delete user (Owner only)"""
    try:
        current_user_id = request.user_id
        
        # Check if current user is owner
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'owner':
            return error_response(
                message='Hanya owner yang dapat menghapus user',
                error='FORBIDDEN',
                status_code=403
            )
        
        user = User.query.get(user_id)
        
        if not user:
            return error_response(
                message='User tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # Prevent deleting self
        if user_id == current_user_id:
            return error_response(
                message='Tidak dapat menghapus akun sendiri',
                error='SELF_DELETE_FORBIDDEN',
                status_code=400
            )
        
        db.session.delete(user)
        db.session.commit()
        
        return success_response(
            data=None,
            message='User berhasil dihapus',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menghapus user',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
