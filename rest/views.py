from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Member
from .serializer import MemberSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404,JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.


@api_view(['GET'])
def get_all_members(request,page,search_string):
    members = Member.objects.all().order_by('-name').filter(name__icontains=search_string)
    if search_string == "any":
        members = Member.objects.all().order_by('-chy_points')
    if len(members) == 0:
        return JsonResponse({
        "members": [{"id": 0,
            "name": "N/A",
            "chy_points": "N/A",
            "cycles": "N/A",
            "countdown": "N/A",
            "vip": "N/A",
            "last_scrapped":"N/A",
            "user_name": "N/A",
            "password": "N/A"}]
        })
    serializer = MemberSerializer(members,many=True)
    paginator = Paginator(serializer.data,10)
    total = paginator.num_pages

    if int(page) > total :
        return JsonResponse({"msg":"Empty page error"},status=412)


    response = {"members" : paginator.page(page).object_list, "total_no_pages":total}
    return JsonResponse(response)
        




@api_view(['POST'])
def create_member(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save() 
        return Response(serializer.data)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ModifyMember(APIView):

    def get_object(self,pk):
        try:
            return Member.objects.get(name=pk)
        except Member.DoesNotExist:
            raise Http404
    
    def get(self,request,pk,format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        member = self.get_object(pk)
        serializer = MemberSerializer(member)
        member.delete()
        return Response(serializer.data)

