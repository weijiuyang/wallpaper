import pymysql
# 创建连接
mydb = pymysql.connect(
    host="127.0.0.1",
    port=3306, 
    user='root', 
    passwd='vajors123',
    db='wallpaper')


girl_path = '/home/vajor/t7/girls'
girl_origin_path = '/home/vajor/t7/girls_origin'
girl_thumbnail_path = '/home/vajor/t7/girls_thumbnail'




