import MySQLdb
from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(
    ('117.17.187.180',4900),
    ssh_username="cloudera",
    ssh_password="cloudera",
    remote_bind_address=('117.17.187.180',3306)
)

server.start()
print('start complete')
print(server._remote_binds)
print(server.local_bind_host)# show assigned local port
# work with `SECRET SERVICE` through `server.local_bind_port`.
conn = MySQLdb.connect(host='127.0.0.1',
                       port=server.local_bind_port,
                       user='root',
                       passwd='cloudera',
                       db='mysql')
# config = {
#   'user': 'root',
#   'password': 'cloudera',
#   'host': '127.0.0.1',
#   'database': 'mysql',
# }

conn = MySQLdb.connect(conn)
conn.set_character_set('utf8')
cursor=conn.cursor()
print("process")
sql="select * from News;"
cursor.execute(sql)
conn.commit()



server.stop()