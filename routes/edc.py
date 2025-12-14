from flask import Blueprint, request
from models.user import db, User
from models.agent_profile import AgentProfile
from models.edc_machine import EdcMachine
from models.cash_flow import CashFlow
from utils.response import success_response, error_response
from utils.jwt_handler import token_required
from decimal import Decimal, InvalidOperation

edc_bp = Blueprint('edc', __name__, url_prefix='/api/edc-machines')

def check_agent_ownership(user_id, agent_id):
    """Check if user owns the agent profile"""
    agent = AgentProfile.query.get(agent_id)
    if not agent or agent.user_id != user_id:
        return False
    return True

@edc_bp.route('', methods=['POST'])
@token_required
def create_edc_machine():
    """
    Create new EDC machine
    
    Request body:
    {
        "agent_profile_id": 1,  // optional
        "name": "EDC BCA 001",
        "bank_name": "BCA",
        "account_number": "1234567890",
        "saldo": 0.00
    }
    """
    try:
        user_id = request.user_id
        
        data = request.get_json()
        
        if not data:
            return error_response(
                message='Request body tidak boleh kosong',
                error='INVALID_REQUEST',
                status_code=400
            )
        
        agent_profile_id = data.get('agent_profile_id')
        name = data.get('name', '').strip()
        bank_name = data.get('bank_name', '').strip()
        account_number = data.get('account_number', '').strip() if data.get('account_number') else None
        saldo = data.get('saldo', 0.00)
        
        # Validate required fields
        if not name or not bank_name:
            return error_response(
                message='name dan bank_name wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # Check agent ownership only if agent_profile_id is provided
        if agent_profile_id is not None:
            if not check_agent_ownership(user_id, agent_profile_id):
                return error_response(
                    message='Anda tidak memiliki akses ke agent profile ini',
                    error='FORBIDDEN',
                    status_code=403
                )
        
        # Validate name length
        if len(name) < 3:
            return error_response(
                message='Name minimal 3 karakter',
                error='INVALID_INPUT',
                status_code=400
            )
        
        # Validate bank_name length
        if len(bank_name) < 2:
            return error_response(
                message='Bank name minimal 2 karakter',
                error='INVALID_INPUT',
                status_code=400
            )
        
        # Validate saldo
        try:
            saldo = float(saldo)
            if saldo < 0:
                return error_response(
                    message='Saldo tidak boleh negatif',
                    error='INVALID_INPUT',
                    status_code=400
                )
        except (ValueError, TypeError):
            return error_response(
                message='Saldo harus berupa angka',
                error='INVALID_INPUT',
                status_code=400
            )
        
        # Check duplicate name per agent
        existing = EdcMachine.query.filter_by(
            agent_profile_id=agent_profile_id,
            name=name
        ).first()
        
        if existing:
            return error_response(
                message='EDC machine dengan nama ini sudah ada',
                error='EDC_ALREADY_EXISTS',
                status_code=409
            )
        
        new_edc = EdcMachine(
            agent_profile_id=agent_profile_id,
            name=name,
            bank_name=bank_name,
            account_number=account_number,
            saldo=saldo,
            status='active'
        )
        
        db.session.add(new_edc)
        db.session.commit()
        
        return success_response(
            data=new_edc.to_dict(),
            message='EDC machine berhasil dibuat',
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat membuat EDC machine',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@edc_bp.route('', methods=['GET'])
@token_required
def get_edc_machines():
    """Get all EDC machines (accessible by all authenticated users)"""
    try:
        user_id = request.user_id
        agent_id = request.args.get('agent_id')
        
        if agent_id:
            # Get EDC machines for specific agent
            machines = EdcMachine.query.filter_by(agent_profile_id=int(agent_id)).all()
        else:
            # Get all EDC machines (no ownership restriction)
            machines = EdcMachine.query.all()
        
        return success_response(
            data=[machine.to_dict() for machine in machines],
            message='Data EDC machine berhasil diambil',
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data EDC machine',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@edc_bp.route('/<int:machine_id>', methods=['GET'])
@token_required
def get_edc_machine(machine_id):
    """Get specific EDC machine (accessible by all authenticated users)"""
    try:
        machine = EdcMachine.query.get(machine_id)
        
        if not machine:
            return error_response(
                message='EDC machine tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # No ownership check - accessible by all authenticated users
        
        return success_response(
            data=machine.to_dict(),
            message='Data EDC machine berhasil diambil',
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data EDC machine',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@edc_bp.route('/<int:machine_id>', methods=['PUT'])
@token_required
def update_edc_machine(machine_id):
    """Update EDC machine"""
    try:
        user_id = request.user_id
        
        machine = EdcMachine.query.get(machine_id)
        
        if not machine:
            return error_response(
                message='EDC machine tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # Check if user is owner
        user = User.query.get(user_id)
        if not user or user.role != 'owner':
            return error_response(
                message='Hanya owner yang dapat mengubah EDC machine',
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
        
        # Update fields
        if 'name' in data:
            name = data.get('name', '').strip()
            if not name:
                return error_response(
                    message='Name tidak boleh kosong',
                    error='INVALID_INPUT',
                    status_code=400
                )
            if len(name) < 3:
                return error_response(
                    message='Name minimal 3 karakter',
                    error='INVALID_INPUT',
                    status_code=400
                )
            
            # Check duplicate
            existing = EdcMachine.query.filter_by(
                name=name
            ).filter(EdcMachine.id != machine_id).first()
            
            if existing:
                return error_response(
                    message='EDC machine dengan nama ini sudah ada',
                    error='EDC_ALREADY_EXISTS',
                    status_code=409
                )
            
            machine.name = name
        
        if 'bank_name' in data:
            bank_name = data.get('bank_name', '').strip()
            if not bank_name:
                return error_response(
                    message='Bank name tidak boleh kosong',
                    error='INVALID_INPUT',
                    status_code=400
                )
            if len(bank_name) < 2:
                return error_response(
                    message='Bank name minimal 2 karakter',
                    error='INVALID_INPUT',
                    status_code=400
                )
            machine.bank_name = bank_name
        
        if 'account_number' in data:
            machine.account_number = data.get('account_number', '').strip() or None
        
        if 'saldo' in data:
            try:
                saldo = float(data.get('saldo', 0))
                if saldo < 0:
                    return error_response(
                        message='Saldo tidak boleh negatif',
                        error='INVALID_INPUT',
                        status_code=400
                    )
                machine.saldo = saldo
            except (ValueError, TypeError):
                return error_response(
                    message='Saldo harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )
        
        if 'status' in data:
            status = data.get('status', '').lower()
            if status not in ['active', 'inactive']:
                return error_response(
                    message='Status harus "active" atau "inactive"',
                    error='INVALID_INPUT',
                    status_code=400
                )
            machine.status = status
        
        db.session.commit()
        
        return success_response(
            data=machine.to_dict(),
            message='EDC machine berhasil diubah',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mengubah EDC machine',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@edc_bp.route('/<int:machine_id>', methods=['DELETE'])
@token_required
def delete_edc_machine(machine_id):
    """Delete EDC machine"""
    try:
        machine = EdcMachine.query.get(machine_id)
        
        if not machine:
            return error_response(
                message='EDC machine tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        db.session.delete(machine)
        db.session.commit()
        
        return success_response(
            data=None,
            message='EDC machine berhasil dihapus',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menghapus EDC machine',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@edc_bp.route('/<int:machine_id>/add-saldo', methods=['POST'])
@token_required
def add_edc_saldo(machine_id):
    """Add saldo to a specific EDC machine. Only accessible by owner role.

    Request body:
    {
        "amount": 100.00
        // or
        "saldo": 100.00
    }
    """
    try:
        user_id = request.user_id

        # Only owner allowed
        user = User.query.get(user_id)
        if not user or user.role != 'owner':
            return error_response(
                message='Hanya owner yang dapat menambah saldo EDC',
                error='FORBIDDEN',
                status_code=403
            )

        machine = EdcMachine.query.get(machine_id)
        if not machine:
            return error_response(
                message='EDC machine tidak ditemukan',
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

        # Accept either 'amount' or 'saldo'
        raw_amount = data.get('amount') if 'amount' in data else data.get('saldo')

        try:
            # Use Decimal for safe arithmetic with DB Numeric/Decimal fields
            amount = Decimal(str(raw_amount))
            if amount <= 0:
                return error_response(
                    message='Amount harus lebih besar dari 0',
                    error='INVALID_INPUT',
                    status_code=400
                )
        except (InvalidOperation, TypeError, ValueError):
            return error_response(
                message='Amount harus berupa angka',
                error='INVALID_INPUT',
                status_code=400
            )

        # Normalize existing saldo to Decimal
        try:
            current = Decimal(str(machine.saldo)) if machine.saldo is not None else Decimal('0')
        except (InvalidOperation, TypeError, ValueError):
            current = Decimal('0')

        machine.saldo = current + amount
        db.session.commit()

        return success_response(
            data=machine.to_dict(),
            message='Saldo EDC berhasil ditambahkan',
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menambah saldo EDC',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )


@edc_bp.route('/reset-all', methods=['POST'])
def reset_all_balances():
    """Owner-only: Reset semua saldo EDC, hapus semua cash flow (cash_in/cash_out),
    dan reset total_balance (tunai di tangan) semua agent menjadi 0.

    Response contains counts of affected rows for convenience.
    """
    try:
        # NOTE: No authentication/validation by design — this endpoint is intentionally open
        # and will reset all EDC balances, agent tunai and delete cash flow records.

        # Bulk reset EDC saldo -> 0
        edc_updated = db.session.query(EdcMachine).update({EdcMachine.saldo: 0})

        # Bulk reset agent total_balance -> 0
        agents_updated = db.session.query(AgentProfile).update({AgentProfile.total_balance: 0})

        # Delete all cash flow records
        cashflows_deleted = db.session.query(CashFlow).delete()

        db.session.commit()

        return success_response(
            data={
                'edc_machines_reset': int(edc_updated),
                'agents_reset': int(agents_updated),
                'cashflows_deleted': int(cashflows_deleted)
            },
            message='Semua saldo EDC, cash flow, dan tunai di tangan berhasil di-reset',
            status_code=200
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mereset data',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
