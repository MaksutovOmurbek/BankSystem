from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.core.validators import RegexValidator 

phone_regex = RegexValidator(regex=r'^\+996\d{9}$', message="Номер телефона необходимо ввести в формате: '+996xxxxxxxxx'.")

class User(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex], max_length=15, verbose_name='Номер телефона')
    age = models.IntegerField(default=0, verbose_name='Возраст')
    wallet_address = models.CharField(max_length=12, unique=True, blank=True ,verbose_name='ID кошелька')
    balance = models.PositiveIntegerField(default = 0, verbose_name='Баланс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def save(self, *args, **kwargs):
        if not self.wallet_address:
            unique_address_generated = False
            while not unique_address_generated:
                wallet_address = get_random_string(length=12)
                if not User.objects.filter(wallet_address=wallet_address).exists():
                    unique_address_generated = True
            self.wallet_address = wallet_address
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
class HistoryTransfer(models.Model):
    from_user = models.ForeignKey(User, related_name='transfers_sent', on_delete=models.CASCADE, verbose_name='Отправющий')
    to_user = models.ForeignKey(User, related_name='transfers_received', on_delete=models.CASCADE, verbose_name='Получающий')
    is_completed = models.BooleanField(default=False, verbose_name='Статус перевода ')
    amount = models.PositiveIntegerField(verbose_name='Сумма', default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания ')


    def __str__(self):
        return f"{self.from_user} отправленo {self.to_user}"
    
    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'
    