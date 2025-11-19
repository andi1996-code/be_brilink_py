from flask import Blueprint, request
from models.user import db, User
from models.agent_profile import AgentProfile
from models.cash_flow import CashFlow
from models.transaction import Transaction
from models.service import Service
from utils.response import success_response, error_response
from datetime import datetime, timedelta
from sqlalchemy import func

cashier_bp = Blueprint('cashier', __name__, url_prefix='/api/cashier')


def parse_date_range(request_obj):
    """
    Parse single date from request params
    Accept: date or start_date (Y-m-d) or default today
    Returns start and end for that day (00:00 to 23:59:59.999999)
    """
    # Prefer explicit 'date' param, fallback to 'start_date'
    date_param = request_obj.args.get('date') or request_obj.args.get('start_date')
    if date_param:
        try:
            d = datetime.strptime(date_param, '%Y-%m-%d')
            start = d.replace(hour=0, minute=0, second=0, microsecond=0)
            end = d.replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            return None, None
    else:
        # default to today
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    return start, end


@cashier_bp.route('/uangmasuk', methods=['GET'])
def get_uang_masuk():
    """
    Endpoint to get aggregated total transfer amount (before fees) for a card (single response)
    Params:
    - agent_id: filter by agent profile id (optional)
    - start_date: YYYY-MM-DD
    - end_date: YYYY-MM-DD
    - days: int (default 1)
    """
    try:
        # no authentication; public endpoint — user_id not required

        start, end = parse_date_range(request)
        if not start or not end:
            return error_response(
                message='Format date tidak valid. Gunakan YYYY-MM-DD',
                error='INVALID_DATE_FORMAT',
                status_code=400
            )

        agent_id = request.args.get('agent_id')

        # Parse agent_id (optional) - no ownership validation (open to all authenticated users)
        if agent_id is not None:
            try:
                agent_id = int(agent_id)
            except (ValueError, TypeError):
                return error_response(
                    message='agent_id harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )

        # Calculate transfer total from transactions (service.category contains transfer)
        transfer_query = db.session.query(func.sum(Transaction.amount)).join(
            Service, Service.id == Transaction.service_id
        ).filter(
            Service.category.ilike('%transfer%'),
            Transaction.created_at.between(start, end)
        )
        if agent_id is not None:
            transfer_query = transfer_query.filter(Transaction.agent_profile_id == agent_id)
        total_transfer = transfer_query.scalar() or 0.00

        return success_response(
            data={
                'period': {
                    'start_date': start.strftime('%Y-%m-%d'),
                    'end_date': end.strftime('%Y-%m-%d')
                },
                # amount before fees (Transaction.amount is final customer amount)
                'total_transfer': float(total_transfer)
            },
            message='Data uang masuk (transfer only) berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data uang masuk',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
