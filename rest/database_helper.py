import sqlite3
import psycopg2
import os

 



class MemberDB:
    def __init__(self,user_name,password,chy_points="0",cycles="0",vip="0",name="user",last_scraped="0",status="0", consumption_point= "0"):
        self.user_name = user_name
        self.password = password
        self.chy_points = chy_points
        self.status = status
        self.consumption_point = consumption_point
        self.cycles = cycles
        self.vip = vip
        self.name = name
        self.last_scraped = last_scraped
        


class DatabaseHelper:
    def __init__(self):
        # self.db = sqlite3.connect("../db.sqlite3")
        # self.c = self.db.cursor()
        # self.member = MemberDB("user","password")


        DATABASE_URL = os.environ['DATABASE_URL']
        # self.db = psycopg2.connect(DATABASE_URL,sslmode='require')
        self.db = psycopg2.connect(DATABASE_URL)
        self.c = self.db.cursor()
    



    def get_members_credentials(self):
        members_q = self.c.execute("""
        SELECT user_name, password
        FROM rest_member
        """
        ) 
        members_t = self.c.fetchall()
        members = [ MemberDB(x[0],x[1]) for x in members_t]
        return members
    def insert_member(self,member):
        try:
            self.c.execute("""
            UPDATE rest_member
            SET chy_points = %s,
            cycles =%s,
            vip = %s,
            status = %s,
            consumption_points = %s,
            last_scrapped = %s
            WHERE user_name = %s;
            """,
            (member.chy_points,member.cycles,member.vip,member.status,member.consumption_point,member.last_scraped,member.user_name))

        except Exception as e:
            print(str(e))
        self.db.commit()
    
    def auth_error(self,member):
        try:
            self.c.execute("""
            UPDATE rest_member
            SET chy_points = 'error !',
            cycles = 'error !',
            vip = 'error !',
            consumption_points = 'error !',
            status = 'error !'
            WHERE user_name = %s;
            """,
            (member.user_name,))
        except Exception as e:
            print(str(e))







        
    