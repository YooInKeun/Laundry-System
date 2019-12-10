from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from accounts.models import User


class Service(models.Model):
    SERVICE_CATEGORY_CHOICES = (
        ('수선', '수선'),
        ('세탁', '세탁'),
    )
    service = models.CharField(max_length=10, primary_key=True)
    category = models.CharField(max_length=2, choices=SERVICE_CATEGORY_CHOICES)


class Clothe(models.Model):
    CLOTHES_CATEGORY_CHOICES = (
        ('아우터', '아우터'),
        ('상의', '상의'),
        ('하의', '하의'),
        ('원피스', '원피스'),
        ('신발', '신발'),
    )

    clothe = models.CharField(max_length=10, primary_key=True)
    category = models.CharField(
        max_length=10, choices=CLOTHES_CATEGORY_CHOICES)


class Customer(models.Model):
    nickname = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    phone_num = models.CharField(max_length=11, null=False, primary_key=True)
    name = models.CharField(max_length=20)
    address = models.TextField()
    get_message = models.SmallIntegerField()
    created_date = models.DateTimeField(default=timezone.now)


class Request(models.Model):
    STATUS = (
        ('처리전', '처리 전'),
        ('처리중', '처리중'),
        ('처리완료', '처리 완료'),
        ('수거완료', '수거 완료'),
    )
    request_num = models.CharField(max_length=20, primary_key=True)
    phone_num = models.ForeignKey('Customer', on_delete=models.CASCADE)
    clothe = models.ForeignKey('Clothe', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS)
    rqst_date = models.DateTimeField(default=timezone.now)
    est_date = models.DateTimeField(null=True)
    fin_date = models.DateTimeField(null=True)
    rtrn_date = models.DateTimeField(null=True)
    requirements = models.TextField(null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.request_num

    def getList(self):
        row = []
        row.append(self.request_num)
        row.append(self.phone_num.phone_num)
        row.append(self.clothe.clothe)
        row.append(self.service.service)
        row.append(self.status)
        row.append(str(self.rqst_date))
        row.append(str(self.est_date))
        row.append(str(self.fin_date))
        row.append(str(self.rtrn_date))
        row.append(self.requiremnets)
        row.append(str(self.price))
        return row
