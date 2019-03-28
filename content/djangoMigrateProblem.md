Title: Migrate problem when replace the db.sqlite3 file
Category: Django
Tags: Django, Migrate
Authors: zqlai


##从其他开发人员拷贝一个db.sqlite3文件，覆盖本地文件
```
python manage.py makemigrations
```
报错
```
sqlite3.OperationalError: table "django_admin_log" already exists

```
估计是靠过来的db.sqlite3文件中已经有django_admin_log表，但是django_migrations 表中没有记录本地的migration脚本，所以导致再建一次表，报错

```
python manage.py migrate easydict
```

单独迁移easydict，希望不会再迁移其他app，但还是报错
```
root@X250:~/118/yiji.git# python manage.py migrate easydict
Operations to perform:
Apply all migrations: easydict
Running migrations:
Applying auth.0002_auto_20181008_1626...Traceback (most recent call last):
File "/usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/utils.py", line 83, in _execute
return self.cursor.execute(sql)
File "/usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/sqlite3/base.py", line 294, in execute
return Database.Cursor.execute(self, query)
sqlite3.OperationalError: table "auth_group" already exists
```

看了一下migrate的帮助文档，有一个--fake-initial参数：
```
  --fake-initial        Detect if tables already exist and fake-apply initial
                        migrations if so. Make sure that the current database
                        schema matches your initial migration before using
                        this flag. Django will only check for an existing
                        table name.

```

意思似乎是现有的表不迁移，所以执行：
```
python manage.py migrate --fake-initial
root@X250:~/118/yiji.git# python manage.py migrate --fake-initial
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, easyadmin, easydict, sessions
  Running migrations:
    Applying admin.0002_logentry... FAKED
    Applying admin.0003_logentry_user... FAKED
    Applying auth.0002_auto_20181008_1626... FAKED
    Applying auth.0003_auto_20181020_0345... OK
    Applying auth.0004_auto_20181028_2319... OK
    Applying easyadmin.0001_initial... OK

ValueError: Related model 'easydict.User' cannot be resolved

```
好了，终于看到这个错误了！！

单独迁移easydict试试：

```
root@X250:~/118/yiji.git# python manage.py migrate easydict
Operations to perform:
  Apply all migrations: easydict
  Traceback (most recent call last):
    File "manage.py", line 22, in <module>

ValueError: The field admin.LogEntry.user was declared with a lazy reference to 'easydict.user', but app 'easydict' isn't installed.
```

* 试了好多方法，还是这个错误，最好暴力。。。
```
root@X250:~/118/yiji.git# rm easydict/migrations/ -r
root@X250:~/118/yiji.git# python manage.py makemigrations easydict 
Migrations for 'easydict':
  easydict/migrations/0001_initial.py
      - Create model User
      - Create model ClassInSchool
      - Create model course_level0_table
      - Create model course_level1_table
      - Create model course_level2_table
      - Create model LearningRecord
      - Create model School
      - Create model UserAct
      - Create model Word
      - Add field word to learningrecord
      - Add field school to classinschool
      - Add field classInSchool to user
      - Add field groups to user
      - Add field school to user
      - Add field user_permissions to user
```

似乎ok了

启动网站，打开http://127.0.0.1:8000/admin/easydict/school/，报错：
```
no such column: easydict_school.telephone
```

奇怪了，难道是数据库的easydict一直没有成功吗？打开dbshell，看一下easydict.school的定义：
```
sqlite> select * from sqlite_master where type='table' and name='easydict_school';
table|easydict_school|easydict_school|28|CREATE TABLE "easydict_school" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL, "address" varchar(200) NOT NULL, "telphone" varchar(20) NOT NULL, "Fax" varchar(20) NOT NULL, "website" varchar(100) NOT NULL, "description" varchar(100) NOT NULL, "manager_id" integer NOT NULL REFERENCES "easydict_user" ("id") DEFERRABLE INITIALLY DEFERRED)
```
果然，还是telphone，少了一个'e'

但是easydict/migrations/0001_initial里的定义是没错的

##似乎找到一个问题, easydict 一直没有迁移成功
也就是说，之前easydict/migrations下有好多脚本，到了0006，包含了model更新的记录，删掉之后重新makemigrations生成的脚本也没有作用到数据库中.
什么原因？

查看数据库中django_migrations表：
```
sqlite> select * from django_migrations;
1|contenttypes|0001_initial|2018-10-28 16:18:49.518411
2|contenttypes|0002_remove_content_type_name|2018-10-28 16:18:49.546412
3|auth|0001_initial|2018-10-28 16:18:49.573414
4|auth|0002_alter_permission_name_max_length|2018-10-28 16:18:49.590415
5|auth|0003_alter_user_email_max_length|2018-10-28 16:18:49.601416
6|auth|0004_alter_user_username_opts|2018-10-28 16:18:49.614416
7|auth|0005_alter_user_last_login_null|2018-10-28 16:18:49.625417
8|auth|0006_require_contenttypes_0002|2018-10-28 16:18:49.629417
9|auth|0007_alter_validators_add_error_messages|2018-10-28 16:18:49.642418
10|auth|0008_alter_user_username_max_length|2018-10-28 16:18:49.653419
11|auth|0009_alter_user_last_name_max_length|2018-10-28 16:18:49.665419
12|easydict|0001_initial|2018-10-28 16:18:49.831429
13|admin|0001_initial|2018-10-28 16:18:49.857430
14|admin|0002_logentry_remove_auto_add|2018-10-28 16:18:49.884432
15|sessions|0001_initial|2018-10-28 16:18:49.897433
16|admin|0002_logentry|2018-11-03 13:24:52.145426
17|admin|0003_logentry_user|2018-11-03 13:24:52.163519
18|auth|0002_auto_20181008_1626|2018-11-03 13:24:52.197976
19|auth|0003_auto_20181020_0345|2018-11-03 13:24:52.211341
20|auth|0004_auto_20181028_2319|2018-11-03 13:24:52.223982
21|easyadmin|0001_initial|2018-11-03 13:24:52.237841
22|easyadmin|0002_charge_manageractlog|2018-11-03 13:35:25.042510
23|sessions|0002_auto_20181008_1626|2018-11-03 13:35:25.055024
24|easydict|0002_auto_20181103_1342|2018-11-03 14:06:10.146670

```
也就是说，这里记录了easydict/0001_initial已经迁移过了，在migrate的时候，新makemigrations生成的0001_initial是不会执行的。

怎么解决，删掉这条记录？
```
root@X250:~/118/yiji.git# python manage.py migrate easydict
Traceback (most recent call last):
     django.db.migrations.exceptions.InconsistentMigrationHistory: Migration easydict.0002_auto_20181103_1342 is applied before its dependency easydict.0001_initial on database 'default'.
```
还不行，删掉整个表数据。
然后，
```
root@X250:~/118/yiji.git# python manage.py migrate easydict
Operations to perform:
  Apply all migrations: easydict
  Running migrations:
  Applying contenttypes.0001_initial...Traceback (most recent call last):
  File "/usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/utils.py", line 83, in _execute
  return self.cursor.execute(sql)
  File "/usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/sqlite3/base.py", line 294, in execute
  return Database.Cursor.execute(self, query)
    sqlite3.OperationalError: table "django_content_type" already exists

```

好吧，再来：
```
root@X250:~/118/yiji.git# python manage.py migrate easydict --fake-initial
Operations to perform:
  Apply all migrations: easydict
  Running migrations:
  Applying contenttypes.0001_initial... FAKED
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_auto_20181008_1626... FAKED
  Applying auth.0003_auto_20181020_0345... OK
  Applying auth.0004_auto_20181028_2319... OK
  Applying easydict.0001_initial... FAKED
  Applying easydict.0002_auto_20181103_1342... OK

```

好了，easydict总算迁移成功。...


** 为什么migrate easydict 还会迁移auth和contecttypes呢？

可能是依赖关系导致.


##等等， easydict.0001_initial是`FAKED`，也就是没有真的迁移？！
去数据库查，果真没有更新，折腾半天都是瞎折腾。。。
试试：
```
root@X250:~/118/yiji.git# python manage.py migrate easydict
....

django.db.utils.OperationalError: table "easydict_user" already exists

```
总结一下：`数据库已经有一个easydict_user表了，如我我们想更新这个表的定义，同时又想保留其数据，一种方法是手动修改数据库各字段定义，比如使用dbshell工具；二种方法是，使用Django的migrate机制，保留每次makemigrations产生的脚本，这样你migrate的时候就可以只更新你修改的部分，也就是要保留这个migrations脚本文件，不然就得自己写。如果不保留这个migrations脚本，每次都删掉重新makemigrations，那么Django会认为，你是要重建一个表，那就与数据库中现有的表冲突了`



