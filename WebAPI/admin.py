from django.contrib import admin
from WebAPI import models
#; Register your models here.
class AnomalyAdmin(admin.ModelAdmin):
    list_display = ['rid','time','event','prob_1','prob_2','prob_3','prob_4','prob_5','prob_6']
    ordering = ['time','prob_1']

admin.site.register(models.Anomaly, AnomalyAdmin)