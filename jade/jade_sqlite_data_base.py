#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : jade_sqlite_data_base.py
# @Author   : jade
# @Date     : 2021/11/27 15:57
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import sqlite3
import threading
import os
class JadeSqliteDataBase(object):
    def __init__(self,root_path,db_name,talbe_name, JadeLog=None):
        if os.path.exists(root_path) is False:
            os.mkdir(root_path)
        self._db_name = os.path.join(root_path, db_name)
        self.table_name = talbe_name
        self.JadeLog = JadeLog
        self.lock = threading.Lock()
        # 使用cursor()方法获取操作游标,连接数据库
        self.db = sqlite3.connect(self._db_name, check_same_thread=False)
        self.cursor = self.db.cursor()
        self.log("#" * 30 + "{}数据库连接成功".format(talbe_name) + "#" * 30,LEVEL="DEBUG")
        super(JadeSqliteDataBase, self).__init__()

    def create_table(self, sql_str):
        try:
            if type(sql_str) == str:
                self.cursor.execute(sql_str)
            elif type(sql_str) == dict:
                self.create_table_by_dic(sql_str)
        except:
            pass

    def create_table_by_dic(self, table_config):
        """:parameter
        table_name:表名
        table_config:dict
        """
        try:
            key_str_list = []
            for key in table_config:
                key_str_list.append(key + " " + table_config[key])
            sql_str = (
                "CREATE TABLE {} ({})".format(
                    self.table_name,",".join(key_str_list)
                )
            )
            self.cursor.execute(sql_str)
        except Exception as e:
            if "exists" in str(e):
                pass
            else:
                self.log("创建表失败,失败原因为{}".format(e))

    def log(self,str,LEVEL="ERROR"):
        if self.JadeLog:
            if LEVEL == "DEBUG":
                self.JadeLog.DEBUG(str)
            elif LEVEL == "INFO":
                self.JadeLog.INFO(str)
            elif LEVEL == "WARNING":
                self.JadeLog.WARNING(str)
            elif LEVEL == "ERROR":
                self.JadeLog.ERROR(str)
        else:
            print(str)

    def base_query(self,sql):
        try:
            try:
                self.lock.acquire(True)
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            finally:
                self.lock.release()
        except Exception as e:
            self.log("查询数据库失败,失败原因为:{},sql语句为:{}".format(e,sql),LEVEL="ERROR")

    def base_update(self,sql):
        try:
            try:
                self.lock.acquire(True)
                self.cursor.execute(sql)
                self.db.commit()
            finally:
                self.lock.release()
        except Exception as e:
            self.log("更新数据库失败,失败原因为:{},sql语句为:{}".format(e,sql),LEVEL="ERROR")

    def base_delete(self,sql):
        try:
            try:
                self.lock.acquire(True)
                self.cursor.execute(sql)
                self.db.commit()
                self.cursor.execute("VACUUM")
                self.db.commit()
            finally:
                self.lock.release()
        except Exception as e:
            self.log("删除表失败,失败原因为:{},sql语句为:{}".format(e, sql),LEVEL="ERROR")

    def judgement_value_type(self,value):
        if type(value) == bool:
            return int(value)
        elif type(value) == int:
            return value
        elif type(value) == str or value == None:
            return "'{}'".format(value)
        else:
            return value

    def insert(self, data):
        """:插入一条数据
        data:插入的数据
        """
        sql_str = "INSERT OR IGNORE    INTO {} (".format(self.table_name)
        for data_key in data.keys():
            sql_str = sql_str + data_key + ","

        sql_str = sql_str[:-1] + ") VALUES ("
        for data_key in data.keys():
            sql_str = sql_str + "{}".format(self.judgement_value_type(data[data_key])) + ","
        sql_str = sql_str[:-1] + ")"
        self.base_update(sql_str)

    def query(self, start_time, end_time):
        """:查询所有的数据
        return:表单
        """
        sql_str = "SELECT * FROM {} where  rec_date >'{}' and rec_date<'{}'".format(self.table_name, start_time,end_time)
        return self.base_query(sql_str)


    def clear(self):
        sql_str = "DELETE FROM {}".format(self.table_name)
        self.base_delete(sql_str)

