import os
from flask import Flask, jsonify
from config import config
from models.user import db

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from routes.health import health_bp
    from routes.auth import auth_bp
    from routes.agent import agent_bp
    from routes.edc import edc_bp
    from routes.service import service_bp
    from routes.service_fee import service_fee_bp
    from routes.bank_fee import bank_fee_bp
    from routes.transaction import transaction_bp
    from routes.cash_flow import cash_flow_bp
    from routes.dashboard import dashboard_bp
    from routes.reports import reports_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(edc_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(service_fee_bp)
    app.register_blueprint(bank_fee_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(cash_flow_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': 'NOT_FOUND'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': 'INTERNAL_ERROR'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
