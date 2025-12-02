import pytest

from app import create_app
from models.user import db, User
from models.edc_machine import EdcMachine
from models.agent_profile import AgentProfile
from models.cash_flow import CashFlow
# no auth required for reset endpoint


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        # Ensure fresh schema
        db.drop_all()
        db.create_all()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def create_owner_user(app):
    with app.app_context():
        user = User(name='Owner Test', email='owner@test.local', password='pass', role='owner')
        db.session.add(user)
        db.session.commit()
        return user


def seed_data(app, owner):
    with app.app_context():
        # Create sample EDC machines
        edc1 = EdcMachine(agent_profile_id=None, name='EDC A', bank_name='BCA', saldo=150000.00)
        edc2 = EdcMachine(agent_profile_id=None, name='EDC B', bank_name='BRI', saldo=50000.00)
        db.session.add_all([edc1, edc2])

        # Create agent with total_balance
        agent = AgentProfile(user_id=owner.id, agent_name='Agent 1', total_balance=200000.00)
        db.session.add(agent)

        # Create some cash flows
        cf1 = CashFlow(agent_profile_id=agent.id, user_id=owner.id, type='cash_in', source='topup', amount=200000.00)
        cf2 = CashFlow(agent_profile_id=agent.id, user_id=owner.id, type='cash_out', source='withdraw', amount=50000.00)
        db.session.add_all([cf1, cf2])

        db.session.commit()


def test_reset_all_endpoint(client, app):
    # create owner and seed DB
    owner = create_owner_user(app)
    seed_data(app, owner)

    # Ensure preconditions
    with app.app_context():
        assert EdcMachine.query.count() == 2
        assert AgentProfile.query.count() == 1
        assert CashFlow.query.count() == 2

    # Call reset endpoint (no validation required)
    resp = client.post('/api/edc-machines/reset-all')
    assert resp.status_code == 200
    body = resp.get_json()
    assert body['success'] is True

    # Verify DB changes
    with app.app_context():
        # All edc saldo should be zero
        edcs = EdcMachine.query.all()
        for e in edcs:
            assert float(e.saldo) == 0.0

        # All agent total_balance should be zero
        agents = AgentProfile.query.all()
        for a in agents:
            assert float(a.total_balance) == 0.0

        # CashFlow entries deleted
        assert CashFlow.query.count() == 0
