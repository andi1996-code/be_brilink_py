from flask import Blueprint, request
from models.user import db, User
from models.agent_profile import AgentProfile
from models.edc_machine import EdcMachine
from models.service import Service
from models.transaction import Transaction
from models.cash_flow import CashFlow
from utils.response import success_response, error_response
from utils.jwt_handler import token_required
from datetime import datetime, timedelta
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

def parse_date_range(request_obj):
    """
    Parse date range from request params
    Accept: start_date, end_date (Y-m-d), or days (int, default 7)
    """
    days = request_obj.args.get('days', 7, type=int)
    days = max(1, days)
    
    start_date_param = request_obj.args.get('start_date')
    end_date_param = request_obj.args.get('end_date')
    
    if start_date_param and end_date_param:
        try:
            start = datetime.strptime(start_date_param, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
            end = datetime.strptime(end_date_param, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
        except ValueError:
            return None, None
    else:
        end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        start = (end - timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    return start, end

@dashboard_bp.route('', methods=['GET'])
@token_required
def get_dashboard():
    """
    Get main dashboard metrics
    Params:
    - days: int (default 7)
    - start_date: YYYY-MM-DD
    - end_date: YYYY-MM-DD
    """
    try:
        user_id = request.user_id
        
        start, end = parse_date_range(request)
        if not start or not end:
            return error_response(
                message='Format date tidak valid. Gunakan YYYY-MM-DD',
                error='INVALID_DATE_FORMAT',
                status_code=400
            )
        
        # TODAY metrics
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        total_revenue_today = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0.00
        
        total_transactions_today = db.session.query(func.count(Transaction.id)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0
        
        # SALDO metrics (cumulative from all time)
        edc_saldo = db.session.query(func.sum(EdcMachine.saldo)).scalar() or 0.00
        
        cash_in_all = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_in'
        ).scalar() or 0.00
        
        cash_out_all = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_out'
        ).scalar() or 0.00
        
        # Convert to float to avoid Decimal - float error
        cash_in_all = float(cash_in_all)
        cash_out_all = float(cash_out_all)
        
        saldo_tunai = cash_in_all - cash_out_all
        
        # ACTIVE KASIR
        active_kasir = db.session.query(func.count(User.id)).filter(
            User.role == 'kasir'
        ).scalar() or 0
        
        # TOP SERVICES BY REVENUE in range
        top_by_revenue = db.session.query(
            Service.id.label('service_id'),
            Service.name,
            func.sum(Transaction.amount).label('revenue'),
            func.count(Transaction.id).label('count')
        ).join(Transaction, Service.id == Transaction.service_id).filter(
            Transaction.created_at.between(start, end)
        ).group_by(Service.id, Service.name).order_by(func.sum(Transaction.amount).desc()).limit(5).all()
        
        top_by_revenue_data = [
            {
                'service_id': row[0],
                'name': row[1],
                'revenue': float(row[2]) if row[2] else 0.00,
                'count': int(row[3]) if row[3] else 0
            }
            for row in top_by_revenue
        ]
        
        # TOP SERVICES BY VOLUME in range
        top_by_volume = db.session.query(
            Service.id.label('service_id'),
            Service.name,
            func.sum(Transaction.amount).label('revenue'),
            func.count(Transaction.id).label('count')
        ).join(Transaction, Service.id == Transaction.service_id).filter(
            Transaction.created_at.between(start, end)
        ).group_by(Service.id, Service.name).order_by(func.count(Transaction.id).desc()).limit(5).all()
        
        top_by_volume_data = [
            {
                'service_id': row[0],
                'name': row[1],
                'revenue': float(row[2]) if row[2] else 0.00,
                'count': int(row[3]) if row[3] else 0
            }
            for row in top_by_volume
        ]
        
        # DAILY TREND
        daily_trend_rows = db.session.query(
            func.date(Transaction.created_at).label('date'),
            func.sum(Transaction.amount).label('revenue'),
            func.count(Transaction.id).label('count')
        ).filter(
            Transaction.created_at.between(start, end)
        ).group_by(func.date(Transaction.created_at)).order_by(func.date(Transaction.created_at)).all()
        
        # Build daily trend period
        daily_trend = []
        cursor = start.replace(hour=0, minute=0, second=0, microsecond=0)
        trend_dict = {str(row[0]): row for row in daily_trend_rows}
        
        while cursor.date() <= end.date():
            date_str = cursor.strftime('%Y-%m-%d')
            row = trend_dict.get(date_str)
            daily_trend.append({
                'date': date_str,
                'revenue': float(row[1]) if row else 0.00,
                'count': int(row[2]) if row else 0
            })
            cursor += timedelta(days=1)
        
        # RECENT TRANSACTIONS
        recent_transactions = db.session.query(Transaction).order_by(
            Transaction.created_at.desc()
        ).limit(10).all()
        
        recent_transactions_data = []
        for t in recent_transactions:
            service = Service.query.get(t.service_id) if t.service_id else None
            edc = EdcMachine.query.get(t.edc_machine_id) if t.edc_machine_id else None
            agent = AgentProfile.query.get(t.agent_profile_id) if t.agent_profile_id else None
            user = User.query.get(t.user_id) if t.user_id else None
            
            recent_transactions_data.append({
                'id': t.id,
                'transaction_number': t.transaction_number,
                'amount': float(t.amount) if t.amount else 0.00,
                'service': {
                    'id': service.id,
                    'name': service.name
                } if service else None,
                'edc_machine': {
                    'id': edc.id,
                    'name': edc.name
                } if edc else None,
                'agent_profile': {
                    'id': agent.id,
                    'agent_name': agent.agent_name
                } if agent else None,
                'user': {
                    'id': user.id,
                    'name': user.name
                } if user else None,
                'created_at': t.created_at.isoformat() if t.created_at else None
            })
        
        return success_response(
            data={
                'total_revenue_today': float(total_revenue_today),
                'total_transactions_today': int(total_transactions_today),
                'saldo_tunai': float(saldo_tunai),
                'saldo_edc': float(edc_saldo),
                'active_kasir': int(active_kasir),
                'top_services_by_revenue': top_by_revenue_data,
                'top_services_by_volume': top_by_volume_data,
                'daily_trend': daily_trend,
                'recent_transactions': recent_transactions_data,
                'period': {
                    'start_date': start.strftime('%Y-%m-%d'),
                    'end_date': end.strftime('%Y-%m-%d')
                }
            },
            message='Dashboard data berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil dashboard data',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@dashboard_bp.route('/cashier', methods=['GET'])
@token_required
def get_cashier_dashboard():
    """
    Get cashier daily dashboard (today only) - GLOBAL DATA (no user filtering)
    Menampilkan data untuk kasir:
    - total_transactions_today: Total transaksi hari ini (semua user)
    - cash_out_today: Kas tunai keluar hari ini (semua user)
    - total_transfer_via_edc: Total transfer via EDC hari ini (semua user)
    - cash_on_hand: Kas tunai di tangan (dari semua agent.total_balance)
    - total_fees_today: Total fee hari ini (service_fee + bank_fee + extra_fee dari semua transaksi)
    """
    try:
        # NOTE: This endpoint shows GLOBAL data - no user filtering applied
        # All authenticated users can see the same dashboard data
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # 1. TOTAL TRANSAKSI HARI INI
        total_transactions_today = db.session.query(func.count(Transaction.id)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0
        
        # 2. KAS TUNAI KELUAR HARI INI (cash_out)
        cash_out_today = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_out',
            CashFlow.created_at.between(today_start, today_end)
        ).scalar() or 0.00
        
        # 3. TOTAL TRANSFER VIA EDC HARI INI
        total_transfer_via_edc = db.session.query(func.sum(Transaction.amount)).join(
            Service, Service.id == Transaction.service_id
        ).filter(
            Service.category.ilike('%transfer%'),
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0.00
        
        # 4. KAS TUNAI DI TANGAN (dari agent.total_balance - bukan dari cash flow)
        # Ambil semua agent dan jumlahkan total_balance mereka
        # placeholder: will compute cash_on_hand after fee aggregation
        cash_on_hand = 0.00

        # 5. TOTAL FEE HARI INI (service_fee + bank_fee + extra_fee)
        total_service_fee_today = db.session.query(func.sum(Transaction.service_fee)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0.00
        
        total_bank_fee_today = db.session.query(func.sum(Transaction.bank_fee)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0.00
        
        total_extra_fee_today = db.session.query(func.sum(Transaction.extra_fee)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0.00
        
        # Convert to float to avoid Decimal + float error
        total_service_fee_today = float(total_service_fee_today)
        total_bank_fee_today = float(total_bank_fee_today)
        total_extra_fee_today = float(total_extra_fee_today)
        
        total_fees_today = total_service_fee_today + total_bank_fee_today + total_extra_fee_today

        # Recompute saldo_tunai from cash flow (all time) and derive cash_on_hand
        cash_in_all = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_in'
        ).scalar() or 0.00
        cash_out_all = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_out'
        ).scalar() or 0.00
        cash_in_all = float(cash_in_all)
        cash_out_all = float(cash_out_all)
        saldo_tunai = cash_in_all - cash_out_all
        
        # cash_on_hand = saldo_tunai + today's service_fee + today's extra_fee
        cash_on_hand = saldo_tunai + total_service_fee_today + total_extra_fee_today
        
        return success_response(
            data={
                'date': today_start.strftime('%Y-%m-%d'),
                'total_transactions_today': int(total_transactions_today),
                'cash_out_today': float(cash_out_today),
                'total_transfer_via_edc': float(total_transfer_via_edc),
                'cash_on_hand': float(cash_on_hand),
                'total_fees_today': float(total_fees_today),
                # Breakdown fee untuk informasi tambahan
                'fee_breakdown': {
                    'service_fee': float(total_service_fee_today),
                    'bank_fee': float(total_bank_fee_today),
                    'extra_fee': float(total_extra_fee_today)
                }
            },
            message='Cashier dashboard data berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil cashier dashboard',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@dashboard_bp.route('/cashier/transactions', methods=['GET'])
@token_required
def get_cashier_transactions():
    """
    Get cashier transactions today with pagination
    Params:
    - per_page: int (default 25, max 200)
    - page: int (default 1)
    """
    try:
        user_id = request.user_id
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # PAGINATION
        per_page = request.args.get('per_page', 25, type=int)
        per_page = max(1, min(per_page, 200))  # min 1, max 200
        
        page = request.args.get('page', 1, type=int)
        page = max(1, page)
        
        # QUERY
        query = Transaction.query.filter(
            Transaction.created_at.between(today_start, today_end)
        ).order_by(Transaction.created_at.desc())
        
        total = query.count()
        
        # PAGINATION
        offset = (page - 1) * per_page
        transactions = query.limit(per_page).offset(offset).all()
        
        # TRANSFORM
        transactions_data = []
        for t in transactions:
            service = Service.query.get(t.service_id) if t.service_id else None
            edc = EdcMachine.query.get(t.edc_machine_id) if t.edc_machine_id else None
            agent = AgentProfile.query.get(t.agent_profile_id) if t.agent_profile_id else None
            user = User.query.get(t.user_id) if t.user_id else None
            
            transactions_data.append({
                'id': t.id,
                'transaction_number': t.transaction_number,
                'customer_name': t.customer_name,
                'amount': float(t.amount) if t.amount else 0.00,
                'service_fee': float(t.service_fee) if t.service_fee else 0.00,
                'bank_fee': float(t.bank_fee) if t.bank_fee else 0.00,
                'extra_fee': float(t.extra_fee) if t.extra_fee else 0.00,
                'reference_number': t.reference_number,
                'net_profit': float(t.net_profit) if t.net_profit else 0.00,
                'service': {
                    'id': service.id,
                    'name': service.name
                } if service else None,
                'edc_machine': {
                    'id': edc.id,
                    'name': edc.name
                } if edc else None,
                'agent_profile': {
                    'id': agent.id,
                    'agent_name': agent.agent_name
                } if agent else None,
                'user': {
                    'id': user.id,
                    'name': user.name
                } if user else None,
                'created_at': t.created_at.isoformat() if t.created_at else None
            })
        
        # CALCULATE last_page
        last_page = (total + per_page - 1) // per_page if total > 0 else 1
        
        return success_response(
            data={
                'date': today_start.strftime('%Y-%m-%d'),
                'meta': {
                    'total': total,
                    'per_page': per_page,
                    'current_page': page,
                    'last_page': last_page
                },
                'transactions': transactions_data
            },
            message='Cashier transactions berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil cashier transactions',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

# ===== DASHBOARD CARDS API =====

@dashboard_bp.route('/cards/total-revenue-today', methods=['GET'])
@token_required
def get_total_revenue_today():
    """
    Get total revenue for today
    """
    try:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        total_revenue = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0.00
        
        return success_response(
            data={
                'total_revenue_today': float(total_revenue),
                'date': today_start.strftime('%Y-%m-%d')
            },
            message='Total pendapatan hari ini berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil total pendapatan hari ini',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@dashboard_bp.route('/cards/saldo-tunai', methods=['GET'])
@token_required
def get_saldo_tunai():
    """
    Get current cash balance (saldo tunai)
    """
    try:
        cash_in_all = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_in'
        ).scalar() or 0.00
        
        cash_out_all = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_out'
        ).scalar() or 0.00
        
        # Convert to float to avoid Decimal - float error
        cash_in_all = float(cash_in_all)
        cash_out_all = float(cash_out_all)
        
        saldo_tunai = cash_in_all - cash_out_all
        
        return success_response(
            data={
                'saldo_tunai': float(saldo_tunai),
                'cash_in_total': float(cash_in_all),
                'cash_out_total': float(cash_out_all)
            },
            message='Saldo tunai berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil saldo tunai',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@dashboard_bp.route('/cards/saldo-edc', methods=['GET'])
@token_required
def get_saldo_edc():
    """
    Get total EDC machine balance (saldo EDC)
    """
    try:
        edc_saldo = db.session.query(func.sum(EdcMachine.saldo)).scalar() or 0.00
        
        return success_response(
            data={
                'saldo_edc': float(edc_saldo)
            },
            message='Saldo EDC berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil saldo EDC',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@dashboard_bp.route('/cards/total-transactions-today', methods=['GET'])
@token_required
def get_total_transactions_today():
    """
    Get total transactions count for today
    """
    try:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        total_transactions = db.session.query(func.count(Transaction.id)).filter(
            Transaction.created_at.between(today_start, today_end)
        ).scalar() or 0
        
        return success_response(
            data={
                'total_transactions_today': int(total_transactions),
                'date': today_start.strftime('%Y-%m-%d')
            },
            message='Total transaksi hari ini berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil total transaksi hari ini',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@dashboard_bp.route('/cards/recent-transactions', methods=['GET'])
@token_required
def get_recent_transactions():
    """
    Get recent transactions (latest 10)
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = max(1, min(limit, 50))  # min 1, max 50
        
        recent_transactions = db.session.query(Transaction).order_by(
            Transaction.created_at.desc()
        ).limit(limit).all()
        
        transactions_data = []
        for t in recent_transactions:
            service = Service.query.get(t.service_id) if t.service_id else None
            edc = EdcMachine.query.get(t.edc_machine_id) if t.edc_machine_id else None
            agent = AgentProfile.query.get(t.agent_profile_id) if t.agent_profile_id else None
            user = User.query.get(t.user_id) if t.user_id else None
            
            transactions_data.append({
                'id': t.id,
                'transaction_number': t.transaction_number,
                'amount': float(t.amount) if t.amount else 0.00,
                'service': {
                    'id': service.id,
                    'name': service.name
                } if service else None,
                'edc_machine': {
                    'id': edc.id,
                    'name': edc.name
                } if edc else None,
                'agent_profile': {
                    'id': agent.id,
                    'agent_name': agent.agent_name
                } if agent else None,
                'user': {
                    'id': user.id,
                    'name': user.name
                } if user else None,
                'created_at': t.created_at.isoformat() if t.created_at else None
            })
        
        return success_response(
            data={
                'recent_transactions': transactions_data,
                'limit': limit
            },
            message='Transaksi terbaru berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil transaksi terbaru',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
