from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from random import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.cache import cache
import datetime
from django_random_id_model import RandomIDModel

class BloodType(models.Model):

    bloodtype = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.bloodtype
    class Meta:
        verbose_name = "หมู่เลือด:Blood type"


class DaysOfWeek(models.Model):
    daysofweek = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.daysofweek}'
    
    class Meta:
        verbose_name = "วันประจำวันเกิด:Days of week"


class NakSus(models.Model):
    naksus = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.naksus}'
    class Meta:
        verbose_name = "นักษัตร:Nak sus"

class RaSi(models.Model):
    rasi = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.rasi}'
    
    class Meta:
        verbose_name = "ราศี:Rasi"


class ScoreBloodType(models.Model):
    bloodtypeA = models.ForeignKey(
        BloodType, blank=True, null=True, on_delete=models.CASCADE, related_name='bloodtype1')
    bloodtypeB = models.ForeignKey(
        BloodType, blank=True, null=True, on_delete=models.CASCADE, related_name='bloodtypeB')
    scorebloodtype = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.bloodtypeA} {self.bloodtypeB} {self.scorebloodtype}'
    
    class Meta:
        verbose_name = "คะแนนของหมู่เลือด:Score Blood type"

class ScoreDaysOfWeek(models.Model):
    daysofweekA = models.ForeignKey(
        DaysOfWeek, blank=True, null=True, on_delete=models.CASCADE, related_name='daysofweek1')
    daysofweekB = models.ForeignKey(
        DaysOfWeek, blank=True, null=True, on_delete=models.CASCADE, related_name='daysofweek2')
    scoredaysofweek = models.IntegerField()

    def __str__(self):
        return f'{self.daysofweekA} {self.daysofweekB} {self.scoredaysofweek}'
    
    class Meta:
        verbose_name = "คะแนนของวันประจำวันเกิด:Score Days of week"


class ScoreNakSus(models.Model):
    naksusA = models.ForeignKey(
        NakSus, blank=True, null=True, on_delete=models.CASCADE, related_name='naksus1')
    naksusB = models.ForeignKey(
        NakSus, blank=True, null=True, on_delete=models.CASCADE, related_name='naksus2')
    scorenaksus = models.IntegerField()

    def __str__(self):
        return f'{self.naksusA} {self.naksusB} {self.scorenaksus}'
    class Meta:
        verbose_name = "คะแนนของนักษัตร:Score Naksus"

class ScoreRaSi(models.Model):
    rasiA = models.ForeignKey(
        RaSi, blank=True, null=True, on_delete=models.CASCADE, related_name='rasi1')
    rasiB = models.ForeignKey(
        RaSi, blank=True, null=True, on_delete=models.CASCADE, related_name='rasi2')
    scorerasi = models.IntegerField()

    def __str__(self):
        return f'{self.rasiA} {self.rasiB} {self.scorerasi}'
    class Meta:
        verbose_name = "คะแนนของราศี:Score Rasi"

def get_daysofweek():
    return DaysOfWeek.objects.get(id=1)


def get_naksus():
    return NakSus.objects.get(id=1)


def get_rasi():
    return RaSi.objects.get(id=1)


def get_bloodtype():
    return BloodType.objects.get(id=1)

def random_image():  
 


    try:
        mm = Member.objects.all()
        for m in mm:
            # print(m.username)
            if m.gender == "M":
                dir = os.path.join(settings.BASE_DIR,'media/male')
                # print(dir,f'____{m.username}___________')
            if m.gender == "F":
                dir = os.path.join(settings.BASE_DIR, 'media/female')
               
            files = os.listdir(dir)
            images = [file for file in files if os.path.isfile(os.path.join(dir, file))]
            rand = choice(images)
        return rand

    except:
        directory = os.path.join(settings.BASE_DIR, 'media/male')
        files = os.listdir(directory)
        images = [file for file in files if os.path.isfile(os.path.join(directory, file))]
        rand = choice(images)
        return rand
           
     
    
class Member(AbstractUser):
    your_date = date(1998, 3, 11)
    GENDER = [('F', 'Female'), ('M', 'Male')]
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=1, default='M')
    testes = models.CharField(
        choices=GENDER, max_length=1, default='M')  # sex of Testes
    # profile_image = models.ImageField(upload_to='profile_pics') 
    profile_image = models.ImageField(
        default=random_image, upload_to='profile_pics')  # default='default.jpg', ทำไว้เผื่อ Auto dump data Command https://campus.campus-star.com/app/uploads/2018/04/TopLazyLoxy17.jpg
    # YYYY-MM-DD
    birthday = models.DateField(default=your_date)
    bloodtype = models.ForeignKey(
        BloodType, default=3, verbose_name="หมู่เลือด", on_delete=models.CASCADE)

    def __str__(self):
        return f'ID:{self.id} ({self.username})'

    class Meta:
        verbose_name = 'สมาชิก:Member'
    



class Profile(models.Model):

    member = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    daysofweek = models.ForeignKey(
        DaysOfWeek, default=get_daysofweek, verbose_name='วันประจำวันเกิด', on_delete=models.CASCADE)
    naksus = models.ForeignKey(
        NakSus, default=get_naksus, verbose_name="นักษัตร", on_delete=models.CASCADE)
    rasi = models.ForeignKey(RaSi, default=get_rasi,
                             verbose_name='ราศี', on_delete=models.CASCADE)
    bloodtype = models.ForeignKey(
        BloodType, default=get_bloodtype, verbose_name="หมู่เลือด", on_delete=models.CASCADE)
    profile_score = models.FloatField(default=5.0)
    created = models.DateTimeField(auto_now_add=True)  # When it was create
    updated = models.DateTimeField(auto_now=True)  # When it was update

    def __str__(self):
        return f'Profile of "id:{self.id} {self.member.username} {self.age}" '

    @receiver(post_save, sender=Member)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(member=instance)

    @receiver(post_save, sender=Member)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
    
   

    def save(self, *args, **kwargs):

        # DAYSOfWEEK = [('SUN','Sunday'),('MON','Monday'),('TUE','Tuesday'),('WED','Wednesday'),('THU','Thursday'),('FRI','Friday'),('SAT','Saturday')]
        if self.member.bloodtype:
            if self.member.bloodtype is None:
                self.bloodtype = get_bloodtype
            else:
                self.bloodtype = self.member.bloodtype
        if self.member.birthday:
            today = date.today()
            self.age = today.year - self.member.birthday.year
            

        if self.daysofweek:
            try:
                daysoftheweek = self.member.birthday.strftime('%A')
                if daysoftheweek == 'Sunday':
                    self.daysofweek_id = 1

                elif daysoftheweek == 'Monday':
                    self.daysofweek_id = 2

                elif daysoftheweek == 'Tuesday':
                    self.daysofweek_id = 3

                elif daysoftheweek == 'Wednesday':
                    self.daysofweek_id = 4

                elif daysoftheweek == 'Thursday':
                    self.daysofweek_id = 5

                elif daysoftheweek == 'Friday':
                    self.daysofweek_id = 6

                elif daysoftheweek == 'Saturday':
                    self.daysofweek_id = 7

            except:
                daysoftheweek = None
        # print('_______day of date________',self.member.birthday.strftime( '%A' ))

        if self.naksus:
            try:
                year = self.member.birthday.year
                # print(f'_______self.member.birthday.year_______{type(year)}__________{year}')
                # if year == 2020 and  year == 2008 and   year == 1996 and   year ==1984 and   year == 1972 and   year == 1960:
                if year == 2020 or year == 2008 or year == 1996 or year == 1984 or year == 1972 or year == 1960:
                    self.naksus_id = 1

                elif year == 2021 or year == 2009 or year == 1997 or year == 1985 or year == 1973 or year == 1961:
                    self.naksus_id = 2

                elif year == 2022 or year == 2010 or year == 1998 or year == 1986 or year == 1974 or year == 1962:
                    self.naksus_id = 3

                elif year == 2023 or year == 2011 or year == 1999 or year == 1987 or year == 1975 or year == 1963:
                    self.naksus_id = 4

                elif year == 2024 or year == 2012 or year == 2000 or year == 1988 or year == 1976 or year == 1964:
                    self.naksus_id = 5

                elif year == 2025 or year == 2013 or year == 2001 or year == 1989 or year == 1977 or year == 1965:
                    self.naksus_id = 6

                elif year == 2026 or year == 2014 or year == 2002 or year == 1990 or year == 1978 or year == 1966:
                    self.naksus_id = 7

                elif year == 2027 or year == 2015 or year == 2003 or year == 1991 or year == 1979 or year == 1967:
                    self.naksus_id = 8

                elif year == 2028 or year == 2016 or year == 2004 or year == 1992 or year == 1980 or year == 1968:
                    self.naksus_id = 9

                elif year == 2029 or year == 2017 or year == 2005 or year == 1993 or year == 1981 or year == 1969:
                    self.naksus_id = 10

                elif year == 2030 or year == 2018 or year == 2006 or year == 1994 or year == 1982 or year == 1970:
                    self.naksus_id = 11

                elif year == 2031 or year == 2019 or year == 2007 or year == 1995 or year == 1983 or year == 1971:
                    self.naksus_id = 12

            except:
                year = None
        # print(f'_______self.member.birthday.year_______{self.naksus}__________{year}_______{self.naksus_id}')
        if self.rasi:
            # pass
            try:
                rasi = self.member.birthday
                print(rasi.day)
                if ((int(rasi.month) == 12 and int(rasi.day) >= 16) or (int(rasi.month) == 1 and int(rasi.day) <= 14)):
                    self.rasi_id = 12

                elif ((int(rasi.month) == 1 and int(rasi.day) >= 15) or (int(rasi.month) == 2 and int(rasi.day) <= 12)):
                    self.rasi_id = 1

                elif ((int(rasi.month) == 2 and int(rasi.day) >= 13) or (int(rasi.month) == 3 and int(rasi.day) <= 14)):
                    self.rasi_id = 2

                elif ((int(rasi.month) == 3 and int(rasi.day) >= 15) or (int(rasi.month) == 4 and int(rasi.day) <= 12)):
                    self.rasi_id = 3

                elif ((int(rasi.month) == 4 and int(rasi.day) >= 13) or (int(rasi.month) == 5 and int(rasi.day) <= 14)):
                    self.rasi_id = 4

                elif ((int(rasi.month) == 5 and int(rasi.day) >= 15) or (int(rasi.month) == 6 and int(rasi.day) <= 14)):
                    self.rasi_id = 5

                elif ((int(rasi.month) == 6 and int(rasi.day) >= 15) or (int(rasi.month) == 7 and int(rasi.day) <= 14)):
                    self.rasi_id = 6

                elif ((int(rasi.month) == 7 and int(rasi.day) >= 15) or (int(rasi.month) == 8 and int(rasi.day) <= 15)):
                    self.rasi_id = 7

                elif ((int(rasi.month) == 8 and int(rasi.day) >= 16) or (int(rasi.month) == 9 and int(rasi.day) <= 16)):
                    self.rasi_id = 8

                elif ((int(rasi.month) == 9 and int(rasi.day) >= 17) or (int(rasi.month) == 10 and int(rasi.day) <= 15)):
                    self.rasi_id = 9

                elif ((int(rasi.month) == 10 and int(rasi.day) >= 17) or (int(rasi.month) == 11 and int(rasi.day) <= 15)):
                    self.rasi_id = 10

                elif ((int(rasi.month) == 11 and int(rasi.day) >= 16) or (int(rasi.month) == 12 and int(rasi.day) <= 15)):
                    self.rasi_id = 11

            except:
                rasi = None

        super(Profile, self).save(*args, **kwargs)
        # print(f'_______{self.member}_____________{year}_______')

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)
    
    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()   
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else: 
            return False
    class Meta:
        verbose_name = "โปรไฟล์:Profile"
    
class Rating(models.Model):
    member_owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='member_owner')
    member_excluded = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='member_excluded')
    ratingPoint = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('member_owner', 'member_excluded')
        verbose_name = "ลำดับคะแนน:Rating"

    def __str__(self):
        return str(self.member_owner) + ' ' + str(self.member_excluded) + ' ' + str(self.ratingPoint)


class Match(models.Model):
    matcher_owner = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='matcher_owner', null=True, blank=True)
    matcher_excluded = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='matcher_excluded', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('matcher_owner', 'matcher_excluded')
       
        verbose_name = "ชอบ:Match"

    def __str__(self):
        return f'{self.matcher_owner}  {self.matcher_excluded}  {self.rating})'


class NoMatch(models.Model):
    nomatcher_owner = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='nomatcher_owner', null=True, blank=True)
    nomatcher_excluded = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='nomatcher_excluded', null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('nomatcher_owner', 'nomatcher_excluded')
       
        verbose_name = "ไม่ชอบ:NoMatch"

    def __str__(self):
        return f'{self.nomatcher_owner}  {self.nomatcher_excluded}  {self.rating})'




