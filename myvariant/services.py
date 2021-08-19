from typing import Iterable, List
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import Transaction, Account



class TransactionService:
    user_model = User
    transaction_model = Transaction
    account_model = Account

    def _validate_user_exists(self, sender_id: int) -> User:
        try:
            validated_user = self.user_model.objects.get(pk=sender_id)
            return validated_user
        except self.user_model.DoesNotExist:
            raise ValidationError(f'Неудалось найти пользователя')

    def _validate_balance(
        self,
        sender_id: int,
        amount: Decimal,
    ) -> None:
        validated_user = self.user_model.objects.filter(
            account__balance__gte=amount,
            id=sender_id,
        ).first()

        if not validated_user:
            raise ValidationError(f'Недостаточно средств на счёте')
      
    def get_account_by_inn(self, inn: str) -> Account:
        try:
            return self.account_model.objects.filter(inn=inn).first()
        except self.account_model.DoesNotExist:
            raise ValidationError(f'ИНН не найден {inn}')
    
    def transact(
        self,
        sender_id: int,
        inn_list: Iterable[int],
        amount: Decimal,
    ) -> List[Transaction]:
        ''' Отправить рубли на ИНН'ы '''
        sender = self._validate_user_exists(sender_id)
        self._validate_balance(sender_id, amount)

        partial_amount = Decimal(round(amount / len(inn_list), 2))
        transactions = []

        for inn in inn_list:
            receiver_acc = self.get_account_by_inn(inn)

            receiver_acc.balance += partial_amount
            receiver_acc.save()

            sender.account.balance -= partial_amount
            receiver_acc.save()

            new_transaction = self.transaction_model(
                sender_id=sender_id,
                receiver_id=receiver_acc.user.id,
            ).save()

            transactions.append(new_transaction)
        return transactions

