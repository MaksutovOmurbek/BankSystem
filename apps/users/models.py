from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator 
from django.contrib.auth import get_user_model
import random

phone_regex = RegexValidator(regex=r'^\+996\d{9}$', message="Номер телефона необходимо ввести в формате: '+996xxxxxxxxx'.")

class User(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex], max_length=15, verbose_name='Номер телефона')
    age = models.IntegerField(default=0, verbose_name='Возраст')
    wallet_address = models.CharField(max_length=12,blank=True ,verbose_name='ID кошелька')
    balance = models.PositiveIntegerField(default=0, verbose_name='Баланс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан в')
    confirm_password = models.CharField(max_length=50, verbose_name='Подтверждения пароля')
    
    def save(self, *args, **kwargs):
        if not self.wallet_address:
            unique_wallet_address = False
            wallet_address = ''
            while not unique_wallet_address:
                for i in range(12):
                    wallet_id = random.randrange(0,10)
                    wallet_address += str(wallet_id)
                if not User.objects.filter(wallet_address=wallet_address).exists():
                    unique_wallet_address = True
            self.wallet_address = wallet_address
        super().save(*args, **kwargs)
	
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

FromUser = get_user_model()

class HistoryTransfer(models.Model):
    from_user = models.ForeignKey(FromUser, related_name='transfers_sent', on_delete=models.CASCADE,verbose_name='Отправитель' )
    to_user = models.ForeignKey(User, related_name='transfers_received', on_delete=models.CASCADE, verbose_name='Получатель')
    is_completed = models.BooleanField(default=False, verbose_name='Сделано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан в')
    amount = models.PositiveIntegerField(default=0, verbose_name='Сумма')
    
    def save(self, *args, **kwargs):            
        if self.is_completed:
            raise ValueError("Транзакция прошла не успешна")

        
        if not self.is_completed:
            from_user_balance = self.from_user.balance
            to_user_wallet = self.to_user.balance

        if from_user_balance < self.amount:
            raise ValueError("Недостаточно средств на вашем балансе")
        
        if self.from_user == self.to_user:
            raise ValueError("Нельзя отправить средства самому себе")

        self.from_user.balance -= self.amount
        self.to_user.balance += self.amount

        self.is_completed = True

        self.from_user.save()
        self.to_user.save()
        super(HistoryTransfer, self).save(*args, **kwargs)



    def __str__(self):
        return f'{self.to_user} | Получено:{self.to_user}'
    
    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'
    