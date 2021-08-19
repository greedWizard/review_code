from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import TransferSerializer
from .models import Users


''' 
    Сразу в глаза бросается реализация логики во view.
    Логику лучше хронить в сервисах, чтобы можно было воспользоваться ей в любом месте (но только через сам сервис).
    Что делать если надо будет создать перевод где-то ещё? Копировать код из view? 
 '''


class TransferViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,) # разрешаем всем переводить деньги с любого счёта?
    serializer_class = TransferSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(True)

        amount = float(request.POST['amount']) # в последних версиях drf .POST уже не используется, да и зачем он, если 
                                                # все данные уже валидированы и лежат в serializer.data
        sum_part = 0

        user_from = User.objects.get(id=request.data['user_from']) # опять же, зачем через реквест?
                                            # да и при обращении к значениям словаря через ключи, лучше использовать .get()

        # ищем сумму на счёте пользователя
        us = user_from.users_set.all() # users_set это что? Вообще не понятно зачем это здесь, слишком много вопросов.
                                    # не ясна даже изначальная задумка.

        if us:
            acc_sum = us[0].account # user_from.balance.first(), если ForeignKey, user_from.balance если OneToOne

            inn_to = Users.objects.filter(inn=request.data['inn_to']) # такой запрос не сработает, надо inn__in=request.data['inn_to']
                                                    # это при условии, что inn_to было бы всё-таки Array полем...
            users_count = 0 # зачем инициализировать переменную здесь?

            if inn_to and acc_sum >= amount: # ужасное условие, которое не будет работать правильно 
                users_count = len(inn_to) # сразу же выдаст эксепшен int object has no len()
                sum_part = round(amount / users_count, 2)

                # со счёта донора списать всю сумму
                res_user = user_from.users_set.get() # что такое users_set, опять же. + пустое условие в get, выдаст ошибку

                # зачем приводить account к дроби, это ж и так дробь
                result_sum = float(res_user.account) - sum_part * users_count # не нужная операция, можно просто сразу
                                                        # вычесть amount
                res_user.account = result_sum
                res_user.save()

                # на счёт каждого записать по части
                for i in inn_to:
                    # если на счёт каждого записываем по частям, то и вычитать надо по частям
                    # если менеджер не найдёт инн в базе, то будет эксепшн, т.е. деньги не переведутся и выполнение остановится,
                    # но при этом вся изначальная сумма уже будет списана со счёта отправителя
                    result_sum = float(i.account) + sum_part # будет эксепшн int object has no attribute account
                                        # надо сделать так User.objects.filter(inn=i).first().account + sum_part
                    i.account = result_sum # куча ненужных переменных. можно просто сразу 
                                        # User.objects.filter(inn=i).first().account += sum_part
                    i.save() # опять ошибка, у int (если бы это был инт, как надо) нет метода .save()

                return Response(serializer.data)
            else:
                return Response('перевод не выполнен') # не совсем красивый ответ от сервера, 
                                    # надо вернуть что-то более правильное, например: 
                                    # { 'status': 'failed', 'info': 'Перевод не выполнен' }
        # условие выше никаким образом не проверяет баланс пользователя
        else:
            acc_sum = 0 # зачем? Ec
            return Response('На счёте недостаточно средств') # та же притензия к ответу, что и выше