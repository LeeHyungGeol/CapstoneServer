from django.db import models
from userApp.models import User
import os
from uuid import uuid4
from django.utils import timezone
from django.conf import settings
from django.conf.urls.static import static
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

class Community(models.Model):
    idx = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    share_complete = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to=date_upload_community, null=True, blank=True)
    user_idx = models.ForeignKey(User, models.DO_NOTHING, db_column='user_idx', blank=True, null=True)

    def delete(self, *args, **kargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Community, self).delete(*args, **kargs)  # 원래의 delete 함수를 실행

    class Meta:
        managed = False
        db_table = 'community'