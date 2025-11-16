from flask import Blueprint, request
from models.user import db, User
from models.service import Service
from models.service_fee import ServiceFee
from utils.response import success_response, error_response
from utils.jwt_handler import token_required

service_bp = Blueprint('service', __name__, url_prefix='/api/services')

def check_admin_role(user_id):
    """Check if user is admin (can manage services)"""
    user = User.query.get(user_id)
    if not user or user.role not in ['owner', 'admin']:
        return False
    return True

@service_bp.route('', methods=['GET'])
def get_services():
    """Get all services (public endpoint)"""
    try:
        services = Service.query.all()
        return success_response(
            data=[service.to_dict() for service in services],
            message='Data service berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data service',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_bp.route('/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Get specific service with fees"""
    try:
        service = Service.query.get(service_id)
        
        if not service:
            return error_response(
                message='Service tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        service_data = service.to_dict()
        fees = ServiceFee.query.filter_by(service_id=service_id).all()
        service_data['fees'] = [fee.to_dict() for fee in fees]
        
        return success_response(
            data=service_data,
            message='Data service berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data service',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_bp.route('', methods=['POST'])
@token_required
def create_service():
    """Create new service (Admin only)"""
    try:
        user_id = request.user_id
        
        if not check_admin_role(user_id):
            return error_response(
                message='Hanya admin yang bisa membuat service',
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
        
        name = data.get('name', '').strip()
        category = data.get('category', '').strip() if data.get('category') else None
        description = data.get('description', '').strip() if data.get('description') else None
        requires_target = data.get('requires_target', False)
        
        if not name:
            return error_response(
                message='Service name wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # Check duplicate
        existing = Service.query.filter_by(name=name).first()
        if existing:
            return error_response(
                message='Service dengan nama ini sudah ada',
                error='SERVICE_ALREADY_EXISTS',
                status_code=409
            )
        
        new_service = Service(
            name=name,
            category=category,
            description=description,
            requires_target=requires_target
        )
        
        db.session.add(new_service)
        db.session.commit()
        
        return success_response(
            data=new_service.to_dict(),
            message='Service berhasil dibuat',
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat membuat service',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_bp.route('/<int:service_id>', methods=['PUT'])
@token_required
def update_service(service_id):
    """Update service (Admin only)"""
    try:
        user_id = request.user_id
        
        if not check_admin_role(user_id):
            return error_response(
                message='Hanya admin yang bisa mengubah service',
                error='FORBIDDEN',
                status_code=403
            )
        
        service = Service.query.get(service_id)
        
        if not service:
            return error_response(
                message='Service tidak ditemukan',
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
        
        if 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                return error_response(
                    message='Service name tidak boleh kosong',
                    error='INVALID_INPUT',
                    status_code=400
                )
            
            existing = Service.query.filter_by(name=name).filter(Service.id != service_id).first()
            if existing:
                return error_response(
                    message='Service dengan nama ini sudah ada',
                    error='SERVICE_ALREADY_EXISTS',
                    status_code=409
                )
            service.name = name
        
        if 'category' in data:
            service.category = data.get('category', '').strip() or None
        
        if 'description' in data:
            service.description = data.get('description', '').strip() or None
        
        if 'requires_target' in data:
            service.requires_target = data.get('requires_target', False)
        
        db.session.commit()
        
        return success_response(
            data=service.to_dict(),
            message='Service berhasil diubah',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mengubah service',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_bp.route('/<int:service_id>', methods=['DELETE'])
@token_required
def delete_service(service_id):
    """Delete service (Admin only)"""
    try:
        user_id = request.user_id
        
        if not check_admin_role(user_id):
            return error_response(
                message='Hanya admin yang bisa menghapus service',
                error='FORBIDDEN',
                status_code=403
            )
        
        service = Service.query.get(service_id)
        
        if not service:
            return error_response(
                message='Service tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        db.session.delete(service)
        db.session.commit()
        
        return success_response(
            data=None,
            message='Service berhasil dihapus',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menghapus service',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
