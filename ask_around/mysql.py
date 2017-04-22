# -*- coding: utf-8 -*-
__author__ =  "olenji"
'''
    date    :2016-10-24 16:20
    function:   数据库插入
    py_version  : 2.7
'''

import json, sys,datetime, pymysql, pdb

class MysqlTool:
    
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',user = 'kst',password='kst410',
                db='kst', charset='utf8mb4')
        self.cur_query = self.connect.cursor()
        self.cur_unique_query = self.connect.cursor()
        self.cur_insert = self.connect.cursor()
        self.cur_update = self.connect.cursor()

    # +++++++++++++++++++ insert +++++++++++++++++
    def insertByDict(self, table, item):
        keys = list()
        values = list()
        for (k,v) in item.items():
            if v:
                keys.append(k)
                v = str(v) if isinstance(v, int) else '\"' + v + '\"'
                values.append(v)
        sql = "insert %s(%s) values(%s)" % ( table, ','.join(keys), ','.join(values))
        if self.cur_insert.execute(sql):
            return True
        else:
            print "error insert item"
            return False

    def uniqueInsertByDict(self, table, item ,unique_key):
        sql = "select * from %s where %s='%s'" % (table, unique_key, item[unique_key])
        if self.cur_unique_query.execute(sql):
            return False
        else:
            return self.insertByDict(table, item)

    def flush(self):
        self.cur_insert.close()
        a = self.connect.commit()
        self.cur_insert = self.connect.cursor()

    # ++++++++++++++++++++ query +++++++++++++++
    def queryAndFetchall(self, sql):
        self.cur_query.execute(sql)
        return self.cur_query.fetchall()


    #++++++++++++++ update ++++++++++++++
    def updateBySql(self, sql, save=False):
        pass


    #++++++++++++++  common ++++++++
    def commit(self):
        pass

    #+++++++++++++  test  ++++++++++
    def test_o(self):
        pass



    def __del__(self):
        self.cur_query.close()
        self.cur_unique_query.close()
        self.cur_insert.close()
        self.connect.commit()
        self.connect.close()

    
class JSONDataManager:

    conn = None
    cur = None
    def __init__(self):
        self.initConn()

    def __del__(self):
        self.closeConn()

    def initConn(self):
        if self.conn :
            print "连接存在"
            return
        else:
            print "connect..."
            #self.conn = MySQLdb.connect(host='56c1952d3edfa.gz.cdb.myqcloud.com',user='cdb_outerroot',passwd='quchu2015',db='scrapingdb',port=8426, charset='utf8')
            self.conn = MySQLdb.connect(host='56f214b4408fa.gz.cdb.myqcloud.com',user='cdb_outerroot',passwd='quchu2015',db='quchu',port=12020, charset='utf8')
            print "create cursor..."
            self.cur = self.conn.cursor()


    def closeConn(self):
        if self.cur:
            print "close cursor..."
            self.cur.close()
        if self.conn:
            self.conn.commit()
            print "close connection..."
            self.conn.close()

    #每次默认取1000条来输出
    #怕内容过大 内存不够
    def getRecord(self, sql, num = 1000):
        offset = 0
        length = num
        while length == num:
            limitsql = sql + " limit %d,%d" % (offset,num)
            print limitsql
            self.cur.execute(limitsql)
            results = self.cur.fetchall()
            length = len(results)
            for res in results:
                yield res
            offset += length

    def exe(self):
        querysql = "select id,name from place"
        self.cur.execute(querysql)
        placelist = self.cur.fetchall()
        start_index = 100
        now = datetime.datetime.now()
        nextcraltime = now +  datetime.timedelta(minutes=5)
        
        for place in placelist:
            placename = place[1].replace('\'','\\\'')
            insertsql = "insert into wechat_word values(%s,2,'%s','%s',800,'%s', now() )" %(start_index,placename,place[0],nextcraltime )
            start_index+=1
            nextcraltime += datetime.timedelta(seconds=1)
            print insertsql
            self.localcur.execute(insertsql)

    def temp(self):
        a = open("dp_categories.json",'r')
        tempstr = ""
        for line in a:
            tempstr += line.replace("\n",'')

        datas = json.loads(tempstr)
        for record in datas['categoryNavs']:
            insertsql = "insert into dp_categories values(%s , '%s', %s)" %(record['id'], record['name'].encode("utf8"),record['parentId'])
            #print insertsql
            self.cur.execute(insertsql)

        


    '''
        self.cursor.execute(sql)
        self.cursor.fetchone()
        self.cursor.fetchall()
        self.cursor.fetchmany()
        self.cursor.lastrowid
        self.cursor.statement
        self.cursor.with_rows
        self.column_names
    '''
        

'''
    def readFile(self, filename):
        temp = open(filename, 'r')
        for line in temp:
            jsonline = json.loads(line)
            if jsonline["entityId"] not in ["NULL", "Null", "null"]:
                yield jsonline


    def insertViewRecord(self,userid,placeid):
        tablename = "view_action"
        querySql = "select * from " + tablename + " where user_id = " + userid + \
            " and place_id = " + placeid
        temp = self.cur.execute(querySql)
        if temp :
            updateSql = "update %s set times=times+1 where user_id = %s and place_id = %s" % (tablename, userid, placeid )
            self.cur.execute(updateSql)
        else:
            insertSql = "insert into " + tablename + " (user_id, place_id, create_tm, last_tm) values (%s, %s, %s, %s )" % (userid, placeid,time.time(), time.time())
            self.cur.execute(insertSql) 

    def olenji(self,filename):
        for row in self.readFile(filename):
            if row['event'] and row['event'] == "view":
                self.insertViewRecord(row['entityId'], row['targetEntityId'])
        

    def olenjidir(self, floder):
        for f in os.listdir(floder):
            if re.search('action',f):
                self.olenji(floder + '/' + f)
'''
    
            
        
    
if __name__ == '__main__':
    mt = MysqlTool()
    item = {'aaa': 123,'bbb':'valueb','ccc':'valuec'}
    mt.insertByDict('taobao_items',item) 
    #b.olenji()
    #b.cur.execute("select product_id,latitude,longitude from sjs_yhouse where product_id in (18872,18934,18940,18943,18987,19003)")
    #print b.cur.fetchall()
