from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
from uuid import uuid4
from django.utils import timezone
# Create your models here.


def date_upload_community(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([
        'community',
        ymd_path,
        uuid_name + extension,
        ])



class LocationWasteInformation(models.Model):
    idx = models.AutoField(primary_key=True)
    dong = models.CharField(max_length=45, blank=True, null=True)
    discharge_day = models.CharField(max_length=45, blank=True, null=True)
    house_start = models.CharField(max_length=45, blank=True, null=True)
    house_end = models.CharField(max_length=45, blank=True, null=True)
    food_start = models.CharField(max_length=45, blank=True, null=True)
    food_end = models.CharField(max_length=45, blank=True, null=True)
    house_method = models.CharField(max_length=255, blank=True, null=True)
    food_method = models.CharField(max_length=255, blank=True, null=True)
    recycle_method = models.CharField(max_length=255, blank=True, null=True)
    house_day = models.CharField(max_length=45, blank=True, null=True)
    food_day = models.CharField(max_length=45, blank=True, null=True)
    recycle_day = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'location_waste_information'


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None):
        if not user_id:
            raise ValueError("Users must have an email address")

        user = self.model(
            user_id=user_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None):
        user = self.create_user(
            user_id=user_id,
            password=password

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    location_idx = models.ForeignKey(LocationWasteInformation, models.DO_NOTHING, db_column='location_idx', blank=True, null=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    idx = models.AutoField(primary_key=True)
    user_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
    user_nm = models.CharField(max_length=50, blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    object = UserManager()
    USERNAME_FIELD = 'user_id'

    class Meta:
        # managed = False
        db_table = 'user'


class Community(models.Model):
    idx = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    share_complete = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to=date_upload_community)
    user_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='user_idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'community'

