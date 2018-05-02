from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Login1(models.Model):
    name = models.CharField(db_column='name', max_length=20, blank=False)
    account = models.CharField(primary_key=True ,db_column='account', max_length=20, blank=False)
    password = models.CharField(db_column='password', max_length=20, blank=False)
    sn1 = models.CharField(db_column='sn1', max_length=20, blank=True)
    sn2 = models.CharField(db_column='sn2', max_length=20, blank=True)
    sn3 = models.CharField(db_column='sn3', max_length=20, blank=True)
    certified = models.CharField(db_column='certified', max_length=20)
    money = models.IntegerField(db_column='money')
    bet = models.IntegerField(db_column='bet')
    totalMoney = models.IntegerField(db_column='totalMoney')
    totalIntro = models.IntegerField(db_column='totalIntro')
    totalPer = models.IntegerField(db_column='totalPer')
    introBet = models.IntegerField(db_column='introBet')
    authority = models.PositiveIntegerField(db_column='authority',validators=[MaxValueValidator(3)] )



class User1(models.Model):
    date = models.DateTimeField(primary_key=True, db_column='date',max_length=100)
    account = models.CharField(primary_key=True, db_column='account',max_length=20,blank=False)
    bet = models.IntegerField(db_column='bet',max_length=20)
    number = models.CharField(db_column='number',max_length=20)
    durationBet = models.IntegerField(db_column='durationBet',max_length=20)

class Period(models.Model) :
    date = models.DateTimeField(primary_key=True, db_column='date',max_length=100)
    period = models.CharField( db_column='period', max_length=2 )
