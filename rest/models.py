from django.db import models
from datetime import datetime
import pandas as pd

# Create your models here.

date = datetime(2020,12,20,8,34,8,8)

class Member(models.Model):
    name = models.CharField(max_length=50,default="user")
    chy_points = models.CharField(max_length=50,default="0")
    cycles = models.CharField(max_length=50,default="0")
    status = models.CharField(max_length=50,default="0")
    vip = models.CharField(max_length=50,default="0")
    user_name = models.CharField(max_length=50,default="user",unique=True)
    password = models.CharField(max_length=50,default="password")
    last_scrapped = models.CharField(max_length=50,default="unscrapped")
    consumption_points = models.CharField(max_length=50,default="unscrapped")


    @staticmethod
    def sort_members(param,member_list):
        member_df = pd.DataFrame(member_list)
        member_sorted = [member_df.sort_values(by=[param],ascending=False).to_dict(orient="index")]
        return member_sorted

