from  gridfs import  GridFS
from pymongo import MongoClient
client= MongoClient('mongodb://localhost:27017/')
db = client['ab']
g_client="噪声防治"
gfs = GridFS(db,collection=g_client)
file = open("C:/Users/MyPc/Pictures/Table.xls","rb")
args = {"content_type":"噪声防治","uploadDate":"2022-6-10","md5":"化工","name":"东方财富"}
gfs.put(file,filename="Table.xls",**args)
file.close()
pdf = gfs.find_one({"filename":"Table.xls"})


# from mongoengine import connect
# from mongoengine import Document, StringField, FileField
# db = connect('lis', host='localhost', port=27017)
#
# # 此处继承的是 mongoengine.Document
# class Animal(Document):
#     genus = StringField()
#     family = StringField()
#     photo = FileField()
# #     ,filename='600618   氯碱化工2014年半年报摘要.pdf'
# marmot = Animal(genus='name', family='Sciuridae')
# marmot_photo = open("C:/Users/MyPc/Pictures/Table.xls","rb")
# marmot.photo.put(marmot_photo, filename='600618   氯碱化工2014年半年报摘要.pdf',contentType='application/pdf')
# import gridfs
# import pymongo
# import time
# import datetime
#
# from gridfs import *
#
#
# class DBConn(object):
#     '''
#     127.0.0.1  -> 你的monogo的服务器地址
#     27017      -> 你的monogo的端口
#     root       -> 你的monogo的用户名
#     password   -> 你的monogo的密码
#     '''
#     server = 'mongodb://localhost:27017/'
#
#     def connect(self):
#         # 创建mongo连接
#         self.conn = pymongo.MongoClient(self.server)
#
#     def close(self):
#         # 关闭mongo连接
#         return self.conn.disconnect()
#
#     def getConn(self):
#         # 获取mongo连接
#         return self.conn
#
#
# # class OperateGridFS(object):
# #     '''
# #         操作mongo的GridFS桶
# #         根据时间查询图片数据，并存储到本地
# #     '''
# #
# #     def __init__(self, inputDate):
# #         # 要过滤的时间范围
# #         self.inuptDate = inputDate
# #
# #     def findGridByQuery(self):
# #         # 获取数据库连接
# #         dbconn = DBConn()
# #         dbconn.connect()
# #         # 获取你要操作的库，这里的image 就是你看到的相当于mysql有一个image库 要结合截图理解
# #
# #         db = dbconn.getConn().lis
# #         # 获取你要操作的表，就是你看到的相当于mysql存在一个image库中，库中又有一张fs表 要结合截图理解
# #         fs = gridfs.GridFS(db, collection='fs')
# #         for grif_out in fs.find({"uploadDate": {"$gte": datetime.datetime.strptime(self.inuptDate, '%Y-%m-%d')}}):
# #             filename = grif_out.filename
# #             data = grif_out.read()
# #             # 存储图片的位置
# #             outf = open(r'C:\Users\MyPc\Pictures\Saved Pictures\{}'.format(filename), 'wb')
# #             outf.write(data)
# #             outf.close()
# #
# # if __name__ == '__main__':
# #     demo = OperateGridFS('2022-7-21')
# #     demo.findGridByQuery()