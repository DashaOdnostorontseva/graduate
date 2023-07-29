from django.db import models
from django.utils import timezone
from users.models import User

   
class documents(models.Model):
    name = models.CharField(max_length=128)
    number = models.CharField(max_length=128, null=True, blank=True)
    date_document = models.DateField(null=True, blank=True)
    date_send = models.DateTimeField(default=timezone.now)
    doc = models.FileField(upload_to='files/', null=True, blank=True)
    doc_sign = models.FileField(upload_to='files/', null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    
    inboxer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='inboxer', null=True, blank=True, default=None)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender', null=True, blank=True, default=None)
    
    recording_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Номер записи: {self.id} | Имя файла: {self.name} | Статус: {self.status} | Дата отправки: {self.date_send}'
    

class usersCerts(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    owner = models.CharField(max_length=512, null=True, blank=True)
    issuerName = models.CharField(max_length=512, null=True, blank=True)
    serialNumber = models.CharField(max_length=512, null=True, blank=True)
    validFromDate = models.CharField(max_length=512, null=True, blank=True)
    validToDate = models.CharField(max_length=512, null=True, blank=True)
    recording_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Номер записи: {self.id} | ID пользователя: {self.user} | Серийный номер: {self.serialNumber}'
    