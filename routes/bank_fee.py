from flask import Blueprint, request
from models.user import db, User
from models.edc_machine import EdcMachine
from models.service import Service
from models.bank_fee import BankFee
from models.agent_profile import AgentProfile
from utils.response import success_response, error_response
from utils.jwt_handler import token_required

bank_fee_bp = Blueprint('bank_fee', __name__, url_prefix='/api/bank-fees')

def check_agent_ownership(user_id, agent_id):
    """Check if user owns the agent profile"""
    agent = AgentProfile.query.get(agent_id)
    if not agent or agent.user_id != user_id:
        return False
    return True

def check_edc_ownership(user_id, edc_id):
    """Check if user owns the EDC machine"""
    edc = EdcMachine.query.get(edc_id)
    if not edc:
        return False
    return check_agent_ownership(user_id, edc.agent_profile_id)

@bank_fee_bp.route('', methods=['GET'])
@token_required
def get_bank_fees():
    """Get all bank fees (accessible by all authenticated users)"""
    try:
        edc_id = request.args.get('edc_id')
        
        if edc_id:
            fees = BankFee.query.filter_by(edc_machine_id=int(edc_id)).all()
        else:
            # Get all bank fees (no ownership restriction)
            fees = BankFee.query.all()
        
        return success_response(
            data=[fee.to_dict() for fee in fees],
            message='Data bank fee berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data bank fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@bank_fee_bp.route('/<int:fee_id>', methods=['GET'])
@token_required
def get_bank_fee(fee_id):
    """Get specific bank fee (accessible by all authenticated users)"""
    try:
        fee = BankFee.query.get(fee_id)
        
        if not fee:
            return error_response(
                message='Bank fee tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # No ownership check - accessible by all authenticated users
        
        return success_response(
            data=fee.to_dict(),
            message='Data bank fee berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data bank fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@bank_fee_bp.route('', methods=['POST'])
@token_required
def create_bank_fee():
    """Create new bank fee"""
    try:
        user_id = request.user_id
        
        data = request.get_json()
        
        if not data:
            return error_response(
                message='Request body tidak boleh kosong',
                error='INVALID_REQUEST',
                status_code=400
            )
        
        edc_machine_id = data.get('edc_machine_id')
        service_id = data.get('service_id')
        fee = data.get('fee', 0)
        
        if not edc_machine_id or not service_id:
            return error_response(
                message='edc_machine_id dan service_id wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # Check EDC ownership
        if not check_edc_ownership(user_id, edc_machine_id):
            return error_response(
                message='Anda tidak memiliki akses ke EDC machine ini',
                error='FORBIDDEN',
                status_code=403
            )
        
        # Check service exists
        service = Service.query.get(service_id)
        if not service:
            return error_response(
                message='Service tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # Validate fee
        try:
            fee = float(fee)
            if fee < 0:
                return error_response(
                    message='Fee tidak boleh negatif',
                    error='INVALID_INPUT',
                    status_code=400
                )
        except (ValueError, TypeError):
            return error_response(
                message='Fee harus berupa angka',
                error='INVALID_INPUT',
                status_code=400
            )
        
        # Check duplicate
        existing = BankFee.query.filter_by(
            edc_machine_id=edc_machine_id,
            service_id=service_id
        ).first()
        
        if existing:
            return error_response(
                message='Bank fee untuk EDC machine dan service ini sudah ada',
                error='BANK_FEE_ALREADY_EXISTS',
                status_code=409
            )
        
        new_fee = BankFee(
            edc_machine_id=edc_machine_id,
            service_id=service_id,
            fee=fee
        )
        
        db.session.add(new_fee)
        db.session.commit()
        
        return success_response(
            data=new_fee.to_dict(),
            message='Bank fee berhasil dibuat',
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat membuat bank fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@bank_fee_bp.route('/<int:fee_id>', methods=['PUT'])
@token_required
def update_bank_fee(fee_id):
    """Update bank fee"""
    try:
        user_id = request.user_id
        
        fee_obj = BankFee.query.get(fee_id)
        
        if not fee_obj:
            return error_response(
                message='Bank fee tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        if not check_edc_ownership(user_id, fee_obj.edc_machine_id):
            return error_response(
                message='Anda tidak memiliki akses untuk mengubah bank fee ini',
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
        
        if 'fee' in data:
            try:
                fee_amount = float(data.get('fee'))
                if fee_amount < 0:
                    return error_response(
                        message='Fee tidak boleh negatif',
                        error='INVALID_INPUT',
                        status_code=400
                    )
                fee_obj.fee = fee_amount
            except (ValueError, TypeError):
                return error_response(
                    message='Fee harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )
        
        db.session.commit()
        
        return success_response(
            data=fee_obj.to_dict(),
            message='Bank fee berhasil diubah',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mengubah bank fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@bank_fee_bp.route('/<int:fee_id>', methods=['DELETE'])
@token_required
def delete_bank_fee(fee_id):
    """Delete bank fee"""
    try:
        user_id = request.user_id
        
        fee_obj = BankFee.query.get(fee_id)
        
        if not fee_obj:
            return error_response(
                message='Bank fee tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        if not check_edc_ownership(user_id, fee_obj.edc_machine_id):
            return error_response(
                message='Anda tidak memiliki akses untuk menghapus bank fee ini',
                error='FORBIDDEN',
                status_code=403
            )
        
        db.session.delete(fee_obj)
        db.session.commit()
        
        return success_response(
            data=None,
            message='Bank fee berhasil dihapus',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menghapus bank fee',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
