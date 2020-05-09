import mysql
import mysql.connector
import redis

connect = mysql.connector.connect(host='base', user='root', password='1234', port = 3306, database='example_schema')
r = redis.Redis(host='redis', port=6379, db=0)
print("Введите Y для продолжения")
answer=input().lower()
create_table = """
CREATE TABLE IF NOT EXISTS users1 (userId INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name CHAR(25));
"""
insert_table="""INSERT INTO users1  (userId, name) VALUES (NULL, 'Andrei Kruglov'), (NULL, 'Dina Yakubovskaya'), (NULL, 'Sergey Marfenko'), (NULL, 'Ivan Ivanov'), (NULL, 'Yulia Isaeva');"""
query="""select * from users1 where userId"""
query1="""show columns from users1"""
truncate="""truncate table users1;"""
cursor0=connect.cursor()
cursor0.execute(truncate)
cursor0.execute(create_table)
cursor0.execute(insert_table)
cursor0.execute(query1)
dict=cursor0.fetchall()
print(dict)
while answer=="y":
    print("Введите знак")
    sign=input()
    print("Введите user_id")
    userId=input()
    if len(r.lrange(sign+userId, 0, -1))!=0:
        print("FROM REDIS: ")
        print(r.lrange(sign+userId, 0, -1))

    else:
            cursor=connect.cursor()
            cursor.execute(query+sign+userId)
            dict = cursor.fetchone()
            list = str(dict)
            print("FROM MYSQL: ")
            while dict is not None:
                r.rpush(sign+userId, list)
                r.expire(sign + userId, 20)
                print(list)
                dict = cursor.fetchone()
                list = str(dict)
    print("Введите Y для продолжения")
    answer = input().lower()