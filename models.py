# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class CategoryRegulation(models.Model):
    idx = models.AutoField(primary_key=True)
    cg_name = models.CharField(max_length=100, blank=True, null=True)
    cg_small_idx = models.ForeignKey('WasteCategoryS', models.DO_NOTHING, db_column='cg_small_idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_regulation'


class Community(models.Model):
    idx = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    share_complete = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=100)
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'community'


class DischargeTips(models.Model):
    idx = models.AutoField(primary_key=True)
    category_m_idx = models.ForeignKey('WasteCategoryM', models.DO_NOTHING, db_column='category_m_idx', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    item_corresponding = models.TextField(blank=True, null=True)
    item_discorresponding = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discharge_tips'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ItemdetectionSHistory(models.Model):
    idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx', blank=True, null=True)
    cg_idx = models.ForeignKey('WasteCategoryS', models.DO_NOTHING, db_column='cg_idx', blank=True, null=True)
    accuracy = models.FloatField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'itemDetection_s_history'


class ItemdetectionappUpload(models.Model):
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'itemdetectionApp_upload'


class ItemdetectionappUploadClean(models.Model):
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'itemdetectionApp_upload_clean'


class KnoxAuthtoken(models.Model):
    digest = models.CharField(primary_key=True, max_length=128)
    salt = models.CharField(unique=True, max_length=16)
    created = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)
    expiry = models.DateTimeField(blank=True, null=True)
    token_key = models.CharField(max_length=8)

    class Meta:
        managed = False
        db_table = 'knox_authtoken'


class LocationWasteInformation(models.Model):
    idx = models.AutoField(primary_key=True)
    dong = models.CharField(max_length=45, blank=True, null=True)
    administrative_area = models.CharField(db_column='Administrative area', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
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
    recycle_start = models.CharField(max_length=45, blank=True, null=True)
    recycle_end = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_waste_information'


class MeasureHistory(models.Model):
    idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx', blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'measure_history'


class MeasureUpload(models.Model):
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'measure_upload'


class MessageReceiver(models.Model):
    idx = models.AutoField(primary_key=True)
    recv_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='recv_idx', blank=True, null=True)
    send_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='send_idx', blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_receiver'


class MessageSender(models.Model):
    idx = models.AutoField(primary_key=True)
    recv_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='recv_idx', blank=True, null=True)
    send_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='send_idx', blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=100, blank=True, null=True)
    recv_chk = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_sender'


class PointHistory(models.Model):
    idx = models.AutoField(primary_key=True)
    user_idx = models.ForeignKey('User', models.DO_NOTHING, db_column='user_idx', blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)
    point_description = models.ForeignKey('WasteCategoryS', models.DO_NOTHING, db_column='point_description', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'point_history'


class RegulationFee(models.Model):
    idx = models.AutoField(primary_key=True)
    fee_flag = models.CharField(max_length=45, blank=True, null=True)
    condition_value = models.FloatField(blank=True, null=True)
    cg_idx = models.ForeignKey('WasteCategoryS', models.DO_NOTHING, db_column='cg_idx', blank=True, null=True)
    over_fee = models.CharField(max_length=45, blank=True, null=True)
    down_fee = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regulation_fee'


class User(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    idx = models.AutoField(primary_key=True)
    user_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
    user_nm = models.CharField(max_length=50, blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    is_admin = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    location_idx = models.ForeignKey(LocationWasteInformation, models.DO_NOTHING, db_column='location_idx', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


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
