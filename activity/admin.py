from django.contrib import admin
from activity import models


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class JoinGroupApplyAdmin(admin.ModelAdmin):
    list_display = ('joiner', 'datetime', 'group', 'accepted', 'remark')
    

class GroupShipAdmin(admin.ModelAdmin):
    list_display = ('group', 'member', 'is_manager', 'balance')


class ActivityDetailAdmin(admin.ModelAdmin):
    list_display = ('group', 'date', 'totoal_fee', 'remark')


class ActivityApplyAdmin(admin.ModelAdmin):
    list_display = ('activity', 'member', 'num', 'remark')


class ActivitySettlementAdmin(admin.ModelAdmin):
    list_display = ('activity', 'groupship', 'balance_pay', 'cash_pay', 'remark')
    

class AccountDetailAdmin(admin.ModelAdmin):
    list_display = ('groupship', 'datetime', 'money', 'remark')    
    
    
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.JoinGroupApply, JoinGroupApplyAdmin)
admin.site.register(models.GroupShip, GroupShipAdmin)
admin.site.register(models.ActivityDetail, ActivityDetailAdmin)
admin.site.register(models.AccountDetail, AccountDetailAdmin)
admin.site.register(models.ActivityApply, ActivityApplyAdmin)
admin.site.register(models.ActivitySettlement, ActivitySettlementAdmin)
