from models.user import db
from datetime import datetime

class ServiceFee(db.Model):
    __tablename__ = 'service_fees'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    service_id = db.Column(db.BigInteger, nullable=False)
    min_amount = db.Column(db.Numeric(15, 2), default=0.00)
    max_amount = db.Column(db.Numeric(15, 2), default=0.00)
    fee = db.Column(db.Numeric(15, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'min_amount': float(self.min_amount) if self.min_amount else 0.00,
            'max_amount': float(self.max_amount) if self.max_amount else 0.00,
            'fee': float(self.fee) if self.fee else 0.00,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
