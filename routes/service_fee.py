from flask import Blueprint, request
from models.user import db, User
from models.service import Service
from models.service_fee import ServiceFee
from utils.response import success_response, error_response
from utils.jwt_handler import token_required

service_fee_bp = Blueprint('service_fee', __name__, url_prefix='/api/service-fees')

def check_admin_role(user_id):
    """Check if user is admin"""
    user = User.query.get(user_id)
    if not user or user.role not in ['owner', 'admin']:
        return False
    return True

@service_fee_bp.route('', methods=['GET'])
def get_service_fees():
    """Get all service fees"""
    try:
        service_id = request.args.get('service_id')
        
        if service_id:
            fees = ServiceFee.query.filter_by(service_id=int(service_id)).all()
        else:
            fees = ServiceFee.query.all()
        
        return success_response(
            data=[fee.to_dict() for fee in fees],
            message='Data service fee berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data service fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_fee_bp.route('/<int:fee_id>', methods=['GET'])
def get_service_fee(fee_id):
    """Get specific service fee"""
    try:
        fee = ServiceFee.query.get(fee_id)
        
        if not fee:
            return error_response(
                message='Service fee tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        return success_response(
            data=fee.to_dict(),
            message='Data service fee berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data service fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_fee_bp.route('', methods=['POST'])
@token_required
def create_service_fee():
    """Create new service fee (Admin only)"""
    try:
        user_id = request.user_id
        
        if not check_admin_role(user_id):
            return error_response(
                message='Hanya admin yang bisa membuat service fee',
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
        
        service_id = data.get('service_id')
        min_amount = data.get('min_amount', 0)
        max_amount = data.get('max_amount', 0)
        fee = data.get('fee', 0)
        
        if not service_id:
            return error_response(
                message='service_id wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # Check service exists
        service = Service.query.get(service_id)
        if not service:
            return error_response(
                message='Service tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # Validate amounts
        try:
            min_amount = float(min_amount)
            max_amount = float(max_amount)
            fee = float(fee)
            
            if min_amount < 0 or max_amount < 0 or fee < 0:
                return error_response(
                    message='Amount tidak boleh negatif',
                    error='INVALID_INPUT',
                    status_code=400
                )
            
            if min_amount > max_amount:
                return error_response(
                    message='min_amount tidak boleh lebih besar dari max_amount',
                    error='INVALID_INPUT',
                    status_code=400
                )
        except (ValueError, TypeError):
            return error_response(
                message='Amount harus berupa angka',
                error='INVALID_INPUT',
                status_code=400
            )
        
        new_fee = ServiceFee(
            service_id=service_id,
            min_amount=min_amount,
            max_amount=max_amount,
            fee=fee
        )
        
        db.session.add(new_fee)
        db.session.commit()
        
        return success_response(
            data=new_fee.to_dict(),
            message='Service fee berhasil dibuat',
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat membuat service fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_fee_bp.route('/<int:fee_id>', methods=['PUT'])
@token_required
def update_service_fee(fee_id):
    """Update service fee (Admin only)"""
    try:
        user_id = request.user_id
        
        if not check_admin_role(user_id):
            return error_response(
                message='Hanya admin yang bisa mengubah service fee',
                error='FORBIDDEN',
                status_code=403
            )
        
        fee_obj = ServiceFee.query.get(fee_id)
        
        if not fee_obj:
            return error_response(
                message='Service fee tidak ditemukan',
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
        
        if 'min_amount' in data:
            try:
                min_amount = float(data.get('min_amount'))
                if min_amount < 0:
                    return error_response(
                        message='min_amount tidak boleh negatif',
                        error='INVALID_INPUT',
                        status_code=400
                    )
                fee_obj.min_amount = min_amount
            except (ValueError, TypeError):
                return error_response(
                    message='min_amount harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )
        
        if 'max_amount' in data:
            try:
                max_amount = float(data.get('max_amount'))
                if max_amount < 0:
                    return error_response(
                        message='max_amount tidak boleh negatif',
                        error='INVALID_INPUT',
                        status_code=400
                    )
                fee_obj.max_amount = max_amount
            except (ValueError, TypeError):
                return error_response(
                    message='max_amount harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )
        
        if 'fee' in data:
            try:
                fee_amount = float(data.get('fee'))
                if fee_amount < 0:
                    return error_response(
                        message='fee tidak boleh negatif',
                        error='INVALID_INPUT',
                        status_code=400
                    )
                fee_obj.fee = fee_amount
            except (ValueError, TypeError):
                return error_response(
                    message='fee harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )
        
        # Validate min <= max
        if fee_obj.min_amount > fee_obj.max_amount:
            return error_response(
                message='min_amount tidak boleh lebih besar dari max_amount',
                error='INVALID_INPUT',
                status_code=400
            )
        
        db.session.commit()
        
        return success_response(
            data=fee_obj.to_dict(),
            message='Service fee berhasil diubah',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mengubah service fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@service_fee_bp.route('/<int:fee_id>', methods=['DELETE'])
@token_required
def delete_service_fee(fee_id):
    """Delete service fee (Admin only)"""
    try:
        user_id = request.user_id
        
        if not check_admin_role(user_id):
            return error_response(
                message='Hanya admin yang bisa menghapus service fee',
                error='FORBIDDEN',
                status_code=403
            )
        
        fee_obj = ServiceFee.query.get(fee_id)
        
        if not fee_obj:
            return error_response(
                message='Service fee tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        db.session.delete(fee_obj)
        db.session.commit()
        
        return success_response(
            data=None,
            message='Service fee berhasil dihapus',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menghapus service fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
