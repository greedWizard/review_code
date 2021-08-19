from django.contrib.auth.models import User
from django.db import models




class Users(models.Model):
    '''
        название класса слишком похоже на User. Кроме того, оно не отображает его сути.
        Оптимальное название было бы Balance или Account.  
    '''
    user =      models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Юзер') # скорее всегот это поле должно быть unique?
                    # точно ли здесь ForeignKey? Скорее больше подходит OneToOneField
                    # Не добавлено свойство related_name. (например)
                                                        # related_name='accounts'
    inn =       models.IntegerField(verbose_name='ИНН') # очень плохая идея хранить всё в integer, учитывая что в тз стоит, что 
                    # инн начинается с нуля. На самом деле дальше можно было бы даже не проверять :)
    account =   models.FloatField(verbose_name='Счёт') # для денег всегда используют Decimal
    # не совсем понятное название переменной, следовало бы назвать как-то вроде value или balance.

    def __str__(self):
        return '{id} {inn}'.format(id=str(self.id), inn=self.inn) # устаревший способ форматирования, сейчас всё делается через f-строки

''' 
По хорошему добавить ещё одну модель со всеми транзакциями, 
чтобы их можно было отследить. Добавить в них поля timestamp и inn_to и inn_from 
'''
