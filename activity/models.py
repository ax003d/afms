# -*- coding: utf-8 -*- 

import datetime
import markdown

from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name        = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def get_description(self):
        return markdown.markdown(self.description)

    def group_ships(self):
        return self.groupship_set.all()

    def activities(self):
        return self.activitydetail_set.all()

    def get_admin(self):
        return self.group_ships().filter(is_manager=True)[0].member


class JoinGroupApply(models.Model):
    joiner    = models.ForeignKey(User)
    datetime  = models.DateTimeField()
    group     = models.ForeignKey(Group)
    accepted  = models.BooleanField()
    processed = models.BooleanField()
    remark    = models.TextField(blank=True)

    def __unicode__(self):
        return self.group.name + "-" + self.joiner.last_name + self.joiner.first_name

    
class GroupShip(models.Model):
    group      = models.ForeignKey(Group)
    member     = models.ForeignKey(User)
    is_manager = models.BooleanField()
    balance    = models.FloatField()
    
    def __unicode__(self):
        return self.group.name + "-" + self.member.last_name + self.member.first_name

    def account_details(self):
        return self.accountdetail_set.all()

    def settlements(self):
        return self.activitysettlement_set.all()



class ActivityDetail(models.Model):
    group      = models.ForeignKey(Group)
    date       = models.DateField()
    totoal_fee = models.FloatField()
    remark     = models.TextField(blank=True)

    def __unicode__(self):
        return self.group.name + " " + str(self.date) 

    def applies(self):
        return self.activityapply_set.all().order_by('apply_time')

    def settlements(self):
        return self.activitysettlement_set.all()


class ActivityApply(models.Model):
    activity   = models.ForeignKey(ActivityDetail)
    apply_time = models.DateTimeField()
    member     = models.ForeignKey(User)
    num        = models.IntegerField()
    remark     = models.TextField(blank=True)


class ActivitySettlement(models.Model):
    activity    = models.ForeignKey(ActivityDetail)    
    groupship   = models.ForeignKey(GroupShip)
    balance_pay = models.FloatField()
    cash_pay    = models.FloatField()
    remark      = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super(ActivitySettlement, self).save(*args, **kwargs)
        if self.balance_pay == 0.0:
            return
        ad = AccountDetail(groupship = self.groupship, 
                           datetime = datetime.datetime.now(),
                           money = self.balance_pay * -1,
                           remark = str(self.activity.date) + u" 活动费用")
        ad.save()


class AccountDetail(models.Model):
    groupship = models.ForeignKey(GroupShip)
    datetime  = models.DateTimeField()
    money     = models.FloatField()
    remark    = models.CharField(max_length=256, blank=True)    
        
    def save(self, *args, **kwargs):
        super(AccountDetail, self).save(*args, **kwargs)
        self.groupship.balance += self.money
        self.groupship.save()


MSG_STATUS_UNREAD  = 0
MSG_STATUS_READ    = 1
MSG_STATUS_DELETED = 2        


class SysMessage(models.Model):
    datetime = models.DateTimeField()
    # message from system
    msg_to   = models.ForeignKey(User)
    message  = models.TextField()
    status   = models.IntegerField()
