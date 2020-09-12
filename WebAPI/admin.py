from django.contrib import admin
from WebAPI import models
#; Register your models here.

class RouterAdmin(admin.ModelAdmin):
    list_display = ['rid','port','portip','neibrid']
    ordering = ['rid']

class AnomalyAdmin(admin.ModelAdmin):
    list_display = ['rid','time','event','prob_1','prob_2','prob_3','prob_4','prob_5','prob_6']
    ordering = ['time','prob_1']

class PacketAdmin(admin.ModelAdmin):
    list_display = ['rid','stime','hello_num','lsr_num','lsu_num','lsa_num']
    ordering = ['rid']

admin.site.register(models.Anomaly, AnomalyAdmin)
admin.site.register(models.Router, RouterAdmin)
admin.site.register(models.Packet,PacketAdmin)