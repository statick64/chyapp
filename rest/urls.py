from django.urls import path
from . import views
from .views import ModifyMember

urlpatterns = [
    path("get_members",views.get_all_members,name="get-all-members"),
    path("get_mems",views.get_all_mems,name="get-all-members"),
    path("create_member",views.create_member,name="create-member"),
    path("modify_member/<str:pk>",ModifyMember.as_view(),name="modify-member"),
]

