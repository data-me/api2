"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from datame.views import *
from authentication import views
from django.conf.urls import include, url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login', obtain_jwt_token),
    path('api/v1/refresh',refresh_jwt_token),
    url('api/v1/offer', Offer_view.as_view()),
    path('api/v1/company/offer/<offer_id>', Offer_view.as_view()),
    path('api/v1/apply', Apply_view.as_view()),
    path('api/v1/accept', AcceptApply_view.as_view(),name='accept apply'),
    path('api/v1/helloworld', views.HelloWorld.as_view()),
    path('api/v1/cv', CV_view.as_view()),
    path('api/v1/section_names', Section_name_view.as_view()),
    path('api/v1/message', Message_view.as_view(), name='mesagge'),
    path('api/v1/section', Section_view.as_view()),
    path('api/v1/section_name', Create_section_name.as_view()),
    path('api/v1/item', Item_view.as_view()),
    path('api/v1/company', Company_view.as_view()),
    path('api/v1/dataScientist', DataScientist_view.as_view()),
    path('api/v1/populate', populate),
    path('api/v1/whoami', whoami.as_view()),
    path('api/v1/register', Register_view.as_view()),
    path('api/v1/check_submition', Check_submition.as_view()),
    path('api/v1/submit', Submition_view.as_view()),
    path('api/v1/change_status', Change_status.as_view()),
    path('api/v2/admin/offers', Offer_admin_view.as_view()),
    path('api/v2/admin/delete_offer', Offer_admin_view.as_view()),
    path('api/v2/admin/delete_offer/<offer_id>', Offer_admin_view.as_view()),
    path('api/v1/users',User_view.as_view()),
    path('api/v1/companies',Companies_view.as_view()),
    path('api/v1/applicationsAccepted',ApplicationsAccepted_view.as_view()),
    path('api/v1/submitions',Submitions_view.as_view()),
    path('api/v1/messages',Messages_view.as_view()),
    path('api/v1/applications',Applications_view.as_view()),
    url(r'api/v1/pagos/', include('pagos.urls')),
    path('api/v2/currentUserPlan', currentUserPlan.as_view()),
    path('api/v2/userPlanHistory', userPlanHistory.as_view()),
    path('api/v2/payUserPlan', payUserPlan.as_view()),
    path('api/v2/list_dataScientists', list_dataScientists.as_view()),
    path('api/v2/list_companies', list_companies.as_view()),
    path('api/v2/list_companies', list_staff.as_view()),
    path('api/v2/delete_user', delete_user.as_view()),
    path('api/v2/get_user_logged', get_user_logged.as_view()),
    path('api/v2/change_info', change_info.as_view()),
    path('api/v2/change_offer/<offer_id>', change_Offer.as_view()),
    path('api/v2/data/delete_item/<item_id>', Item_delete_view.as_view()),
    path('api/v2/applicationsOfOffer/<offer_id>', ApplicationsOfOffer.as_view()),
    path('api/v2/application/<application_id>', Apply_v2_view.as_view()),
    path('api/v2/data/delete_section/<section_id>', Section_delete_view.as_view()),
]
