from django.db import models

# Create your models here.

class Login1(models.Model):
    name = models.CharField(db_column='name', max_length=20, blank=False)
    account = models.CharField(primary_key=True ,db_column='account', max_length=20, blank=False)
    password = models.CharField(db_column='password', max_length=20, blank=False)
    sn1 = models.CharField(db_column='sn1', max_length=20, blank=True)
    sn2 = models.CharField(db_column='sn2', max_length=20, blank=True)
    sn3 = models.CharField(db_column='sn3', max_length=20, blank=True)
    certified = models.IntegerField(db_column='certified', max_length=3)
    money = models.IntegerField(db_column='money', max_length=10)
    bet = models.IntegerField(db_column='bet', max_length=10)
    totalMoney = models.IntegerField(db_column='totalMoney', max_length=10)
    totalIntro = models.IntegerField(db_column='totalIntro', max_length=10)
    totalPer = models.IntegerField(db_column='totalPer', max_length=3)
    introBet = models.IntegerField(db_column='introBet', max_length=10)
    authority = models.IntegerField(db_column='authority', max_length=3)



class User1(models.Model):
    date = models.DateTimeField(db_column='date',max_length=100)
    account = models.CharField(primary_key=True, db_column='account',max_length=20,blank=False)
    bet = models.IntegerField(db_column='bet',max_length=20)
    number = models.CharField(db_column='number',max_length=20)
    durationBet = models.IntegerField(db_column='durationBet',max_length=20)

