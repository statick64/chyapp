from django.urls import path
from . import views
from .views import ModifyMember

urlpatterns = [
    path("get_members/<str:page>/<str:search_string>",views.get_all_members,name="get-all-members"),
    path("create_member",views.create_member,name="create-member"),
    path("modify_member/<str:pk>",ModifyMember.as_view(),name="modify-member"),
]

