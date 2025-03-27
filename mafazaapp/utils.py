from .models import AssignedProject, Transaction, UserLedger
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils.timezone import now
from datetime import timedelta

from django.utils import timezone
from datetime import timedelta




from django.core.exceptions import ValidationError
from django.utils.timezone import now
from decimal import Decimal
from datetime import timedelta

# def create_transaction(user, project, amount, transaction_type, receipt, narration):
#     print(f"Transaction Debug - Type: {transaction_type}, Amount: {amount}, Project: {project.project_name}")

#     # Get LAST ledger entry FOR THIS SPECIFIC PROJECT
#     last_ledger = UserLedger.objects.filter(
#         transaction__user=user,
#         project_name=project.project_name
#     ).order_by('-date').first()
    
#     current_balance = last_ledger.balance if last_ledger else Decimal('0.00')
#     print(f"DEBUG: Current balance for project {project.project_name}: {current_balance}")

#     # Withdrawal logic
#     if transaction_type == 'withdrawal':
#         print("\nDEBUG: Processing WITHDRAWAL")
        
#         if not last_ledger or current_balance < amount:
#             error_msg = f"Insufficient balance in project {project.project_name} for withdrawal. Current balance: {current_balance}"
#             print(f"DEBUG: {error_msg}")
#             raise ValidationError(error_msg)

#         new_balance = current_balance - amount
#         print(f"DEBUG: New balance will be: {new_balance}")

#         transaction = Transaction.objects.create(
#             user=user,
#             project=project,
#             amount=amount,
#             transaction_type='withdrawal',
#             receipt=receipt,  
#             narration=narration,
#         )

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=project.project_name,
#             principal_investment=Decimal('0.00'),
#             returns=Decimal('0.00'),
#             withdrawal=amount,
#             balance=new_balance,
#             receipt=receipt,
#             narration=narration
#         )

#         print(f"Withdrawal processed. New Balance for {project.project_name}: {new_balance}")
#         return transaction

#     # Investment logic
#     elif transaction_type == 'investment':
#         print("\nDEBUG: Processing INVESTMENT")
        
#         assigned_project = AssignedProject.objects.get(
#             user=user,
#             project=project
#         )
#         roi = assigned_project.rate_of_interest / Decimal('100')
#         annual_return = amount * roi
#         interval_return = (annual_return / Decimal('525600')) * Decimal('2')

#         new_balance = current_balance + interval_return
        
#         print(f"DEBUG: Project ROI: {assigned_project.rate_of_interest}%")
#         print(f"DEBUG: 2-minute return: {interval_return}")
#         print(f"DEBUG: New balance will be: {new_balance}")

#         transaction = Transaction.objects.create(
#             user=user,
#             project=project,
#             amount=amount,
#             transaction_type='investment',
#             status='pending',
#             receipt=receipt,
#             narration=narration,
#         )

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=project.project_name,
#             principal_investment=amount,
#             returns=interval_return,
#             withdrawal=Decimal('0.00'),
#             balance=new_balance,
#             receipt=receipt,
#             narration=narration
#         )

#         print(f"Investment processed. New Balance for {project.project_name}: {new_balance}")
#         return transaction

# def update_user_ledger(transaction):
#     # Get the last balance from the ledger FOR THIS SPECIFIC PROJECT
#     last_ledger = UserLedger.objects.filter(
#         transaction__user=transaction.user,
#         project_name=transaction.project.project_name
#     ).order_by('-date').first()
    
#     last_balance = last_ledger.balance if last_ledger else Decimal('0.00')
#     print(f"DEBUG: Updating ledger for project {transaction.project.project_name}. Last balance: {last_balance}")

#     if transaction.transaction_type == 'investment':
#         try:
#             assigned_project = AssignedProject.objects.get(
#                 user=transaction.user,
#                 project=transaction.project
#             )
#             roi = assigned_project.rate_of_interest / Decimal('100')
#             annual_return = transaction.amount * roi
#             interval_return = (annual_return / Decimal('525600')) * Decimal('2')

#             new_balance = last_balance + interval_return
#             print(f"DEBUG: Adding {interval_return} to project {transaction.project.project_name}. New balance: {new_balance}")

#             UserLedger.objects.create(
#                 transaction=transaction,
#                 date=now(),
#                 project_name=transaction.project.project_name,
#                 principal_investment=transaction.amount,
#                 returns=interval_return,
#                 withdrawal=Decimal('0.00'),
#                 balance=new_balance,
#             )

#         except AssignedProject.DoesNotExist:
#             raise ValidationError(f"No project assignment found for {transaction.user} in {transaction.project}")

#     elif transaction.transaction_type == 'withdrawal':
#         if last_balance < transaction.amount:
#             raise ValidationError(
#                 f"Insufficient balance in project {transaction.project.project_name}. "
#                 f"Available: {last_balance}, Attempted withdrawal: {transaction.amount}"
#             )
        
#         new_balance = last_balance - transaction.amount
#         print(f"DEBUG: Deducting {transaction.amount} from project {transaction.project.project_name}. New balance: {new_balance}")

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=transaction.project.project_name,
#             principal_investment=Decimal('0.00'),
#             returns=Decimal('0.00'),
#             withdrawal=transaction.amount,
#             balance=new_balance,
#         )


# def generate_missed_returns():
#     transactions = Transaction.objects.filter(transaction_type='investment', status='approved')

#     for transaction in transactions:
#         try:
#             assigned_project = AssignedProject.objects.get(
#                 user=transaction.user,
#                 project=transaction.project
#             )
#         except AssignedProject.DoesNotExist:
#             continue

#         if assigned_project.return_period != '2m':
#             continue

#         last_ledger = UserLedger.objects.filter(
#             transaction__user=transaction.user,
#             project_name=transaction.project.project_name
#         ).order_by('-date').first()
        
#         current_time = now()

#         # ✅ Find the last return entry (ignore withdrawals)
#         last_return_entry = UserLedger.objects.filter(
#             transaction__user=transaction.user,
#             project_name=transaction.project.project_name,
#             returns__gt=Decimal('0.00')  # Only consider return entries
#         ).order_by('-date').first()

#         if last_return_entry:
#             correct_next_time = (last_return_entry.date + timedelta(minutes=2)).replace(second=0)
#         else:
#             correct_next_time = (last_ledger.date + timedelta(minutes=2)).replace(second=0)

#         while correct_next_time <= current_time:
#             roi = assigned_project.rate_of_interest / Decimal('100')
#             annual_return = transaction.amount * roi
#             interval_return = (annual_return / Decimal('525600')) * Decimal('2')

#             last_balance = UserLedger.objects.filter(
#                 transaction__user=transaction.user,
#                 project_name=transaction.project.project_name
#             ).order_by('-date').first().balance

#             new_balance = last_balance + interval_return

#             last_ledger = UserLedger.objects.create(
#                 transaction=transaction,
#                 date=correct_next_time,  # ✅ Ensures correct timing even after withdrawal
#                 project_name=transaction.project.project_name,
#                 principal_investment=Decimal('0.00'),
#                 returns=interval_return,
#                 withdrawal=Decimal('0.00'),
#                 balance=new_balance,
#                 receipt=transaction.receipt
#             )
#             print(f"DEBUG: Added return at {correct_next_time} for {transaction.project.project_name}. New balance: {new_balance}")

#             correct_next_time += timedelta(minutes=2) 





#firstone
#firstone
#firstone
#firstone
#firstone
#firstone

# def update_user_ledger(transaction):
#     # Get the last balance from the ledger FOR THIS SPECIFIC PROJECT
#     last_ledger = UserLedger.objects.filter(
#         transaction__user=transaction.user,
#         project_name=transaction.project.project_name
#     ).order_by('-date').first()
    
#     last_balance = last_ledger.balance if last_ledger else Decimal('0.00')
#     print(f"DEBUG: Updating ledger for project {transaction.project.project_name}. Last balance: {last_balance}")

#     if transaction.transaction_type == 'investment':
#         try:
#             assigned_project = AssignedProject.objects.get(
#                 user=transaction.user,
#                 project=transaction.project
#             )
#             roi = assigned_project.rate_of_interest / Decimal('100')
#             annual_return = transaction.amount * roi
#             interval_return = (annual_return / Decimal('525600')) * Decimal('2')

#             new_balance = last_balance + interval_return
#             print(f"DEBUG: Adding {interval_return} to project {transaction.project.project_name}. New balance: {new_balance}")

#             UserLedger.objects.create(
#                 transaction=transaction,
#                 date=now(),
#                 project_name=transaction.project.project_name,
#                 principal_investment=transaction.amount,
#                 returns=interval_return,
#                 withdrawal=Decimal('0.00'),
#                 balance=new_balance,
#             )

#         except AssignedProject.DoesNotExist:
#             raise ValidationError(f"No project assignment found for {transaction.user} in {transaction.project}")

#     elif transaction.transaction_type == 'withdrawal':
#         if last_balance < transaction.amount:
#             raise ValidationError(
#                 f"Insufficient balance in project {transaction.project.project_name}. "
#                 f"Available: {last_balance}, Attempted withdrawal: {transaction.amount}"
#             )
        
#         new_balance = last_balance - transaction.amount
#         print(f"DEBUG: Deducting {transaction.amount} from project {transaction.project.project_name}. New balance: {new_balance}")

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=transaction.project.project_name,
#             principal_investment=Decimal('0.00'),
#             returns=Decimal('0.00'),
#             withdrawal=transaction.amount,
#             balance=new_balance,
#         )
        
        
# from dateutil.relativedelta import relativedelta       
# def create_transaction(user, project, amount, transaction_type, receipt, narration):
#     print(f"Transaction Debug - Type: {transaction_type}, Amount: {amount}, Project: {project.project_name}")

#     # Get LAST ledger entry FOR THIS SPECIFIC PROJECT
#     last_ledger = UserLedger.objects.filter(
#         transaction__user=user,
#         project_name=project.project_name
#     ).order_by('-date').first()
    
#     current_balance = last_ledger.balance if last_ledger else Decimal('0.00')
#     print(f"DEBUG: Current balance for project {project.project_name}: {current_balance}")

#     # Withdrawal logic
#     if transaction_type == 'withdrawal':
#         print("\nDEBUG: Processing WITHDRAWAL")
        
#         if not last_ledger or current_balance < amount:
#             error_msg = f"Insufficient balance in project {project.project_name} for withdrawal. Current balance: {current_balance}"
#             print(f"DEBUG: {error_msg}")
#             raise ValidationError(error_msg)

#         new_balance = current_balance - amount
#         print(f"DEBUG: New balance will be: {new_balance}")

#         transaction = Transaction.objects.create(
#             user=user,
#             project=project,
#             amount=amount,
#             transaction_type='withdrawal',
#             receipt=receipt,  
#             narration=narration,
#         )

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=project.project_name,
#             principal_investment=Decimal('0.00'),
#             returns=Decimal('0.00'),
#             withdrawal=amount,
#             balance=new_balance,
#             receipt=receipt,
#             narration=narration
#         )

#         print(f"Withdrawal processed. New Balance for {project.project_name}: {new_balance}")
#         return transaction

#     # Investment logic
#     elif transaction_type == 'investment':
#         print("\nDEBUG: Processing INVESTMENT")
        
#         assigned_project = AssignedProject.objects.get(
#             user=user,
#             project=project
#         )
#         roi = assigned_project.rate_of_interest / Decimal('100')
#         annual_return = amount * roi
        
#         # Calculate interval return based on return period
#         if assigned_project.return_period == '2m':
#             interval_return = (annual_return / Decimal('525600')) * Decimal('2')  # 2 minutes
#         elif assigned_project.return_period == '10m':
#             interval_return = (annual_return / Decimal('52560')) * Decimal('10')  # 10 minutes
#         elif assigned_project.return_period == 'monthly':
#             interval_return = annual_return / Decimal('12')  # Monthly
#         elif assigned_project.return_period == 'quarterly':
#             interval_return = annual_return / Decimal('4')  # Quarterly
#         elif assigned_project.return_period == 'semiannual':
#             interval_return = annual_return / Decimal('2')  # Semiannual
#         elif assigned_project.return_period == 'annual':
#             interval_return = annual_return  # Annual
#         else:
#             interval_return = Decimal('0.00')

#         new_balance = current_balance + interval_return
        
#         print(f"DEBUG: Project ROI: {assigned_project.rate_of_interest}%")
#         print(f"DEBUG: {assigned_project.return_period} return: {interval_return}")
#         print(f"DEBUG: New balance will be: {new_balance}")

#         transaction = Transaction.objects.create(
#             user=user,
#             project=project,
#             amount=amount,
#             transaction_type='investment',
#             status='pending',
#             receipt=receipt,
#             narration=narration,
#         )

#         UserLedger.objects.create(
#             transaction=transaction,
#             date=now(),
#             project_name=project.project_name,
#             principal_investment=amount,
#             returns=interval_return,
#             withdrawal=Decimal('0.00'),
#             balance=new_balance,
#             receipt=receipt,
#             narration=narration
#         )

#         print(f"Investment processed. New Balance for {project.project_name}: {new_balance}")
#         return transaction

# def generate_missed_returns():
#     transactions = Transaction.objects.filter(transaction_type='investment', status='approved')

#     for transaction in transactions:
#         try:
#             assigned_project = AssignedProject.objects.get(
#                 user=transaction.user,
#                 project=transaction.project
#             )
#         except AssignedProject.DoesNotExist:
#             continue

#         last_ledger = UserLedger.objects.filter(
#             transaction__user=transaction.user,
#             project_name=transaction.project.project_name
#         ).order_by('-date').first()
        
#         current_time = now()

#         # Find the last return entry (ignore withdrawals)
#         last_return_entry = UserLedger.objects.filter(
#             transaction__user=transaction.user,
#             project_name=transaction.project.project_name,
#             returns__gt=Decimal('0.00')  # Only consider return entries
#         ).order_by('-date').first()

#         if last_return_entry:
#             if assigned_project.return_period == '2m':
#                 correct_next_time = (last_return_entry.date + timedelta(minutes=2)).replace(second=0)
#             elif assigned_project.return_period == '10m':
#                 correct_next_time = (last_return_entry.date + timedelta(minutes=10)).replace(second=0)
#             elif assigned_project.return_period == 'monthly':
#                 correct_next_time = (last_return_entry.date + relativedelta(months=1)).replace(day=1)
#             elif assigned_project.return_period == 'quarterly':
#                 correct_next_time = (last_return_entry.date + relativedelta(months=3)).replace(day=1)
#             elif assigned_project.return_period == 'semiannual':
#                 correct_next_time = (last_return_entry.date + relativedelta(months=6)).replace(day=1)
#             elif assigned_project.return_period == 'annual':
#                 correct_next_time = (last_return_entry.date + relativedelta(years=1)).replace(month=1, day=1)
#         else:
#             if assigned_project.return_period == '2m':
#                 correct_next_time = (last_ledger.date + timedelta(minutes=2)).replace(second=0)
#             elif assigned_project.return_period == '10m':
#                 correct_next_time = (last_ledger.date + timedelta(minutes=10)).replace(second=0)
#             elif assigned_project.return_period == 'monthly':
#                 correct_next_time = (last_ledger.date + relativedelta(months=1)).replace(day=1)
#             elif assigned_project.return_period == 'quarterly':
#                 correct_next_time = (last_ledger.date + relativedelta(months=3)).replace(day=1)
#             elif assigned_project.return_period == 'semiannual':
#                 correct_next_time = (last_ledger.date + relativedelta(months=6)).replace(day=1)
#             elif assigned_project.return_period == 'annual':
#                 correct_next_time = (last_ledger.date + relativedelta(years=1)).replace(month=1, day=1)

#         while correct_next_time <= current_time:
#             roi = assigned_project.rate_of_interest / Decimal('100')
#             annual_return = transaction.amount * roi
            
#             # Calculate interval return based on return period
#             if assigned_project.return_period == '2m':
#                 interval_return = (annual_return / Decimal('525600')) * Decimal('2')
#             elif assigned_project.return_period == '10m':
#                 interval_return = (annual_return / Decimal('52560')) * Decimal('10')
#             elif assigned_project.return_period == 'monthly':
#                 interval_return = annual_return / Decimal('12')
#             elif assigned_project.return_period == 'quarterly':
#                 interval_return = annual_return / Decimal('4')
#             elif assigned_project.return_period == 'semiannual':
#                 interval_return = annual_return / Decimal('2')
#             elif assigned_project.return_period == 'annual':
#                 interval_return = annual_return
#             else:
#                 interval_return = Decimal('0.00')

#             last_balance = UserLedger.objects.filter(
#                 transaction__user=transaction.user,
#                 project_name=transaction.project.project_name
#             ).order_by('-date').first().balance

#             new_balance = last_balance + interval_return

#             last_ledger = UserLedger.objects.create(
#                 transaction=transaction,
#                 date=correct_next_time,
#                 project_name=transaction.project.project_name,
#                 principal_investment=Decimal('0.00'),
#                 returns=interval_return,
#                 withdrawal=Decimal('0.00'),
#                 balance=new_balance,
#                 receipt=transaction.receipt
#             )
#             print(f"DEBUG: Added return at {correct_next_time} for {transaction.project.project_name}. New balance: {new_balance}")

#             # Calculate next return time based on return period
#             if assigned_project.return_period == '2m':
#                 correct_next_time += timedelta(minutes=2)
#             elif assigned_project.return_period == '10m':
#                 correct_next_time += timedelta(minutes=10)
#             elif assigned_project.return_period == 'monthly':
#                 correct_next_time += relativedelta(months=1)
#             elif assigned_project.return_period == 'quarterly':
#                 correct_next_time += relativedelta(months=3)
#             elif assigned_project.return_period == 'semiannual':
#                 correct_next_time += relativedelta(months=6)
#             elif assigned_project.return_period == 'annual':
#                 correct_next_time += relativedelta(years=1)        



# sorteddd
# divmoddd
# ddd
# divmodd
# divmodd

from decimal import Decimal
from datetime import timedelta
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from .models import UserLedger, Transaction, AssignedProject



def create_transaction(user, project, amount, transaction_type, receipt, narration):
    """Creates an investment or withdrawal transaction and updates the ledger."""
    print(f"Transaction Debug - Type: {transaction_type}, Amount: {amount}, Project: {project.project_name}")

    last_ledger = UserLedger.objects.filter(
        transaction__user=user,
        project_name=project.project_name
    ).order_by('-date').first()
    
    current_balance = last_ledger.balance if last_ledger else Decimal('0.00')
    print(f"DEBUG: Current balance for project {project.project_name}: {current_balance}")

    if transaction_type == 'withdrawal':
        print("\nDEBUG: Processing WITHDRAWAL")
        
        if not last_ledger or current_balance < amount:
            error_msg = f"Insufficient balance in project {project.project_name} for withdrawal. Current balance: {current_balance}"
            print(f"DEBUG: {error_msg}")
            raise ValidationError(error_msg)

        new_balance = current_balance - amount
        print(f"DEBUG: New balance will be: {new_balance}")

        transaction = Transaction.objects.create(
            user=user,
            project=project,
            amount=amount,
            transaction_type='withdrawal',
            receipt=receipt,  
            narration=narration,
        )

        UserLedger.objects.create(
            transaction=transaction,
            date=now(),
            project_name=project.project_name,
            principal_investment=Decimal('0.00'),
            returns=Decimal('0.00'),
            withdrawal=amount,
            balance=new_balance,
            receipt=receipt,
            narration=narration
        )

        print(f"Withdrawal processed. New Balance for {project.project_name}: {new_balance}")
        return transaction

    elif transaction_type == 'investment':
        print("\nDEBUG: Processing INVESTMENT")

        assigned_project = AssignedProject.objects.get(
            user=user,
            project=project
        )

        transaction = Transaction.objects.create(
            user=user,
            project=project,
            amount=amount,
            transaction_type='investment',
            status='pending',
            receipt=receipt,
            narration=narration,
        )

        # No immediate return, only principal investment recorded
        UserLedger.objects.create(
            transaction=transaction,
            date=now(),
            project_name=project.project_name,
            principal_investment=amount,
            returns=Decimal('0.00'),  # No immediate return
            withdrawal=Decimal('0.00'),
            balance=current_balance,  # Balance remains unchanged initially
            receipt=receipt,
            narration=narration
        )

        print(f"Investment processed. Return will be added in the next interval for {project.project_name}.")
        return transaction


from decimal import Decimal
from django.utils.timezone import now
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

# Define return periods dynamically
RETURN_PERIODS = {
    '2m':  Decimal('525600') / Decimal('2'),   # 2-minute intervals in a year
    '10m': Decimal('525600') / Decimal('10'),  # 10-minute intervals in a year
    'monthly': Decimal('12'),                  # 12 months in a year
    'quarterly': Decimal('4'),                 # 4 quarters in a year
    'semiannual': Decimal('2'),                # 2 halves in a year
    'annual': Decimal('1')                     # 1 return per year
}

def update_user_ledger(transaction):
    """Updates the user's ledger when an investment or withdrawal is made."""
    last_ledger = UserLedger.objects.filter(
        transaction__user=transaction.user,
        project_name=transaction.project.project_name
    ).order_by('-date').first()
    
    last_balance = last_ledger.balance if last_ledger else Decimal('0.00')
    print(f"DEBUG: Updating ledger for {transaction.project.project_name}. Last balance: {last_balance}")
    
    if transaction.transaction_type == 'investment':
        try:
            assigned_project = AssignedProject.objects.get(
                user=transaction.user,
                project=transaction.project
            )
            
            new_balance = last_balance  # Keep balance unchanged initially
            UserLedger.objects.create(
                transaction=transaction,
                date=now(),
                project_name=transaction.project.project_name,
                principal_investment=transaction.amount,
                returns=Decimal('0.00'),
                withdrawal=Decimal('0.00'),
                balance=new_balance,
            )
        except AssignedProject.DoesNotExist:
            raise ValidationError(f"No project assignment found for {transaction.user} in {transaction.project}")

    elif transaction.transaction_type == 'withdrawal':
        if last_balance < transaction.amount:
            raise ValidationError("Insufficient balance for withdrawal.")
        
        new_balance = last_balance - transaction.amount
        UserLedger.objects.create(
            transaction=transaction,
            date=now(),
            project_name=transaction.project.project_name,
            principal_investment=Decimal('0.00'),
            returns=Decimal('0.00'),
            withdrawal=transaction.amount,
            balance=new_balance,
        )

def generate_missed_returns():
    """Generates missed returns based on the scheduled return intervals."""
    transactions = Transaction.objects.filter(transaction_type='investment', status='approved')
    
    for transaction in transactions:
        try:
            assigned_project = AssignedProject.objects.get(
                user=transaction.user,
                project=transaction.project
            )
        except AssignedProject.DoesNotExist:
            continue
        
        last_ledger = UserLedger.objects.filter(
            transaction__user=transaction.user,
            project_name=transaction.project.project_name
        ).order_by('-date').first()
        
        current_time = now()
        last_return_entry = UserLedger.objects.filter(
            transaction__user=transaction.user,
            project_name=transaction.project.project_name,
            returns__gt=Decimal('0.00')
        ).order_by('-date').first()

        correct_next_time = last_return_entry.date if last_return_entry else last_ledger.date
        
        return_periods = {
            '2m': timedelta(minutes=2),
            '10m': timedelta(minutes=10),
            'monthly': relativedelta(months=1),
            'quarterly': relativedelta(months=3),
            'semiannual': relativedelta(months=6),
            'annual': relativedelta(years=1),
        }
        
        if assigned_project.return_period in return_periods:
            correct_next_time += return_periods[assigned_project.return_period]
        
        while correct_next_time <= current_time:
            roi = assigned_project.rate_of_interest / Decimal('100')
            annual_return = transaction.amount * roi
            interval_return = annual_return / RETURN_PERIODS.get(assigned_project.return_period, Decimal('1'))
            
            last_balance = UserLedger.objects.filter(
                transaction__user=transaction.user,
                project_name=transaction.project.project_name
            ).order_by('-date').first().balance
            
            new_balance = last_balance + interval_return
            UserLedger.objects.create(
                transaction=transaction,
                date=correct_next_time,
                project_name=transaction.project.project_name,
                principal_investment=Decimal('0.00'),
                returns=interval_return,
                withdrawal=Decimal('0.00'),
                balance=new_balance,
                receipt=transaction.receipt
            )
            print(f"DEBUG: Added return at {correct_next_time} for {transaction.project.project_name}. New balance: {new_balance}")
            correct_next_time += return_periods[assigned_project.return_period]
