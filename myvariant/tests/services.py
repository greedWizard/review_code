from decimal import Decimal
from django.test import TestCase
from myvariant.services import TransactionService
from myvariant.models import Account
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


# по хорошему здесь должны быть сервисы для каждой модели,
# но в целях упрощения будем использовать операции напрямую через менджера
class TransactionServiceTestCase(TestCase):
    service = TransactionService
    account_model = Account
    user_model = User

    def setUp(self) -> None:
        # аоздём пользователя для тестов и привязываем к нему аккаунт
        self.test_user = self.user_model.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='12345'
        )
        self.test_user.save()

        account = self.account_model.objects.create(
            user_id=self.test_user.id,
            inn='0000000000',
            balance=Decimal(100),
        )
        account.save()

        self.test_user2 = self.user_model.objects.create_user(
            username='testuser2',
            email='testuser2@test.com',
            password='12345'
        )
        self.test_user2.save()

        account = self.account_model.objects.create(
            user_id=self.test_user.id,
            inn='1111111111',
        )
        account.save()

        self.test_user3 = self.user_model.objects.create_user(
            username='testuser3',
            email='testuser3@test.com',
            password='12345'
        )
        self.test_user3.save()

        account = self.account_model.objects.create(
            user_id=self.test_user.id,
            inn='2222222222',
        )
        account.save()

        self.inn_list = [
            self.test_user2.account.inn,
            self.test_user3.account.inn,
        ]

    def test_transaction_success(self):
        self.service().transact(
            sender_id=self.test_user.id,
            inn_list=self.inn_list,
            amount=Decimal(100),
        )
        self.assertEqual(
            self.test_user2.account.balance, Decimal(50)
        )
        self.assertEqual(
            self.test_user3.account.balance, Decimal(50),
        )

    def test_transaction_not_enough_founds(self):
        try:
            self.service().transact(
                sender_id=self.test_user.id,
                inn_list=self.inn_list,
                amount=Decimal(100000)
            )
        except Exception as e:
            self.assertIsInstance(e, ValidationError)
    
    def test_transaction_user_not_found(self):
        try:
            self.service().transact(
                sender_id=12345,
                inn_list=self.inn_list,
                amount=Decimal(10)
            )
        except Exception as e:
            self.assertIsInstance(e, ValidationError)

    def test_sent_inn_not_found(self):
        inn_list = self.inn_list + ['1234123214124']
        try:
            self.service().transact(
                sender_id=12345,
                inn_list=inn_list,
                amount=Decimal(10)
            )
        except Exception as e:
            self.assertIsInstance(e, ValidationError)