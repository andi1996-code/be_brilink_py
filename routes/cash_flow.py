from flask import Blueprint, request
from models.user import db, User
from models.agent_profile import AgentProfile
from models.cash_flow import CashFlow
from utils.response import success_response, error_response
from utils.jwt_handler import token_required

cash_flow_bp = Blueprint('cash_flow', __name__, url_prefix='/api/cash-flows')

def check_agent_ownership(user_id, agent_id):
    """Check if user owns the agent profile"""
    agent = AgentProfile.query.get(agent_id)
    if not agent:
        return False
    
    # If user is the direct owner of the agent
    if agent.user_id == user_id:
        return True
    
    # If user is owner role and agent.owner_id matches
    user = User.query.get(user_id)
    if user and user.role == 'owner' and agent.owner_id == user_id:
        return True
    
    return False

@cash_flow_bp.route('', methods=['GET'])
@token_required
def get_cash_flows():
    """Get cash flows for user's agents"""
    try:
        user_id = request.user_id
        agent_id = request.args.get('agent_id')
        cash_type = request.args.get('type')  # cash_in atau cash_out
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = CashFlow.query.filter_by(user_id=user_id)
        
        if agent_id:
            if not check_agent_ownership(user_id, int(agent_id)):
                return error_response(
                    message='Anda tidak memiliki akses ke agent profile ini',
                    error='FORBIDDEN',
                    status_code=403
                )
            query = query.filter_by(agent_profile_id=int(agent_id))
        
        if cash_type:
            if cash_type not in ['cash_in', 'cash_out']:
                return error_response(
                    message='Type harus "cash_in" atau "cash_out"',
                    error='INVALID_INPUT',
                    status_code=400
                )
            query = query.filter_by(type=cash_type)
        
        total = query.count()
        cash_flows = query.order_by(CashFlow.created_at.desc()).limit(limit).offset(offset).all()
        
        return success_response(
            data={
                "cash_flows": [cf.to_dict() for cf in cash_flows],
                "total": total,
                "limit": limit,
                "offset": offset
            },
            message='Data cash flow berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data cash flow',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@cash_flow_bp.route('/<int:cash_flow_id>', methods=['GET'])
@token_required
def get_cash_flow(cash_flow_id):
    """Get specific cash flow"""
    try:
        user_id = request.user_id
        
        cash_flow = CashFlow.query.get(cash_flow_id)
        
        if not cash_flow:
            return error_response(
                message='Cash flow tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        if cash_flow.user_id != user_id:
            if cash_flow.agent_profile_id and not check_agent_ownership(user_id, cash_flow.agent_profile_id):
                return error_response(
                    message='Anda tidak memiliki akses ke cash flow ini',
                    error='FORBIDDEN',
                    status_code=403
                )
        
        return success_response(
            data=cash_flow.to_dict(),
            message='Data cash flow berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data cash flow',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@cash_flow_bp.route('', methods=['POST'])
@token_required
def create_cash_flow():
    """
    Create new cash flow
    
    Request body:
    {
        "agent_profile_id": 1,  // optional
        "type": "cash_in",
        "source": "Transfer",
        "amount": 100000.00,
        "description": "Cash in from transfer"
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
        cash_type = data.get('type', '').lower()
        source = data.get('source', '').strip()
        amount = data.get('amount', 0)
        description = data.get('description', '').strip() if data.get('description') else None
        
        # Validate required fields
        if not cash_type or not source:
            return error_response(
                message='type dan source wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # Validate type
        if cash_type not in ['cash_in', 'cash_out']:
            return error_response(
                message='Type harus "cash_in" atau "cash_out"',
                error='INVALID_INPUT',
                status_code=400
            )
        
        # Validate amount
        try:
            amount = float(amount)
            if amount <= 0:
                return error_response(
                    message='Amount harus lebih dari 0',
                    error='INVALID_INPUT',
                    status_code=400
                )
        except (ValueError, TypeError):
            return error_response(
                message='Amount harus berupa angka',
                error='INVALID_INPUT',
                status_code=400
            )
        
        new_cash_flow = CashFlow(
            agent_profile_id=agent_profile_id,
            user_id=user_id,
            type=cash_type,
            source=source,
            amount=amount,
            description=description
        )
        
        db.session.add(new_cash_flow)
        db.session.commit()
        
        return success_response(
            data=new_cash_flow.to_dict(),
            message='Cash flow berhasil dibuat',
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat membuat cash flow',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@cash_flow_bp.route('/<int:cash_flow_id>', methods=['PUT'])
@token_required
def update_cash_flow(cash_flow_id):
    """Update cash flow"""
    try:
        user_id = request.user_id
        
        cash_flow = CashFlow.query.get(cash_flow_id)
        
        if not cash_flow:
            return error_response(
                message='Cash flow tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        if cash_flow.user_id != user_id:
            return error_response(
                message='Anda tidak memiliki akses untuk mengubah cash flow ini',
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
        
        if 'description' in data:
            cash_flow.description = data.get('description', '').strip() or None
        
        if 'source' in data:
            source = data.get('source', '').strip()
            if not source:
                return error_response(
                    message='Source tidak boleh kosong',
                    error='INVALID_INPUT',
                    status_code=400
                )
            cash_flow.source = source
        
        if 'amount' in data:
            try:
                amount = float(data.get('amount'))
                if amount <= 0:
                    return error_response(
                        message='Amount harus lebih dari 0',
                        error='INVALID_INPUT',
                        status_code=400
                    )
                cash_flow.amount = amount
            except (ValueError, TypeError):
                return error_response(
                    message='Amount harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )
        
        db.session.commit()
        
        return success_response(
            data=cash_flow.to_dict(),
            message='Cash flow berhasil diubah',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat mengubah cash flow',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@cash_flow_bp.route('/<int:cash_flow_id>', methods=['DELETE'])
@token_required
def delete_cash_flow(cash_flow_id):
    """Delete cash flow"""
    try:
        user_id = request.user_id
        
        cash_flow = CashFlow.query.get(cash_flow_id)
        
        if not cash_flow:
            return error_response(
                message='Cash flow tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        if cash_flow.user_id != user_id:
            return error_response(
                message='Anda tidak memiliki akses untuk menghapus cash flow ini',
                error='FORBIDDEN',
                status_code=403
            )
        
        db.session.delete(cash_flow)
        db.session.commit()
        
        return success_response(
            data=None,
            message='Cash flow berhasil dihapus',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menghapus cash flow',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
