from models.user import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    transaction_number = db.Column(db.String(255), unique=True, nullable=True)
    edc_machine_id = db.Column(db.BigInteger, nullable=False)
    service_id = db.Column(db.BigInteger, nullable=False)
    agent_profile_id = db.Column(db.BigInteger, nullable=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    cashier_name = db.Column(db.String(255), nullable=True)  # Nama kasir yang membuat transaksi
    customer_name = db.Column(db.String(255), nullable=True)
    target_number = db.Column(db.String(255), nullable=True)
    reference_number = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Numeric(15, 2), default=0.00)
    service_fee = db.Column(db.Numeric(15, 2), default=0.00)
    bank_fee = db.Column(db.Numeric(15, 2), default=0.00)
    extra_fee = db.Column(db.Numeric(15, 2), default=0.00)
    net_profit = db.Column(db.Numeric(15, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        amount = float(self.amount) if self.amount else 0.00
        service_fee = float(self.service_fee) if self.service_fee else 0.00
        bank_fee = float(self.bank_fee) if self.bank_fee else 0.00
        extra_fee = float(self.extra_fee) if self.extra_fee else 0.00
        total_received = amount + service_fee + bank_fee + extra_fee
        
        return {
            'id': self.id,
            'transaction_number': self.transaction_number,
            'edc_machine_id': self.edc_machine_id,
            'service_id': self.service_id,
            'agent_profile_id': self.agent_profile_id,
            'user_id': self.user_id,
            'cashier_name': self.cashier_name,
            'customer_name': self.customer_name,
            'target_number': self.target_number,
            'reference_number': self.reference_number,
            'amount': amount,
            'service_fee': service_fee,
            'bank_fee': bank_fee,
            'extra_fee': extra_fee,
            'total_received': total_received,
            'net_profit': float(self.net_profit) if self.net_profit else 0.00,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
