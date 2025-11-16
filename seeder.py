import os
import sys
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Add the current directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.user import db
from models.transaction import Transaction
from models.cash_flow import CashFlow
from models.service import Service
from models.edc_machine import EdcMachine
from models.agent_profile import AgentProfile
from models.user import User
from models.service_fee import ServiceFee
from models.bank_fee import BankFee
from models.service_fee import ServiceFee
from models.bank_fee import BankFee

def generate_transaction_number():
    """Generate unique transaction number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = str(random.randint(1000, 9999))
    return f"TXN{timestamp}{random_suffix}"

def get_random_date(start_date=None, end_date=None):
    """Get random date between start and end"""
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    time_diff = end_date - start_date
    random_days = random.randint(0, time_diff.days)
    random_date = start_date + timedelta(days=random_days)

    # Add random hours/minutes
    random_date = random_date.replace(
        hour=random.randint(8, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )

    return random_date

def get_service_fee(service_id, amount):
    """Get service fee based on amount ranges"""
    service_fee = ServiceFee.query.filter(
        ServiceFee.service_id == service_id,
        ServiceFee.min_amount <= amount,
        ServiceFee.max_amount >= amount
    ).first()

    return Decimal(str(service_fee.fee)) if service_fee else Decimal('0')

def get_bank_fee(edc_machine_id, service_id):
    """Get bank fee for specific EDC and service"""
    bank_fee = BankFee.query.filter(
        BankFee.edc_machine_id == edc_machine_id,
        BankFee.service_id == service_id
    ).first()

    return Decimal(str(bank_fee.fee)) if bank_fee else Decimal('0')

def seed_transactions(num_transactions=50):
    """Seed transactions with realistic data"""
    print(f"Seeding {num_transactions} transactions...")

    # Get existing data
    services = Service.query.all()
    edc_machines = EdcMachine.query.all()
    agents = AgentProfile.query.all()
    users = User.query.filter(User.role == 'kasir').all()

    if not services or not edc_machines or not agents or not users:
        print("Error: Missing required data. Please ensure services, EDC machines, agents, and users exist.")
        print(f"Services: {len(services)}, EDC: {len(edc_machines)}, Agents: {len(agents)}, Users: {len(users)}")
        return

    transactions_created = 0

    for i in range(num_transactions):
        # Select random entities
        service = random.choice(services)
        edc_machine = random.choice(edc_machines)
        agent = random.choice(agents)
        user = random.choice(users)

        # Generate realistic amount based on service
        if service.category and 'transfer' in service.category.lower():
            amount = Decimal(str(random.randint(50000, 2000000)))  # 50k - 2M for transfers
        elif service.category and 'pulsa' in service.category.lower():
            amount = Decimal(str(random.choice([25000, 50000, 100000, 150000, 200000])))
        elif service.category and 'pln' in service.category.lower():
            amount = Decimal(str(random.randint(20000, 2000000)))  # 20k - 2M for PLN
        else:
            amount = Decimal(str(random.randint(10000, 500000)))

        # Get fees from database
        service_fee = get_service_fee(service.id, amount)
        bank_fee = get_bank_fee(edc_machine.id, service.id)

        # Extra fee (optional - 30% chance)
        extra_fee = Decimal('0') if random.random() > 0.3 else Decimal(str(random.randint(1000, 5000)))

        # Calculate net profit (amount - extra_fee)
        net_profit = amount - extra_fee

        # Generate transaction data
        transaction = Transaction(
            transaction_number=generate_transaction_number(),
            edc_machine_id=edc_machine.id,
            service_id=service.id,
            agent_profile_id=agent.id,
            user_id=user.id,
            customer_name=random.choice([
                'Budi Santoso', 'Siti Aminah', 'Ahmad Rahman', 'Dewi Lestari',
                'Joko Widodo', 'Ani Suryani', 'Rudi Hartono', 'Maya Sari',
                'Dedi Kusuma', 'Rina Puspita', 'Agus Salim', 'Lina Marlina',
                'Hendra Gunawan', 'Sri Wahyuni', 'Toni Hartanto', 'Yuni Kristanti'
            ]),
            target_number=f"08{random.randint(1000000000, 9999999999)}" if service.requires_target else None,
            reference_number=f"REF{random.randint(100000, 999999)}",
            amount=amount,
            service_fee=service_fee,
            bank_fee=bank_fee,
            extra_fee=extra_fee,
            net_profit=net_profit,
            created_at=get_random_date()
        )

        db.session.add(transaction)
        transactions_created += 1

        # Print progress every 10 transactions
        if transactions_created % 10 == 0:
            print(f"Created {transactions_created} transactions...")

    db.session.commit()
    print(f"✅ Successfully seeded {transactions_created} transactions!")

def seed_today_transactions(num_transactions=20):
    """Seed transactions for today only (useful for dashboard testing)"""
    print(f"Seeding {num_transactions} transactions for today...")

    # Get existing data
    services = Service.query.all()
    edc_machines = EdcMachine.query.all()
    agents = AgentProfile.query.all()
    users = User.query.filter(User.role == 'kasir').all()

    if not services or not edc_machines or not agents or not users:
        print("Error: Missing required data. Please ensure services, EDC machines, agents, and users exist.")
        print(f"Services: {len(services)}, EDC: {len(edc_machines)}, Agents: {len(agents)}, Users: {len(users)}")
        return

    transactions_created = 0
    today = datetime.now()

    for i in range(num_transactions):
        # Select random entities
        service = random.choice(services)
        edc_machine = random.choice(edc_machines)
        agent = random.choice(agents)
        user = random.choice(users)

        # Generate realistic amount based on service
        if service.category and 'transfer' in service.category.lower():
            amount = Decimal(str(random.randint(50000, 2000000)))  # 50k - 2M for transfers
        elif service.category and 'pulsa' in service.category.lower():
            amount = Decimal(str(random.choice([25000, 50000, 100000, 150000, 200000])))
        elif service.category and 'pln' in service.category.lower():
            amount = Decimal(str(random.randint(20000, 2000000)))  # 20k - 2M for PLN
        else:
            amount = Decimal(str(random.randint(10000, 500000)))

        # Get fees from database
        service_fee = get_service_fee(service.id, amount)
        bank_fee = get_bank_fee(edc_machine.id, service.id)

        # Extra fee (optional - 30% chance)
        extra_fee = Decimal('0') if random.random() > 0.3 else Decimal(str(random.randint(1000, 5000)))

        # Calculate net profit (amount - extra_fee)
        net_profit = amount - extra_fee

        # Generate transaction data with TODAY's date
        # Random time between 08:00 and 22:00 today
        random_hour = random.randint(8, 22)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)

        created_at = today.replace(
            hour=random_hour,
            minute=random_minute,
            second=random_second
        )

        transaction = Transaction(
            transaction_number=generate_transaction_number(),
            edc_machine_id=edc_machine.id,
            service_id=service.id,
            agent_profile_id=agent.id,
            user_id=user.id,
            customer_name=random.choice([
                'Budi Santoso', 'Siti Aminah', 'Ahmad Rahman', 'Dewi Lestari',
                'Joko Widodo', 'Ani Suryani', 'Rudi Hartono', 'Maya Sari',
                'Dedi Kusuma', 'Rina Puspita', 'Agus Salim', 'Lina Marlina',
                'Hendra Gunawan', 'Sri Wahyuni', 'Toni Hartanto', 'Yuni Kristanti'
            ]),
            target_number=f"08{random.randint(1000000000, 9999999999)}" if service.requires_target else None,
            reference_number=f"REF{random.randint(100000, 999999)}",
            amount=amount,
            service_fee=service_fee,
            bank_fee=bank_fee,
            extra_fee=extra_fee,
            net_profit=net_profit,
            created_at=created_at
        )

        db.session.add(transaction)
        transactions_created += 1

        # Print progress every 5 transactions
        if transactions_created % 5 == 0:
            print(f"Created {transactions_created} transactions for today...")

    db.session.commit()
    print(f"✅ Successfully seeded {transactions_created} transactions for today!")

def seed_historical_cash_flows(num_entries=30):
    """Seed cash flow entries with realistic data (historical dates)"""
    print(f"Seeding {num_entries} historical cash flow entries...")

    # Get existing data
    agents = AgentProfile.query.all()
    users = User.query.all()

    if not agents or not users:
        print("Error: Missing required data. Please ensure agents and users exist.")
        return

    cash_flows_created = 0

    # Define cash flow sources with more variety
    cash_in_sources = [
        'Setoran Modal Pemilik',
        'Penjualan Pulsa',
        'Transfer Masuk',
        'Penarikan ATM',
        'Pembayaran Tagihan PLN',
        'Top Up Saldo',
        'Komisi Agen',
        'Bonus Sistem',
        'Penjualan Token Listrik',
        'Pembayaran BPJS',
        'Transfer Antar Bank',
        'Pembelian Voucher'
    ]

    cash_out_sources = [
        'Penarikan Pemilik',
        'Pembelian Pulsa Grosir',
        'Biaya Operasional',
        'Pembayaran Listrik',
        'Sewa Tempat',
        'Gaji Karyawan',
        'Pemeliharaan EDC',
        'Pembelian Bahan',
        'Pembayaran Internet',
        'Biaya Promosi',
        'Pembelian ATK',
        'Transportasi'
    ]

    for i in range(num_entries):
        # 60% cash_in, 40% cash_out
        is_cash_in = random.random() < 0.6
        flow_type = 'cash_in' if is_cash_in else 'cash_out'
        sources = cash_in_sources if is_cash_in else cash_out_sources

        # Select random entities
        agent = random.choice(agents)
        user = random.choice(users)

        # Generate realistic amount
        if is_cash_in:
            amount = Decimal(str(random.randint(50000, 2000000)))  # 50k - 2M for cash in
        else:
            amount = Decimal(str(random.randint(25000, 500000)))  # 25k - 500k for cash out

        # Generate cash flow data
        cash_flow = CashFlow(
            agent_profile_id=agent.id,
            user_id=user.id,
            type=flow_type,
            source=random.choice(sources),
            amount=amount,
            description=f"{'Pemasukan' if is_cash_in else 'Pengeluaran'} {random.choice(['rutin', 'tambahan', 'darurat', 'terjadwal', 'insidental'])} - {random.choice(['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'])} {random.randint(2024, 2025)}",
            created_at=get_random_date()
        )

        db.session.add(cash_flow)
        cash_flows_created += 1

        # Print progress every 5 entries
        if cash_flows_created % 5 == 0:
            print(f"Created {cash_flows_created} historical cash flow entries...")

    db.session.commit()
    print(f"✅ Successfully seeded {cash_flows_created} historical cash flow entries!")

def clear_existing_data():
    """Clear existing transaction and cash flow data"""
    print("🧹 Clearing existing transaction and cash flow data...")

    # Delete in correct order (due to foreign keys)
    Transaction.query.delete()
    CashFlow.query.delete()

    db.session.commit()
    print("✅ Existing data cleared!")

def show_stats():
    """Show current database statistics"""
    print("\n📊 Current Database Statistics:")
    print("-" * 40)

    transaction_count = Transaction.query.count()
    cash_flow_count = CashFlow.query.count()
    service_count = Service.query.count()
    edc_count = EdcMachine.query.count()
    agent_count = AgentProfile.query.count()
    user_count = User.query.count()

    print(f"Transactions: {transaction_count}")
    print(f"Cash Flows: {cash_flow_count}")
    print(f"Services: {service_count}")
    print(f"EDC Machines: {edc_count}")
    print(f"Agents: {agent_count}")
    print(f"Users: {user_count}")

    if transaction_count > 0:
        total_revenue = db.session.query(db.func.sum(Transaction.amount)).scalar() or 0
        print(f"Total Revenue: Rp {total_revenue:,.0f}")

    if cash_flow_count > 0:
        total_cash_in = db.session.query(db.func.sum(CashFlow.amount)).filter(CashFlow.type == 'cash_in').scalar() or 0
        total_cash_out = db.session.query(db.func.sum(CashFlow.amount)).filter(CashFlow.type == 'cash_out').scalar() or 0
        net_cash = total_cash_in - total_cash_out
        print(f"Total Cash In: Rp {total_cash_in:,.0f}")
        print(f"Total Cash Out: Rp {total_cash_out:,.0f}")
        print(f"Net Cash Flow: Rp {net_cash:,.0f}")

def main():
    """Main seeder function"""
    print("🌱 Brilink Database Seeder")
    print("=" * 50)

    # Parse command line arguments
    args = sys.argv[1:]

    # Create Flask app context
    app = create_app()

    with app.app_context():
        try:
            # Show current stats
            show_stats()

            # Check for command line arguments
            if args:
                if args[0] == '--clear-and-seed':
                    print("\n🚀 Clearing existing data and seeding new data...")
                    clear_existing_data()
                    seed_transactions(50)
                    seed_historical_cash_flows(30)
                elif args[0] == '--add-data':
                    print("\n➕ Adding additional data...")
                    seed_transactions(25)
                    seed_historical_cash_flows(15)
                elif args[0] == '--transactions':
                    num = int(args[1]) if len(args) > 1 and args[1].isdigit() else 50
                    print(f"\n💳 Seeding {num} transactions...")
                    seed_transactions(num)
                elif args[0] == '--cashflows':
                    num = int(args[1]) if len(args) > 1 and args[1].isdigit() else 30
                    print(f"\n💰 Seeding {num} historical cash flow entries...")
                    seed_historical_cash_flows(num)
                elif args[0] == '--today-transactions':
                    num = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10
                    print(f"\n📅 Seeding {num} transactions for today...")
                    seed_today_transactions(num)
                elif args[0] == '--stats':
                    return
                else:
                    print("❌ Invalid argument!")
                    print("Usage: python seeder.py [--clear-and-seed|--add-data|--transactions [num]|--cashflows [num]|--today-transactions [num]|--stats]")
                    return
            else:
                # Interactive mode
                print("\nOptions:")
                print("1. Clear existing data and seed new data")
                print("2. Seed additional data (keep existing)")
                print("3. Seed only transactions")
                print("4. Seed only cash flows")
                print("5. Seed today's transactions (for dashboard testing)")
                print("6. Show statistics only")

                choice = input("Choose option (1-6): ").strip()

                if choice == '1':
                    clear_existing_data()
                    seed_transactions(50)
                    seed_historical_cash_flows(30)
                elif choice == '2':
                    seed_transactions(25)
                    seed_historical_cash_flows(15)
                elif choice == '3':
                    num_txn = input("How many transactions to seed? (default: 50): ").strip()
                    num_txn = int(num_txn) if num_txn.isdigit() else 50
                    seed_transactions(num_txn)
                elif choice == '4':
                    num_cf = input("How many cash flow entries to seed? (default: 30): ").strip()
                    num_cf = int(num_cf) if num_cf.isdigit() else 30
                    seed_historical_cash_flows(num_cf)
                elif choice == '5':
                    num_today = input("How many today's transactions to seed? (default: 10): ").strip()
                    num_today = int(num_today) if num_today.isdigit() else 10
                    seed_today_transactions(num_today)
                elif choice == '6':
                    return
                else:
                    print("❌ Invalid choice!")
                    return

            print("=" * 50)
            print("🎉 Seeding completed successfully!")

            # Show updated stats
            show_stats()

            print("\n💡 Tips:")
            print("- Run this seeder multiple times to add more data")
            print("- Use option 2 to add data without clearing existing")
            print("- Check your dashboard and reports to see the seeded data")
            print("- Use option 5 to just view current statistics")

        except Exception as e:
            print(f"❌ Error during seeding: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    main()