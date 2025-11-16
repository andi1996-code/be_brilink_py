from flask import Blueprint, request
from models.user import db, User
from models.agent_profile import AgentProfile
from utils.response import success_response, error_response
from utils.jwt_handler import token_required

agent_bp = Blueprint('agent', __name__, url_prefix='/api/agents')

def check_owner_role(user_id):
    """Check if user has owner role"""
    user = User.query.get(user_id)
    if not user or user.role != 'owner':
        return False
    return True

@agent_bp.route('', methods=['POST'])
@token_required
def create_agent():
    """
    Create new agent profile (Owner only)
    
    NOTE: Disabled in single-agent mode
    """
    return error_response(
        message='Fitur multi-agen sedang dinonaktifkan. Setiap owner hanya memiliki 1 agent.',
        error='MULTI_AGENT_DISABLED',
        status_code=403
    )

@agent_bp.route('', methods=['GET'])
@token_required
def get_agents():
    """Get all agent profiles for current owner"""
    try:
        user_id = request.user_id
        
        # Check if user is owner
        if not check_owner_role(user_id):
            return error_response(
                message='Hanya owner yang bisa melihat agent profile',
                error='FORBIDDEN',
                status_code=403
            )
        
        agents = AgentProfile.query.filter_by(user_id=user_id).all()
        
        return success_response(
            data=[agent.to_dict() for agent in agents],
            message='Data agent profile berhasil diambil',
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data agent profile',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@agent_bp.route('/<int:agent_id>', methods=['GET'])
@token_required
def get_agent(agent_id):
    """Get specific agent profile"""
    try:
        user_id = request.user_id
        
        agent = AgentProfile.query.get(agent_id)
        
        if not agent:
            return error_response(
                message='Agent profile tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # Check ownership
        if agent.user_id != user_id and not check_owner_role(user_id):
            return error_response(
                message='Anda tidak memiliki akses ke agent profile ini',
                error='FORBIDDEN',
                status_code=403
            )
        
        return success_response(
            data=agent.to_dict(),
            message='Data agent profile berhasil diambil',
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data agent profile',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@agent_bp.route('/<int:agent_id>', methods=['PUT'])
@token_required
def update_agent(agent_id):
    """Update agent profile (Owner only - all fields allowed in single-agent mode)
    
    Allowed fields: agent_name, address, phone, logo
    """
    try:
        user_id = request.user_id

        # Check if user is owner
        if not check_owner_role(user_id):
            return error_response(
                message='Hanya owner yang bisa mengubah agent profile',
                error='FORBIDDEN',
                status_code=403
            )

        agent = AgentProfile.query.get(agent_id)

        if not agent:
            return error_response(
                message='Agent profile tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )

        # Check ownership
        if agent.user_id != user_id:
            return error_response(
                message='Anda tidak memiliki akses untuk mengubah agent profile ini',
                error='FORBIDDEN',
                status_code=403
            )

        data = request.get_json()

        if not data:
            return error_response(
                message='Request body tidak boleh kosong',
                error='INVALID_REQUEST',
                status_code=400
            )

        # In single-agent mode, allow updating all fields
        # Update agent_name if provided
        if 'agent_name' in data:
            agent_name = data.get('agent_name', '').strip()
            if not agent_name:
                return error_response(
                    message='Agent name tidak boleh kosong',
                    error='INVALID_INPUT',
                    status_code=400
                )
            if len(agent_name) < 3:
                return error_response(
                    message='Agent name minimal 3 karakter',
                    error='INVALID_INPUT',
                    status_code=400
                )
            
            # Check duplicate name (per owner)
            existing = AgentProfile.query.filter_by(
                agent_name=agent_name,
                user_id=user_id
            ).filter(AgentProfile.id != agent_id).first()
            
            if existing:
                return error_response(
                    message='Agent profile dengan nama ini sudah ada',
                    error='AGENT_NAME_EXISTS',
                    status_code=409
                )
            
            agent.agent_name = agent_name

        # Update other fields
        if 'address' in data:
            agent.address = data.get('address', '').strip() or None

        if 'phone' in data:
            agent.phone = data.get('phone', '').strip() or None

        if 'logo' in data:
            agent.logo = data.get('logo', '').strip() or None

        db.session.commit()

        return success_response(
            data=agent.to_dict(),
            message='Agent profile berhasil diubah',
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mengubah agent profile',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@agent_bp.route('/<int:agent_id>', methods=['DELETE'])
@token_required
def delete_agent(agent_id):
    """
    Delete agent profile (Owner only)
    
    NOTE: Disabled in single-agent mode
    """
    return error_response(
        message='Fitur hapus agent sedang dinonaktifkan dalam mode single-agent.',
        error='AGENT_DELETE_DISABLED',
        status_code=403
    )
