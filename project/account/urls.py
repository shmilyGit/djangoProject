from django.urls import path, re_path
from django.conf.urls import url
from django.conf import settings
from django.views.generic import TemplateView
from . import views as auth_views

app_name='account'
urlpatterns = [
	#注意基本类的视图的写法 .as_view(template_name= TemplateName),不再是{"template_name":"account/logout.html"},后者是基于视图的写法
	#django2.1已经使用基于类的视图代替了基于函数的视图,不过真用基于视图的也可以

    ##基于类的视图

    ##登录与注册
	path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name="user_login"),
	path('logout/', auth_views.LogoutView.as_view(template_name='account/login.html'), name="user_logout"),
	path('register/', auth_views.RegistrationView.as_view(), name="user_register"),

    ##基本信息修改
	re_path(r'^user-profile/(?P<tab>[1,2])/$', auth_views.UserProfileView.as_view(), name="user_profile"),
	path('save-userinfo/', auth_views.UserProfileView.as_view(), name="save_userinfo"),
	path('my-headimage/', auth_views.MineHeadImage.as_view(), name="my_headimage"),

    ##密码修改
	path('password-change/', auth_views.PasswordChangeView.as_view(template_name='account/user_profile.html',success_url='/account/password-change-done/'), name="password_change"),
	path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='account/user_profile.html'), name="password_change_done"),

    ##密码重置
	path('password-reset/', auth_views.PasswordResetView.as_view(
                                template_name='account/password_reset_form.html',
                                email_template_name='account/password_reset_email.html',
                                subject_template_name='account/password_reset_subject.txt',
                                success_url='/account/password-reset-done/'), name="password_reset"),
	path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
                                template_name='account/password_reset_done.html'), name="password_reset_done"),
	re_path(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(
                                template_name='account/password_reset_confirm.html',
                                success_url='/account/password-reset-complete/'), name="password_reset_confirm"),
	path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
                                template_name='account/password_reset_complete.html',
                                ), name="password_reset_complete"),


    ##基于函数的视图 django 低版本中可以使用url来指定URL,2.0版本之后弃用了url,改成了path
	#url(r'^login/$', auth_views.login, {"template_name":"account/login.html"}, name="user_login"), #也可以使用,不推荐使用
	#url(r'^logout/$', auth_views.logout,{"template_name":"account/login.html"}, name="user_logout"),
	#url(r'^user-profile/$', TemplateView.as_view(template_name='account/user_profile.html'), name="user_profile"),

    ##密码修改
	##template_name是给get请求使用, post_change_redirect是给post请求使用的
	#url(r'^password-change/$', auth_views.password_change,{"template_name":"account/user_profile.html","post_change_redirect":"/account/password-change-done/"}, name="password_change"),
	#url(r'^password-change-done/$', auth_views.password_change_done,{"template_name":"account/user_profile.html"}, name="password_change_done"),
    
    ##密码重置
	#url(r'^password-reset/$', auth_views.password_reset,{
    #                            "template_name":"account/password_reset_form.html",
    #                            "email_template_name":"account/password_reset_email.html",
    #                            "subject_template_name":"account/password_reset_subject.txt",
    #                            "post_reset_redirect":"/account/password-reset-done/"}, name="password_reset"),
	#url(r'^password-reset-done/$', auth_views.password_reset_done,{
    #                            "template_name":"account/password_reset_done.html"}, name="password_reset_done"),
	#url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,{
    #                            "post_reset_redirect":"/account/password-reset-complete/",
    #                            "template_name":"account/password_reset_confirm.html",}, name="password_reset_confirm"),
	#url(r'^password-reset-complete/$', auth_views.password_reset_complete, {
    #                             "template_name":"account/password_reset_complete.html"}, name="password_reset_complete"),
]
