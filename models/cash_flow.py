from models.user import db
from datetime import datetime

class CashFlow(db.Model):
    __tablename__ = 'cash_flows'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    agent_profile_id = db.Column(db.BigInteger, nullable=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # cash_in atau cash_out
    source = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(15, 2), default=0.00)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_profile_id': self.agent_profile_id,
            'user_id': self.user_id,
            'type': self.type,
            'source': self.source,
            'amount': float(self.amount) if self.amount else 0.00,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
