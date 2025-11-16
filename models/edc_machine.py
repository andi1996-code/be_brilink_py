from models.user import db
from datetime import datetime

class EdcMachine(db.Model):
    __tablename__ = 'edc_machines'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    agent_profile_id = db.Column(db.BigInteger, nullable=True)
    name = db.Column(db.String(255), nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), nullable=True)
    saldo = db.Column(db.Numeric(15, 2), default=0.00)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_profile_id': self.agent_profile_id,
            'name': self.name,
            'bank_name': self.bank_name,
            'account_number': self.account_number,
            'saldo': float(self.saldo) if self.saldo else 0.00,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
