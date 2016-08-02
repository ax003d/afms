# -*- coding: utf-8 -*- 

import datetime
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import simplejson
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models.query import QuerySet

import markdown

from activity import models
from activity import utils
from activity.forms import PasswordResetForm, GroupForm
from activity.models import Group, GroupShip


logger = logging.getLogger('django.request')


@login_required
def profile(request):
    groups = request.user.groupship_set.all()
    ctx = {'user': request.user, 
           'groups': groups }
    return render_to_response('activity/profile.html', ctx)


@login_required
def group_detail(request):
    if 'gid' not in request.GET:
        return HttpResponse("group not found!")
    try:
        group = models.Group.objects.get(id=request.GET['gid'])
        group_ships = group.group_ships()
        self_gs = group_ships.get(member=request.user)
        activities = group.activities().order_by('-date')
        activity = None
        applies  = None
        applied  = False        
        settles = None
        if len(activities) > 0:
            activity = activities[0]
            applies = activity.applies()
            if len(applies.filter(member=request.user)) != 0:
                applied = True
            settles = activity.settlements()
        ctx = {'group': group, 
               'gss': group_ships, 
               'is_manager': self_gs.is_manager,
               'activity': activity,
               'applies': applies,
               'applied': applied,
               'activities': activities,
               'settles': settles}
        ctx.update(csrf(request))
        return render_to_response('activity/group_detail.html', ctx)
    except models.Group.DoesNotExist:
        return HttpResponse("group not found!")
    except Exception, e:
        return HttpResponse(e)


@login_required
def apply_activity(request):
    activity = models.ActivityDetail.objects.get(
        id=request.POST['activity'])
    if len(activity.applies().filter(member=request.user)) == 0:
        aa = models.ActivityApply(activity=activity, 
                                  apply_time=datetime.datetime.now(),
                                  member=request.user,
                                  num=request.POST['num'],
                                  remark=request.POST['remark'])
        aa.save()
    return HttpResponseRedirect(
        "/activity/group/?gid=%s" % activity.group.id)


@login_required
def cancel_apply(request):
    activity = models.ActivityDetail.objects.get(id=request.POST['activity'])
    activity.applies().get(member=request.user).delete()
    return HttpResponseRedirect("/activity/group/?gid=%s" % activity.group.id)


@login_required
def recharge(request):
    groupship = None
    results = {'success': False}
    try:
        groupship = models.GroupShip.objects.get(id=int(request.POST['groupship']))
        account_detail = models.AccountDetail(
            groupship = groupship,
            datetime = datetime.datetime.now(),
            money = float(request.POST['money']),
            remark = request.POST['remark']
            )
        account_detail.save()
        results['success'] = True
        results['member']  = groupship.member.last_name + groupship.member.first_name
        results['balance'] = groupship.balance
    except models.GroupShip.DoesNotExist:
        results['message'] = "groupship does not exist!"
    except Exception, e:
        results['message'] = str(e)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required
def activity_detail(request):
    if 'id' in request.GET:
        activity = models.ActivityDetail.objects.get(id=request.GET['id'])
        ctx = {'activity': activity, 
               'applies': activity.applies(), 
               'settles': activity.settlements() }
        return render_to_response('activity/activity_detail.html', ctx)
    return HttpResponse("activity not found!")


@login_required
def balance(request):
    return render_to_response('activity/balance.html', 
                              {'groups': request.user.groupship_set.all()})


@login_required
def account_detail(request):
    account_details = [ gs.account_details() for gs in request.user.groupship_set.all() ]
    if len(account_details) > 0:
        account_details = reduce(QuerySet.__or__, account_details)
    ctx = {'account_details': account_details}
    return render_to_response('activity/account_detail.html', ctx)


@login_required
def activities(request):
    activities = [ gs.activitysettlement_set.all() for gs in request.user.groupship_set.all() ]
    if len(activities) > 0:
        activities = reduce(QuerySet.__or__, activities)
    ctx = {'activities': activities}
    return render_to_response('activity/activities.html', ctx)
    

@login_required
def settle_activity(request):
    results = {'success': False}
    idx = 0
    try:
        activity = models.ActivityDetail.objects.get(id=request.POST['activity'])
        settles = []
        while True:
            k_groupship = u"set_lst[%d]['groupship']" % idx
            k_b_pay = u"set_lst[%d]['balance_pay']" % idx
            k_b_pay = u"0" if len(k_b_pay) == 0 else k_b_pay;
            k_c_pay = u"set_lst[%d]['cash_pay']" % idx
            k_c_pay = u"0" if len(k_c_pay) == 0 else k_c_pay;
            k_remark = u"set_lst[%d]['remark']" % idx
            if k_groupship not in request.POST:
                break
            groupship = models.GroupShip.objects.get(id=request.POST[k_groupship])
            settle = models.ActivitySettlement(
                activity  = activity,
                groupship = groupship,
                balance_pay = float(request.POST[k_b_pay]),
                cash_pay = float(request.POST[k_c_pay]),
                remark = request.POST[k_remark]
                )
            settles.append(settle)            
            idx += 1
        for s in settles:
            s.save()
        results['success'] = True
        results['gid'] = activity.group.id
    except models.ActivityDetail.DoesNotExist:
        pass
    except Exception, e:
        pass
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required
def add_activity(request):
    results = {'success': False}
    try:
        group = models.Group.objects.get(id=request.POST['group'])
        if len(models.ActivityDetail.objects.filter(
                group=group, date=request.POST['date'])) == 0:
            activity = models.ActivityDetail(
                group = group,
                date = request.POST['date'],
                totoal_fee = 0.0,
                remark = request.POST['remark']
                )
            activity.save()
        results['success'] = True
        results['gid'] = group.id
    except models.Group.DoesNotExist:
        results['message'] = "group not found!";
    except Exception, e:
        results['message'] = str(e);
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')    


@login_required
def chg_activity(request):
    results = {'success': False}
    try:
        activity = models.ActivityDetail.objects.get(id=request.POST['activity'])
        activity.date = request.POST['date']
        activity.totoal_fee = request.POST['total_fee']
        activity.remark = request.POST['remark']
        activity.save()
        results['success'] = True
        results['gid'] = activity.group.id
    except models.ActivityDetail.DoesNotExist:
        results['message'] = "activity not found!";
    except Exception, e:
        results['message'] = str(e);
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required
def get_dlg(request):
    ctx = {}
    ctx.update(csrf(request))
    try:
        return render_to_response('activity/%s.html' % request.GET['dlg_type'], ctx)
    except:
        return HttpResponse("dlg not found!")


@login_required
def managed_groups(request):
    items = []
    for gs in request.user.groupship_set.filter(is_manager=True):
        item = {}
        item['group'] = gs.group
        item['activity_num'] = len(gs.group.activities())
        group_ships = gs.group.group_ships()
        item['member_num'] = len(group_ships)
        balance = 0
        for sub_gs in group_ships:
            balance += sub_gs.balance
        item['total_balance'] = balance
        items.append(item)
    ctx = {'items': items}
    return render_to_response('activity/managed_groups.html', ctx)


@login_required
def joined_groups(request):
    items = []
    others = []
    groups = []
    try:
        for gs in request.user.groupship_set.all():
            item = {}
            item['group'] = gs.group
            groups.append(gs.group)
            group_ships = gs.group.group_ships()
            item['member_num'] = len(group_ships)
            item['activity_num'] = len(gs.group.activities())
            item['joined_num'] = len(gs.settlements())
            item['percentage'] = item['joined_num'] * 1.0 / item['activity_num'] * 100 if item['activity_num'] != 0 else 0
            item['balance'] = gs.balance
            items.append(item)    
        for g in models.Group.objects.all():
            if g in groups:
                continue
            item = {}
            item['group'] = g
            group_ships = g.group_ships()
            item['member_num'] = len(group_ships)
            item['activity_num'] = len(g.activities())
            others.append(item)
            item['applied'] = True if len(models.JoinGroupApply.objects.filter(
                    joiner=request.user, group=g, processed=False)) > 0 else False
    except Exception, e:
        return HttpResponse(str(e))
    ctx = {'items': items, 'others': others}
    return render_to_response('activity/joined_groups.html', ctx)


@login_required
def join_group_apply(request):
    results = {'success': False}
    try:
        group = models.Group.objects.get(id=request.POST['group'])
        apply = models.JoinGroupApply(
            joiner = request.user,
            datetime = datetime.datetime.now(),
            group = group,
            accepted = False,
            processed = False,
            remark = request.POST['remark'],
            )
        apply.save()
        admin = group.get_admin()
        if len(admin.email) != 0:
            utils.send_mail(u"加入小组请求",
                            u"%s 请求加入小组 %s!" % (request.user.username, 
                                                      group.name), 
                            admin.email)
        results['success'] = True
    except models.Group.DoesNotExist:
        resutls['message'] = "group doesnot found!"
    except Exception, e:
        resutls['message'] = str(e)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required
def sys_msgs(request):
    applies = []
    for gs in request.user.groupship_set.filter(is_manager=True):
        applies.extend(gs.group.joingroupapply_set.filter(processed=False))
    ctx = {'applies': applies, 
           'sys_msgs': request.user.sysmessage_set.all() }
    ctx.update(csrf(request))
    return render_to_response("activity/sys_msgs.html", ctx)


@login_required
def process_group_apply(request):
    results = {'success': False}
    try:
        apply = models.JoinGroupApply.objects.get(id=request.POST['apply'])
        apply.accepted = (request.POST['accepted'] == "1")
        apply.processed = True
        apply.save()
        if len(models.GroupShip.objects.filter(group=apply.group, member=apply.joiner)) != 0:
            results = {'success': True}
            json = simplejson.dumps(results)
            return HttpResponse(json, mimetype='application/json')
        
        if apply.accepted:
            gs = models.GroupShip(group=apply.group,
                                  member=apply.joiner,
                                  is_manager=False,
                                  balance=0)
            gs.save()
            if len(gs.member.email) != 0:
                utils.send_mail(u"成功加入小组",
                                u"您已被管理员批准加入小组 %s !" % gs.group.name,
                                gs.member.email)
        else:
            msg = models.SysMessage(
                datetime=datetime.datetime.now(),
                msg_to=apply.joiner,
                message=u"抱歉, 您被拒绝加入小组:" + apply.group.name,
                status=models.MSG_STATUS_UNREAD)
            msg.save()
        results = {'success': True}
    except models.JoinGroupApply.DoesNotExist:
        results['message'] = 'join group apply not found!'
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')    


@login_required
def personal_infos(request):
    ctx = {'user': request.user}
    ctx.update(csrf(request))
    return render_to_response('activity/personal_info.html', ctx)


@login_required
def chg_pwd(request):
    results = {'success': False, 
               'old_pwd_err': False,
               'new_pwd_err': False}
    try:
        if not request.user.check_password(request.POST['old_pwd']):
            results['old_pwd_err'] = True
        if request.POST['password1'] != request.POST['password2']:
            results['new_pwd_err'] =  True
        if (not results['old_pwd_err']) and ( not results['new_pwd_err']):
            request.user.set_password(request.POST['password1'])
            request.user.save()
            results['success'] = True
    except Exception, e:
        results['message'] = str(e)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')    
    

@login_required
def chg_personal_info(request):
    results = {'success': False,
               'email_used': False}
    try:
        request.user.last_name = request.POST['last_name']
        request.user.first_name = request.POST['first_name']
        if len(models.User.objects.filter(
                Q(email=request.POST['email']),
                ~Q(username=request.user.username))
               ) != 0:
            results['email_used'] = True
        else:
            request.user.email = request.POST['email']
        request.user.save()
        results['success'] = True
    except Exception, e:
        results['message'] = str(e)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required
def send_test_mail(request):
    results = {'success': False}
    try:
        email = request.GET['email']
        utils.send_mail(u"测试邮件", 
                        u"This is a test email from afms.sinaapp.com!",
                        email)
        results['success'] = True
    except Exception, e:
        results['message'] = str(e)
        logger.exception('send test mail failed')
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')


@login_required
def create_group(request):
    results = {'success': False}
    try:
        group = models.Group(
            name=request.POST['name'],
            description=request.POST['remark'])
        group.save()
        gs = models.GroupShip(
            group=group,
            member=request.user,
            is_manager=True,
            balance=0)
        gs.save()
        results['success'] = True
    except Exception, e:
        results['message'] = str(e)
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')
    

def register(request):
    ctx = {'user_exist': False,
           'email_used': False}
    ctx.update(csrf(request))
    if request.method == 'GET':
        return render_to_response("registration/register.html", ctx)
    
    try:
        ctx['username'] = request.POST['username']
        ctx['email'] = request.POST['email']
        user = models.User.objects.get(username=request.POST['username'])
        ctx['user_exist'] = True
    except models.User.DoesNotExist:
        if len(models.User.objects.filter(email=request.POST['email'])) != 0:
            ctx['email_used'] = True
        else:
            user = models.User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password_1'])
            user.first_name = request.POST['username']
            user.save()
            user = authenticate(username=user.username, 
                                password=request.POST['password_1'])
            login(request, user)
            return HttpResponseRedirect("/")
    except Exception, e:
        ctx['message'] = str(e)
    return render_to_response("registration/register.html", ctx)    


def verify_username(request):
    try:
        models.User.objects.get(username=request.GET.get('username'))
        return HttpResponse('false')
    except models.User.DoesNotExist:
        return HttpResponse('true')


def verify_email(request):
    try:
        models.User.objects.get(email=request.GET.get('email'))
        return HttpResponse('false')
    except models.User.DoesNotExist:
        return HttpResponse('true')


# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above

@csrf_protect
def password_reset(request, is_admin_site=False, template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        password_reset_form=PasswordResetForm, token_generator=default_token_generator,
        post_reset_redirect=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            opts['request'] = request
            if is_admin_site:
                opts['domain_override'] = request.META['HTTP_HOST']
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))



def index(request):
    return render_to_response('index.html', {}, RequestContext(request))


@login_required
def groupadmin(request):
    gid = request.GET.get('gid')

    group = get_object_or_404(Group, id=gid)
    # check is admin
    if GroupShip.objects.filter(group=group, member=request.user, is_manager=True).count() == 0:
        ctx = {'title': u'您没有权限管理该小组',
               'message': u'只有小组管理员才可管理该小组!'}
        return render_to_response('warning.html', ctx, RequestContext(request))

    ctx = {}
    if request.method == 'POST':
        form = GroupForm(request.POST)
        form.instance = group
        if not form.is_valid():
            ctx['status'] = 'ERROR'
        else:
            ctx['status'] = 'OK'
            form.save()
            group = form.instance

    ctx['group'] = group
    ctx.update(csrf(request))
    return render_to_response('groupadmin.html', ctx, RequestContext(request))


def monitor__500(request):
    raise Exception("should show 500 error page.")


@csrf_exempt
def preview__markdown(request):
    html = markdown.markdown(request.POST.get('data'))
    return HttpResponse(html)
