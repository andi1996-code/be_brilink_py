from models.user import db
from datetime import datetime

class BankFee(db.Model):
    __tablename__ = 'bank_fees'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    edc_machine_id = db.Column(db.BigInteger, nullable=False)
    service_id = db.Column(db.BigInteger, nullable=False)
    fee = db.Column(db.Numeric(15, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'edc_machine_id': self.edc_machine_id,
            'service_id': self.service_id,
            'fee': float(self.fee) if self.fee else 0.00,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
