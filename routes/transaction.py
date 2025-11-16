from flask import Blueprint, request, send_file
from models.user import db, User
from models.agent_profile import AgentProfile
from models.edc_machine import EdcMachine
from models.service import Service
from models.service_fee import ServiceFee
from models.bank_fee import BankFee
from models.transaction import Transaction
from models.cash_flow import CashFlow
from utils.response import success_response, error_response
from utils.jwt_handler import token_required
import uuid
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import io

transaction_bp = Blueprint('transaction', __name__, url_prefix='/api/transactions')

def check_agent_ownership(user_id, agent_id):
    """Check if user owns the agent profile"""
    agent = AgentProfile.query.get(agent_id)
    if not agent or agent.user_id != user_id:
        return False
    return True

def generate_transaction_number():
    """Generate unique transaction number"""
    return f"TRX-{uuid.uuid4().hex[:12].upper()}"

def get_service_fee(service_id, amount):
    """
    Get service fee berdasarkan service_id dan amount
    Mencari fee yang sesuai dengan range amount
    """
    try:
        service_fee = ServiceFee.query.filter(
            ServiceFee.service_id == service_id,
            ServiceFee.min_amount <= amount,
            ServiceFee.max_amount >= amount
        ).first()
        
        if service_fee:
            return float(service_fee.fee)
        return 0.00
    except Exception:
        return 0.00

def get_bank_fee(edc_machine_id, service_id):
    """
    Get bank fee berdasarkan edc_machine_id dan service_id
    """
    try:
        bank_fee = BankFee.query.filter(
            BankFee.edc_machine_id == edc_machine_id,
            BankFee.service_id == service_id
        ).first()
        
        if bank_fee:
            return float(bank_fee.fee)
        return 0.00
    except Exception:
        return 0.00

@transaction_bp.route('', methods=['GET'])
@token_required
def get_transactions():
    """Get all transactions (accessible by all authenticated users)"""
    try:
        agent_id = request.args.get('agent_id')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = Transaction.query
        
        if agent_id:
            query = query.filter_by(agent_profile_id=int(agent_id))
        # No ownership restriction - all authenticated users can see all transactions
        
        total = query.count()
        transactions = query.order_by(Transaction.created_at.desc()).limit(limit).offset(offset).all()
        
        return success_response(
            data={
                "transactions": [trx.to_dict() for trx in transactions],
                "total": total,
                "limit": limit,
                "offset": offset
            },
            message='Data transaction berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data transaction',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
@token_required
def get_transaction(transaction_id):
    """Get specific transaction (accessible by all authenticated users)"""
    try:
        transaction = Transaction.query.get(transaction_id)
        
        if not transaction:
            return error_response(
                message='Transaction tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # No ownership check - accessible by all authenticated users
        
        return success_response(
            data=transaction.to_dict(),
            message='Data transaction berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data transaction',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@transaction_bp.route('/today', methods=['GET'])
@token_required
def get_today_transactions():
    """Get all transactions for today (cashier endpoint - accessible by all authenticated users)"""
    try:
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        transactions = Transaction.query.filter(
            Transaction.created_at >= today,
            Transaction.created_at < tomorrow
        ).order_by(Transaction.created_at.desc()).all()
        
        return success_response(
            data={
                "transactions": [trx.to_dict() for trx in transactions],
                "total": len(transactions)
            },
            message='Data transaksi hari ini berhasil diambil',
            status_code=200
        )
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat mengambil data transaksi hari ini',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@transaction_bp.route('/report/daily/pdf', methods=['GET'])
@token_required
def download_daily_report_pdf():
    """Download PDF report of today's transactions"""
    try:
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        # Get current user info
        current_user = User.query.get(request.user_id)
        cashier_name = current_user.name if current_user else "Unknown"
        
        # Get today's transactions
        transactions = Transaction.query.filter(
            Transaction.created_at >= today,
            Transaction.created_at < tomorrow
        ).order_by(Transaction.created_at.asc()).all()
        
        # Get unique cashier names from transactions
        cashier_names = list(set(trx.cashier_name for trx in transactions if trx.cashier_name))
        report_cashier_name = ", ".join(cashier_names) if cashier_names else cashier_name
        
        # Calculate summary statistics
        total_transactions = len(transactions)
        total_amount = sum(float(trx.amount) for trx in transactions) if transactions else 0
        total_service_fee = sum(float(trx.service_fee) for trx in transactions) if transactions else 0
        total_bank_fee = sum(float(trx.bank_fee) for trx in transactions) if transactions else 0
        total_extra_fee = sum(float(trx.extra_fee) for trx in transactions) if transactions else 0
        total_net_profit = sum(float(trx.net_profit) for trx in transactions) if transactions else 0
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph("Laporan Transaksi Harian", title_style))
        story.append(Spacer(1, 12))
        
        # Report info
        info_style = styles['Normal']
        story.append(Paragraph(f"Tanggal: {today.strftime('%d %B %Y')}", info_style))
        story.append(Paragraph(f"Kasir: {report_cashier_name}", info_style))
        story.append(Paragraph(f"Waktu Generate: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", info_style))
        story.append(Spacer(1, 20))
        
        # Summary section
        summary_style = ParagraphStyle(
            'SummaryHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10
        )
        story.append(Paragraph("Ringkasan Transaksi", summary_style))
        
        # Summary data
        summary_data = [
            ["Total Transaksi", f"{total_transactions} transaksi"],
            ["Total Nominal", f"Rp {total_amount:,.0f}"],
            ["Total Service Fee", f"Rp {total_service_fee:,.0f}"],
            ["Total Bank Fee", f"Rp {total_bank_fee:,.0f}"],
            ["Total Extra Fee", f"Rp {total_extra_fee:,.0f}"],
            ["Total Net Profit", f"Rp {total_net_profit:,.0f}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[200, 200])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Transactions table
        if transactions:
            transactions_style = ParagraphStyle(
                'TransactionsHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=10
            )
            story.append(Paragraph("Detail Transaksi", transactions_style))
            
            # Table headers
            table_data = [["No", "Waktu", "No. Transaksi", "Kasir", "Customer", "Service", "Amount", "Service Fee", "Bank Fee", "Net Profit"]]
            
            # Table rows
            for i, trx in enumerate(transactions, 1):
                # Get service name
                service = Service.query.get(trx.service_id)
                service_name = service.name if service else "Unknown"
                
                row = [
                    str(i),
                    trx.created_at.strftime('%H:%M:%S'),
                    trx.transaction_number,
                    trx.cashier_name or "-",
                    trx.customer_name or "-",
                    service_name,
                    f"Rp {float(trx.amount):,.0f}",
                    f"Rp {float(trx.service_fee):,.0f}",
                    f"Rp {float(trx.bank_fee):,.0f}",
                    f"Rp {float(trx.net_profit):,.0f}"
                ]
                table_data.append(row)
            
            # Create table
            col_widths = [25, 50, 90, 60, 60, 60, 70, 55, 55, 65]
            transactions_table = Table(table_data, colWidths=col_widths)
            
            # Style the table
            transactions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Center first column
                ('ALIGN', (5, 1), (8, -1), 'RIGHT'),   # Right align numeric columns
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            story.append(transactions_table)
        else:
            story.append(Paragraph("Tidak ada transaksi hari ini.", styles['Normal']))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.gray,
            alignment=1
        )
        story.append(Paragraph("Laporan ini dihasilkan secara otomatis oleh sistem Brilink", footer_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        # Return PDF file
        filename = f'laporan-transaksi-{today.strftime("%Y-%m-%d")}.pdf'
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return error_response(
            message='Terjadi kesalahan saat generate laporan PDF',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@transaction_bp.route('', methods=['POST'])
@token_required
def create_transaction():
    """
    Create new transaction
    Service fee dan bank fee akan otomatis terisi berdasarkan:
    - Service fee: dari tabel service_fees berdasarkan service_id dan amount range
    - Bank fee: dari tabel bank_fees berdasarkan edc_machine_id dan service_id
    """
    try:
        user_id = request.user_id
        
        # Get current user info for cashier name
        current_user = User.query.get(user_id)
        cashier_name = current_user.name if current_user else "Unknown"
        
        data = request.get_json()
        
        if not data:
            return error_response(
                message='Request body tidak boleh kosong',
                error='INVALID_REQUEST',
                status_code=400
            )
        
        edc_machine_id = data.get('edc_machine_id')
        service_id = data.get('service_id')
        agent_profile_id = data.get('agent_profile_id')  # Optional now
        customer_name = data.get('customer_name', '').strip()
        target_number = data.get('target_number', '').strip() if data.get('target_number') else None
        reference_number = data.get('reference_number', '').strip() if data.get('reference_number') else None
        amount = data.get('amount', 0)
        extra_fee = data.get('extra_fee', 0)  # extra_fee bisa di-set manual
        
        # Validate required fields
        if not edc_machine_id or not service_id:
            return error_response(
                message='edc_machine_id dan service_id wajib diisi',
                error='MISSING_FIELDS',
                status_code=400
            )
        
        # No ownership check - accessible by all authenticated users
        
        # Check EDC machine exists
        edc = EdcMachine.query.get(edc_machine_id)
        if not edc:
            return error_response(
                message='EDC machine tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # Check service exists
        service = Service.query.get(service_id)
        if not service:
            return error_response(
                message='Service tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        # Get agent profile untuk cek uang tunai (jika ada)
        agent = None
        if agent_profile_id is not None:
            try:
                agent_profile_id = int(agent_profile_id)
            except (ValueError, TypeError):
                return error_response(
                    message='agent_profile_id harus berupa angka',
                    error='INVALID_INPUT',
                    status_code=400
                )
            agent = AgentProfile.query.get(agent_profile_id)
            if not agent:
                return error_response(
                    message='Agent profile tidak ditemukan',
                    error='NOT_FOUND',
                    status_code=404
                )
        
        # Validate amount
        try:
            amount = float(amount)
            extra_fee = float(extra_fee)
            
            if amount <= 0:
                return error_response(
                    message='Amount harus lebih dari 0',
                    error='INVALID_INPUT',
                    status_code=400
                )
            
            if extra_fee < 0:
                return error_response(
                    message='Extra fee tidak boleh negatif',
                    error='INVALID_INPUT',
                    status_code=400
                )
        except (ValueError, TypeError):
            return error_response(
                message='Amount harus berupa angka',
                error='INVALID_INPUT',
                status_code=400
            )
        
        # VALIDASI SALDO: Pastikan saldo EDC atau uang tunai cukup sesuai service category
        edc_saldo = float(edc.saldo) if edc.saldo else 0.00
        agent_tunai = float(agent.total_balance) if agent and agent.total_balance else 0.00
        
        if service.category and service.category.lower() == "transfer":
            # Transfer: butuh saldo EDC cukup
            if edc_saldo < amount:
                return error_response(
                    message=f'Saldo EDC tidak cukup. Saldo tersedia: {edc_saldo}, Amount dibutuhkan: {amount}',
                    error='INSUFFICIENT_BALANCE',
                    status_code=400
                )
        elif service.category and service.category.lower() == "tarik tunai":
            # Tarik tunai: agent opsional. Jika agent diberikan, pastikan saldo tunai cukup.
            if agent:
                if agent_tunai < amount:
                    return error_response(
                        message=f'Uang tunai tidak cukup. Saldo tersedia: {agent_tunai}, Amount dibutuhkan: {amount}',
                        error='INSUFFICIENT_BALANCE',
                        status_code=400
                    )
        
        # AUTO-FILL: Get service fee dari database berdasarkan amount range
        service_fee = get_service_fee(service_id, amount)
        
        # AUTO-FILL: Get bank fee dari database berdasarkan edc_machine_id dan service_id
        bank_fee = get_bank_fee(edc_machine_id, service_id)
        
        # Calculate total yang harus dikumpulkan (amount adalah nilai final, tidak boleh dipotong)
        # total = amount (yang diterima customer) + service_fee + bank_fee + extra_fee
        total_received = amount + service_fee + bank_fee + extra_fee
        
        # Net profit = amount yang diterima dikurangi extra fee
        net_profit = amount - extra_fee
        
        # Info yang di-return untuk user
        fee_info = {
            "service_fee_source": "auto-calculated",
            "bank_fee_source": "auto-calculated",
            "calculation_details": {
                "amount": f"nilai final yang diterima customer (tidak dipotong)",
                "service_fee": "otomatis dari service_fees tabel (amount range)",
                "bank_fee": "otomatis dari bank_fees tabel (edc + service)",
                "extra_fee": "biaya tambahan manual (opsional)",
                "total_received": f"amount + service_fee + bank_fee + extra_fee = {total_received}",
                "net_profit": f"amount - extra_fee = {net_profit}"
            }
        }
        
        new_transaction = Transaction(
            transaction_number=generate_transaction_number(),
            edc_machine_id=edc_machine_id,
            service_id=service_id,
            agent_profile_id=agent_profile_id,
            user_id=user_id,
            cashier_name=cashier_name,
            customer_name=customer_name if customer_name else None,
            target_number=target_number,
            reference_number=reference_number,
            amount=amount,
            service_fee=service_fee,
            bank_fee=bank_fee,
            extra_fee=extra_fee,
            net_profit=net_profit
        )
        
        db.session.add(new_transaction)
        db.session.commit()
        
        # Update EDC machine saldo dan create cash flow berdasarkan service category (jika agent ada)
        try:
            if service.category and service.category.lower() == "transfer":
                # Transfer: saldo EDC berkurang, uang tunai bertambah (cash_in)
                edc.saldo = float(edc.saldo) - amount
                db.session.add(edc)
                if agent:
                    agent.total_balance = float(agent.total_balance) + amount
                    db.session.add(agent)
                    
                    # Catat cash_in (uang masuk)
                    cash_flow = CashFlow(
                        agent_profile_id=agent_profile_id,
                        user_id=user_id,
                        type="cash_in",
                        source=f"Transfer EDC - {service.name}",
                        amount=amount,
                        description=f"Transfer dari EDC. Transaction: {new_transaction.transaction_number}"
                    )
                    db.session.add(cash_flow)
                
            elif service.category and service.category.lower() == "tarik tunai":
                # Tarik tunai: uang tunai berkurang (jika ada agent), saldo EDC bertambah (cash_out)
                if agent:
                    agent.total_balance = float(agent.total_balance) - amount
                    db.session.add(agent)
                
                # Catat cash_out (uang keluar) — agent_profile_id boleh None
                cash_flow = CashFlow(
                    agent_profile_id=agent_profile_id if agent else None,
                    user_id=user_id,
                    type="cash_out",
                    source=f"Tarik Tunai - {service.name}",
                    amount=amount,
                    description=f"Tarik tunai. Transaction: {new_transaction.transaction_number}"
                )
                db.session.add(cash_flow)
                
                edc.saldo = float(edc.saldo) + amount
                db.session.add(edc)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return error_response(
                message='Terjadi kesalahan saat update saldo dan cash flow',
                error='INTERNAL_ERROR',
                details={'error': str(e)},
                status_code=500
            )
        
        transaction_data = new_transaction.to_dict()
        transaction_data['fee_calculation'] = fee_info
        
        return success_response(
            data=transaction_data,
            message='Transaction berhasil dibuat dengan fee otomatis',
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat membuat transaction',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )

@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
@token_required
def update_transaction(transaction_id):
    """Update transaction (read-only, cannot update after created)"""
    return error_response(
        message='Transaction tidak dapat diubah setelah dibuat',
        error='FORBIDDEN',
        status_code=403
    )

@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
@token_required
def delete_transaction(transaction_id):
    """Delete transaction"""
    try:
        user_id = request.user_id
        
        transaction = Transaction.query.get(transaction_id)
        
        if not transaction:
            return error_response(
                message='Transaction tidak ditemukan',
                error='NOT_FOUND',
                status_code=404
            )
        
        if not check_agent_ownership(user_id, transaction.agent_profile_id):
            return error_response(
                message='Anda tidak memiliki akses untuk menghapus transaction ini',
                error='FORBIDDEN',
                status_code=403
            )
        
        db.session.delete(transaction)
        db.session.commit()
        
        return success_response(
            data=None,
            message='Transaction berhasil dihapus',
            status_code=200
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(
            message='Terjadi kesalahan saat menghapus transaction',
            error='INTERNAL_ERROR',
            details={'error': str(e)},
            status_code=500
        )
