from django.db import models

# Create your models here.


class DischargeTips(models.Model):
    idx = models.AutoField(primary_key=True)
    category_m_idx = models.ForeignKey('WasteCategoryM', models.DO_NOTHING, db_column='category_m_idx', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    item_corresponding = models.TextField(blank=True, null=True)
    item_discorresponding = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discharge_tips'


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