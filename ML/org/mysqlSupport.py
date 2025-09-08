import MySQLdb
from MySQLdb.cursors import DictCursor
def initmysql():
    map = {}
    with open("application.properties","r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            key, value = line.split('=', 1)  # 使用1作为split的第二个参数，确保只分割第一个等号
            key = key.strip()
            value = value.strip()
            map[key]=value
                ## 查询数据库
    return map

def getmysql(sql:str):
    map = initmysql()
    mysqluser = map['mysqluser']
    mysqlpass = map['mysqlpass']
    mysqldb = map['mysqldb']
    connhost = map['connhost']
    print("sql:"+sql)
    conn = MySQLdb.connect(host=connhost, user=mysqluser, password=mysqlpass, db=mysqldb, charset='utf8',cursorclass=DictCursor)
    cursor = conn.cursor()
    try:
        # 使用execute方法执行SQL语句
        cursor.execute(sql)
        ## 数据库所表说有行记录
        results = cursor.fetchall()
        list = [row for row in results]
    except MySQLdb.Error as e:
        print(e)
    return list


def updatemysql(sql:str):
    map = initmysql()
    mysqluser = map['mysqluser']
    mysqlpass = map['mysqlpass']
    mysqldb = map['mysqldb']
    connhost = map['connhost']
    print("sql:"+sql)
    conn = MySQLdb.connect(connhost, mysqluser, mysqlpass, mysqldb, charset='utf8')
    cursor = conn.cursor()
    row = 0
    try:
        # 使用execute方法执行SQL语句
        row = cursor.execute(sql)
        conn.commit()
    except MySQLdb.Error as e:
        print(e)
    return row


## http://127.0.0.1/com.testController!insertmysql?name=张三&age=13&table=user  必须要传table
def insertmysql(dictmap:dict):
    table = dictmap.pop('table')  # 删除'age'键并返回其值
    # 动态生成keys和values
    keys = ','.join(dictmap.keys())
    values = tuple(dictmap.values())
    # 使用参数化查询防止SQL注入 拼接占位符
    placeholders = ', '.join(['%s'] * len(dictmap))
    sql = f"insert into {table}({keys}) values ({placeholders})"

    map = initmysql()
    mysqluser = map['mysqluser']
    mysqlpass = map['mysqlpass']
    mysqldb = map['mysqldb']
    connhost = map['connhost']

    conn = MySQLdb.connect(connhost, mysqluser, mysqlpass, mysqldb, charset='utf8')
    cursor = conn.cursor()
    row = 0
    try:
        # 使用execute方法执行SQL语句
        print(sql)
        print(dictmap.values())
        row = cursor.execute(sql,values)
        conn.commit()
    except MySQLdb.Error as e:
        print(e)
    return row