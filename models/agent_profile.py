from models.user import db
from datetime import datetime

class AgentProfile(db.Model):
    __tablename__ = 'agent_profiles'
    
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    owner_id = db.Column(db.BigInteger, nullable=True)
    agent_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(255), nullable=True)
    total_balance = db.Column(db.Numeric(15, 2), default=0.00)
    logo = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'owner_id': self.owner_id,
            'agent_name': self.agent_name,
            'address': self.address,
            'phone': self.phone,
            'total_balance': float(self.total_balance) if self.total_balance else 0.00,
            'logo': self.logo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
