from django.db import models
import os
from uuid import uuid4
from django.utils import timezone

# Create your models here.

def date_upload_measure(instance, filename):
    # upload_to="%Y/%m/%d" 처럼 날짜로 세분화
    ymd_path = timezone.now().strftime('%Y/%m/%d')
    # 길이 32 인 uuid 값
    uuid_name = uuid4().hex
    # 확장자 추출
    extension = os.path.splitext(filename)[-1].lower()
    # 결합 후 return
    return '/'.join([
        'measure',
        ymd_path,
        uuid_name + extension,
        ])


class Upload(models.Model):
    image = models.ImageField(upload_to=date_upload_measure)

    class Meta:
        managed = False
        db_table = 'itemdetectionApp_upload'