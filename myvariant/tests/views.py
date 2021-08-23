from decimal import Decimal
from django.test import TestCase
from myvariant.services import TransactionService
from myvariant.models import Account
from django.contrib.auth.models import User
from rest_framework.test import APIClient


# по хорошему здесь должны быть сервисы для каждой модели,
# но в целях упрощения будем использовать операции напрямую через менджера
class TransactionViewTestCase(TestCase):
    service = TransactionService
    account_model = Account
    user_model = User
    client = APIClient()
    TRANSACTION_URL = 'api/v1/transactions/transact/'

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

    def test_transaction_view_success(self):
        response = self.client.post(
            self.TRANSACTION_URL,
            data={
                'sender_id': self.test_user.id,
                'inn_to': self.inn_list,
                'amount': 100,
            },
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(len(response_json), 2)

    def test_transaction_not_enough_founds(self):
        response = self.client.post(
            self.TRANSACTION_URL,
            data={
                'sender_id': self.test_user.id,
                'inn_to': self.inn_list,
                'amount': 1234512345,
            },
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
    
    def test_transaction_inn_not_found(self):
        response = self.client.post(
            self.TRANSACTION_URL,
            data={
                'sender_id': self.test_user.id,
                'inn_to': self.inn_list + ['1234123124'],
                'amount': 10,
            }
        )
        self.assertEqual(response.status_code, 400)

