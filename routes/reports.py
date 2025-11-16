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

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

def parse_report_date_range(request_obj):
    """
    Parse date range for reports
    Accept: period (daily, weekly, monthly, custom), year, month, start_date, end_date
    """
    period = request_obj.args.get('period', 'monthly')

    now = datetime.now()

    if period == 'daily':
        # Today
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        period_name = f"Harian - {start.strftime('%d %B %Y')}"

    elif period == 'weekly':
        # Current week (Monday to Sunday)
        start = now - timedelta(days=now.weekday())  # Monday
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
        period_name = f"Mingguan - {start.strftime('%d %b')} sampai {end.strftime('%d %b %Y')}"

    elif period == 'monthly':
        # Current month
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Next month, first day, minus 1 second
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        else:
            end = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        period_name = f"Bulanan - {start.strftime('%B %Y')}"

    elif period == 'yearly':
        # Current year
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        period_name = f"Tahunan - {start.strftime('%Y')}"

    elif period == 'custom':
        start_date_param = request_obj.args.get('start_date')
        end_date_param = request_obj.args.get('end_date')

        if not start_date_param or not end_date_param:
            return None, None, None

        try:
            start = datetime.strptime(start_date_param, '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
            end = datetime.strptime(end_date_param, '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999999)
            period_name = f"Custom - {start.strftime('%d %b %Y')} sampai {end.strftime('%d %b %Y')}"
        except ValueError:
            return None, None, None

    else:
        # Default to monthly
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        else:
            end = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
        period_name = f"Bulanan - {start.strftime('%B %Y')}"

    return start, end, period_name

@reports_bp.route('', methods=['GET'])
@token_required
def get_reports():
    """
    Get comprehensive reports for different periods
    Params:
    - period: daily, weekly, monthly, yearly, custom (default: monthly)
    - start_date: YYYY-MM-DD (for custom period)
    - end_date: YYYY-MM-DD (for custom period)
    """
    try:
        start, end, period_name = parse_report_date_range(request)
        if not start or not end:
            return error_response(
                message='Parameter periode tidak valid. Gunakan period=custom dengan start_date dan end_date, atau period=daily/weekly/monthly/yearly',
                error='INVALID_PERIOD',
                status_code=400
            )

        # ===== REVENUE & TRANSACTIONS =====
        total_revenue_result = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.created_at.between(start, end)
        ).scalar()
        total_revenue = float(total_revenue_result) if total_revenue_result is not None else 0.00

        total_transactions = db.session.query(func.count(Transaction.id)).filter(
            Transaction.created_at.between(start, end)
        ).scalar() or 0

        avg_transaction_amount = total_revenue / total_transactions if total_transactions > 0 else 0.00

        # ===== FEES BREAKDOWN =====
        total_service_fee_result = db.session.query(func.sum(Transaction.service_fee)).filter(
            Transaction.created_at.between(start, end)
        ).scalar()
        total_service_fee = float(total_service_fee_result) if total_service_fee_result is not None else 0.00

        total_bank_fee_result = db.session.query(func.sum(Transaction.bank_fee)).filter(
            Transaction.created_at.between(start, end)
        ).scalar()
        total_bank_fee = float(total_bank_fee_result) if total_bank_fee_result is not None else 0.00

        total_extra_fee_result = db.session.query(func.sum(Transaction.extra_fee)).filter(
            Transaction.created_at.between(start, end)
        ).scalar()
        total_extra_fee = float(total_extra_fee_result) if total_extra_fee_result is not None else 0.00

        total_fees = total_service_fee + total_bank_fee + total_extra_fee

        # ===== NET PROFIT =====
        total_net_profit_result = db.session.query(func.sum(Transaction.net_profit)).filter(
            Transaction.created_at.between(start, end)
        ).scalar()
        total_net_profit = float(total_net_profit_result) if total_net_profit_result is not None else 0.00

        # ===== CASH FLOW =====
        cash_in_result = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_in',
            CashFlow.created_at.between(start, end)
        ).scalar()
        cash_in_period = float(cash_in_result) if cash_in_result is not None else 0.00

        cash_out_result = db.session.query(func.sum(CashFlow.amount)).filter(
            CashFlow.type == 'cash_out',
            CashFlow.created_at.between(start, end)
        ).scalar()
        cash_out_period = float(cash_out_result) if cash_out_result is not None else 0.00

        net_cash_flow = cash_in_period - cash_out_period

        # ===== SERVICE BREAKDOWN =====
        service_breakdown = db.session.query(
            Service.id.label('service_id'),
            Service.name,
            Service.category,
            func.sum(Transaction.amount).label('revenue'),
            func.count(Transaction.id).label('count'),
            func.sum(Transaction.service_fee).label('service_fee_total'),
            func.sum(Transaction.bank_fee).label('bank_fee_total'),
            func.sum(Transaction.net_profit).label('net_profit_total')
        ).join(Transaction, Service.id == Transaction.service_id).filter(
            Transaction.created_at.between(start, end)
        ).group_by(Service.id, Service.name, Service.category).order_by(func.sum(Transaction.amount).desc()).all()

        service_data = []
        for row in service_breakdown:
            service_data.append({
                'service_id': row[0],
                'name': row[1],
                'category': row[2],
                'revenue': float(row[3]) if row[3] is not None else 0.00,
                'transaction_count': int(row[4]) if row[4] is not None else 0,
                'service_fee_total': float(row[5]) if row[5] is not None else 0.00,
                'bank_fee_total': float(row[6]) if row[6] is not None else 0.00,
                'net_profit_total': float(row[7]) if row[7] is not None else 0.00
            })

        # ===== DAILY BREAKDOWN (for weekly/monthly reports) =====
        daily_breakdown = []
        if (end - start).days > 1:  # Only for periods longer than 1 day
            daily_rows = db.session.query(
                func.date(Transaction.created_at).label('date'),
                func.sum(Transaction.amount).label('revenue'),
                func.count(Transaction.id).label('count'),
                func.sum(Transaction.net_profit).label('net_profit')
            ).filter(
                Transaction.created_at.between(start, end)
            ).group_by(func.date(Transaction.created_at)).order_by(func.date(Transaction.created_at)).all()

            # Fill in missing dates with zero values
            cursor = start.replace(hour=0, minute=0, second=0, microsecond=0)
            daily_dict = {str(row[0]): row for row in daily_rows}

            while cursor.date() <= end.date():
                date_str = cursor.strftime('%Y-%m-%d')
                row = daily_dict.get(date_str)
                daily_breakdown.append({
                    'date': date_str,
                    'revenue': float(row[1]) if row and row[1] is not None else 0.00,
                    'transaction_count': int(row[2]) if row and row[2] is not None else 0,
                    'net_profit': float(row[3]) if row and row[3] is not None else 0.00
                })
                cursor += timedelta(days=1)

        # ===== EDC MACHINE PERFORMANCE =====
        edc_performance = db.session.query(
            EdcMachine.id.label('edc_id'),
            EdcMachine.name,
            func.sum(Transaction.amount).label('revenue'),
            func.count(Transaction.id).label('count')
        ).join(Transaction, EdcMachine.id == Transaction.edc_machine_id).filter(
            Transaction.created_at.between(start, end)
        ).group_by(EdcMachine.id, EdcMachine.name).order_by(func.sum(Transaction.amount).desc()).all()

        edc_data = []
        for row in edc_performance:
            edc_data.append({
                'edc_id': row[0],
                'name': row[1],
                'revenue': float(row[2]) if row[2] is not None else 0.00,
                'transaction_count': int(row[3]) if row[3] is not None else 0
            })

        # ===== AGENT PERFORMANCE (if multi-agent enabled in future) =====
        agent_performance = db.session.query(
            AgentProfile.id.label('agent_id'),
            AgentProfile.agent_name,
            func.sum(Transaction.amount).label('revenue'),
            func.count(Transaction.id).label('count')
        ).join(Transaction, AgentProfile.id == Transaction.agent_profile_id).filter(
            Transaction.created_at.between(start, end)
        ).group_by(AgentProfile.id, AgentProfile.agent_name).order_by(func.sum(Transaction.amount).desc()).all()

        agent_data = []
        for row in agent_performance:
            agent_data.append({
                'agent_id': row[0],
                'agent_name': row[1],
                'revenue': float(row[2]) if row[2] is not None else 0.00,
                'transaction_count': int(row[3]) if row[3] is not None else 0
            })

        return success_response(
            data={
                'period': {
                    'name': period_name,
                    'start_date': start.strftime('%Y-%m-%d'),
                    'end_date': end.strftime('%Y-%m-%d'),
                    'days': (end - start).days + 1
                },
                'summary': {
                    'total_revenue': float(total_revenue),
                    'total_transactions': int(total_transactions),
                    'avg_transaction_amount': float(avg_transaction_amount),
                    'total_fees': float(total_fees),
                    'total_net_profit': float(total_net_profit),
                    'cash_in': float(cash_in_period),
                    'cash_out': float(cash_out_period),
                    'net_cash_flow': float(net_cash_flow)
                },
                'fees_breakdown': {
                    'service_fee': float(total_service_fee),
                    'bank_fee': float(total_bank_fee),
                    'extra_fee': float(total_extra_fee)
                },
                'service_breakdown': service_data,
                'daily_breakdown': daily_breakdown,
                'edc_performance': edc_data,
                'agent_performance': agent_data
            },
            message='Laporan berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil laporan',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )