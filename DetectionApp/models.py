from django.db import models
from userApp.models import User
import os
from uuid import uuid4
from django.utils import timezone

def date_upload_clean(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([
        'clean',
        ymd_path,
        uuid_name + extension,
        ])

def date_upload_detection(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([
        'detection',
        ymd_path,
        uuid_name + extension,
        ])

# Create your models here.
class WasteCategoryL(models.Model):
    idx = models.AutoField(primary_key=True)
    cg_name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'waste_category_l'


class WasteCategoryM(models.Model):
    idx = models.AutoField(primary_key=True)
    cg_name = models.CharField(max_length=45)
    cg_large_idx = models.ForeignKey(WasteCategoryL, models.DO_NOTHING, db_column='cg_large_idx', blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'waste_category_m'


class WasteCategoryS(models.Model):
    idx = models.AutoField(primary_key=True)
    cg_name = models.CharField(max_length=45)
    cg_middle_idx = models.ForeignKey(WasteCategoryM, models.DO_NOTHING, db_column='cg_middle_idx', blank=True, null=True)
    label_name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waste_category_s'

class CategoryRegulation(models.Model):
    idx = models.AutoField(primary_key=True)
    cg_name = models.CharField(max_length=100, blank=True, null=True)
    cg_small_idx = models.ForeignKey(WasteCategoryS, models.DO_NOTHING, db_column='cg_small_idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_regulation'

class Upload(models.Model):
    image = models.ImageField(upload_to=date_upload_detection)

    class Meta:
        managed = False
        db_table = 'itemdetectionApp_upload'

class Upload_Clean(models.Model):
    image = models.ImageField(upload_to=date_upload_clean)

    class Meta:
        managed = False
        db_table = 'itemdetectionApp_upload_clean'


class ItemdetectionSHistory(models.Model):
    idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='user_idx', blank=True, null=True)
    cg_idx = models.ForeignKey(WasteCategoryS, models.DO_NOTHING, db_column='cg_idx', blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to=date_upload_detection)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'itemDetection_s_history'


class PointHistory(models.Model):
    idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='user_idx', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(blank=True, null=True)
    point_description = models.ForeignKey(WasteCategoryS, models.DO_NOTHING, db_column='point_description', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'point_history'