from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns(
    'activity.views',
    (r'^group/$',  'group_detail'),
    (r'^cancel_apply/$', 'cancel_apply'),
    (r'^apply_activity/$', 'apply_activity'),
    (r'^activity_detail/$', 'activity_detail'),

    (r'^balance/$', 'balance'),
    (r'^account_detail/$', 'account_detail'),
    (r'^activities/$', 'activities'),
    (r'^recharge/$', 'recharge'),
    (r'^settle_activity/$', 'settle_activity'),
    (r'^add_activity/$', 'add_activity'),
    (r'^chg_activity/$', 'chg_activity'),
    (r'^get_dlg/$', 'get_dlg'),
    (r'^managed_groups/$', 'managed_groups'),
    (r'^joined_groups/$', 'joined_groups'),
    (r'^join_group_apply/$', 'join_group_apply'),
    (r'^sys_msgs/$', 'sys_msgs'),
    (r'^process_group_apply/$', 'process_group_apply'),
    (r'^personal_infos/$', 'personal_infos'),
    (r'^chg_pwd/$', 'chg_pwd'),
    (r'^chg_personal_info/$', 'chg_personal_info'),
    (r'^send_test_mail/$', 'send_test_mail'),
    (r'^create_group/$', 'create_group'),
    (r'^register/$', 'register'),

    url(r'^index/$', 'index'),
    url(r'^groupadmin/$', 'groupadmin'),

    url(r'^monitor/500/$', 'monitor__500'),
)
