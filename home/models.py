from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    image = models.ImageField(upload_to="profile/", 
        verbose_name="Фотография", help_text="Картинка должна быть Х на Х",
        blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона",unique=True)
    birth_date = models.DateField(verbose_name="Дата рождения",
        blank=True, null=True)
    about = models.TextField(max_length=200,
        verbose_name="Обо мне", blank=True, null=True)
    balance=models.PositiveIntegerField(default=0,verbose_name="Баланс")
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
        verbose_name="Пользователь")
    iin=models.CharField(max_length=12,verbose_name="ИНН",unique=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.first_name.title()} {self.user.last_name.title()[0]}"
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural="Профили"
        ordering=["created_at"]


class Transaction(models.Model):
    sender=models.ForeignKey(UserProfile, on_delete=models.PROTECT,related_name="send_transactions",verbose_name="Отправитель")
    recipient=models.ForeignKey(UserProfile,on_delete=models.PROTECT,related_name="recipient_transaction",verbose_name="Получатель")
    summa=models.PositiveIntegerField(verbose_name="сумма")
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.sender.balance < self.summa:
            raise Exception("Недостаточно средств на балансе отправителя")
        
        self.sender.balance -= self.summa
        self.recipient.balance += self.summa
        self.sender.save()
        self.recipient.save()
        super().save(*args, **kwargs)



    def __str__(self) -> str:
        return f"{self.sender_id} -> {self.recipient_id}"
    
    class Meta:
        verbose_name ="Транзакция"
        verbose_name_plural="Транзакции"
        ordering=["created_at"]

    
