var tipuesearch = {"pages":[{"title":"About","text":"","tags":"pages","url":"/about.html","loc":"/about.html"},{"title":"Contact","text":"this is me","tags":"pages","url":"/contact.html","loc":"/contact.html"},{"title":"See the scence at 5:00am again","text":"Went to bed at 5:00am last night or, this morning Saw the dawn scene of Changsha again alone, not lonely tired, but exited fell into sleep with hope and prospect with more responsibilty for the engels by my side","tags":"life","url":"/blog/see-the-scence-at-500am-again.html","loc":"/blog/see-the-scence-at-500am-again.html"},{"title":"setting for ssh login without password input","text":"just two steps 1.generate key pairs if not exist ssh - keygen - t rsa If success, you will find id_rsa and id_rsa.pub in the ~/.ssh/ dir 2.copy the public key to the server you want to login ssh - copy - id username @hostname Then, it will authorize your permission by password. If both steps is done, you can ssh to the server without password input. In the ~/.ssh/authorized_key file on the server, you will find an entry like: sh - rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCpwXmBPQcLBDDZxUa18bLHoL0WrCRx9KR / 4 Dryyp4bbqq9877 / hYQCKq9Cxvjvo6pBkQB6DdykEHnJIVKhgGGt1y85L0IYTkazM8O4Q04sj / RhBvscf5fOdSedRu7UVzULVccBrm1 / uzfDZQnUgDUTrmGe3ynGVU0tjxwjXay5Xj7KZJmggGKR40bQ3eZAiXGbQSDSYaF9teT1aLh6z3Z0Z / 7 g7EtOwBWRrWoLlhgNiBF7uHi4FGlHxj2u9jcRTKzdI / rfTaVJZNyVuS7sSUqDl7fGyQ1XJq4AEKZg / wRuomKlme7aLl9Ee + 8 Lj +/ kpdEcRYNImJHV9CdTKYZXNIFZ XX @XX","tags":"Linux","url":"/blog/setting-for-ssh-login-without-password-input.html","loc":"/blog/setting-for-ssh-login-without-password-input.html"},{"title":"misc","text":"This is the content of my super blog post.","tags":"misc","url":"/blog/misc.html","loc":"/blog/misc.html"},{"title":"horovod on TH -1A works with mnist example","text":"step to launch the mnist training task 1. login the th-es-ln0 2. source zqlai/.bashrc 3.allocate 2 GPU nodes with 4 processes yhalloc - N2 - n4 - pTH_GPU 4.check the allocated job and responsive nodes yhq 5.load the task using mpirun cd horovod mpirun -np 4 -H gn6,gn7 python examples/tensorflow_mnist.py","tags":"note","url":"/blog/horovod works.html","loc":"/blog/horovod works.html"},{"title":"resnet on horovod with multi GPUs","text":"2018 - 11 - 15 23 : 37 : 49 . 001918 : I tensorflow / core / common_runtime / gpu / gpu_device . cc : 1490 ] Adding visible gpu devices : 1 2018 - 11 - 15 23 : 37 : 49 . 001953 : I tensorflow / core / common_runtime / gpu / gpu_device . cc : 971 ] Device interconnect StreamExecutor with strength 1 edge matrix : 2018 - 11 - 15 23 : 37 : 49 . 001960 : I tensorflow / core / common_runtime / gpu / gpu_device . cc : 977 ] 1 2018 - 11 - 15 23 : 37 : 49 . 001965 : I tensorflow / core / common_runtime / gpu / gpu_device . cc : 990 ] 1 : N Traceback ( most recent call last ) : File \" cifar10_main.py \" , line 274 , in < module > absl_app . run ( main ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/absl/app.py \" , line 300 , in run _run_main ( main , args ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/absl/app.py \" , line 251 , in _run_main sys . exit ( main ( argv )) File \" cifar10_main.py \" , line 268 , in main run_cifar ( flags . FLAGS ) File \" cifar10_main.py \" , line 263 , in run_cifar shape = [ _HEIGHT , _WIDTH , _NUM_CHANNELS ] ) File \" /THL5/home/wql17/zqlai/models/official/resnet/resnet_run_loop.py \" , line 587 , in resnet_main max_steps = flags_obj . max_train_steps ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py \" , line 356 , in train loss = self . _train_model ( input_fn , hooks , saving_listeners ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py \" , line 1179 , in _train_model return self . _train_model_distributed ( input_fn , hooks , saving_listeners ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py \" , line 1326 , in _train_model_distributed saving_listeners ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py \" , line 1406 , in _train_with_estimator_spec log_step_count_steps = self . _config . log_step_count_steps ) as mon_sess : File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py \" , line 504 , in MonitoredTrainingSession stop_grace_period_secs = stop_grace_period_secs ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py \" , line 921 , in __init__ stop_grace_period_secs = stop_grace_period_secs ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py \" , line 643 , in __init__ self . _sess = _RecoverableSession ( self . _coordinated_creator ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py \" , line 1107 , in __init__ _WrappedSession . __init__ ( self , self . _create_session ()) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py \" , line 1112 , in _create_session return self . _sess_creator . create_session () File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py \" , line 800 , in create_session self . tf_sess = self . _session_creator . create_session () File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py \" , line 566 , in create_session init_fn = self . _scaffold . init_fn ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/session_manager.py \" , line 281 , in prepare_session config = config ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/session_manager.py \" , line 184 , in _restore_checkpoint sess = session . Session ( self . _target , graph = self . _graph , config = config ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/client/session.py \" , line 1511 , in __init__ I1115 23 : 37 : 49 . 481643 47000205927040 tf_logging . py : 115 ] Running local_init_op . super ( Session , self ) . __init__ ( target , graph , config = config ) File \" /THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/client/session.py \" , line 634 , in __init__ self . _session = tf_session . TF_NewSessionRef ( self . _graph . _c_graph , opts )","tags":"ML","url":"/blog/resnet-on-horovod-with-multi-gpus.html","loc":"/blog/resnet-on-horovod-with-multi-gpus.html"},{"title":"Migrate problem when replace the db.sqlite3 file","text":"从其他开发人员拷贝一个db.sqlite3文件，覆盖本地文件 python manage . py makemigrations 报错 sqlite3 . OperationalError : table \"django_admin_log\" already exists 估计是靠过来的db.sqlite3文件中已经有django_admin_log表，但是django_migrations 表中没有记录本地的migration脚本，所以导致再建一次表，报错 python manage . py migrate easydict 单独迁移easydict，希望不会再迁移其他app，但还是报错 root @ X250 : ~/ 118 / yiji . git # python manage . py migrate easydict Operations to perform : Apply all migrations : easydict Running migrations : Applying auth . 0002 _auto_20181008_1626 ... Traceback ( most recent call last ) : File \" /usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/utils.py \" , line 83 , in _execute return self . cursor . execute ( sql ) File \" /usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/sqlite3/base.py \" , line 294 , in execute return Database . Cursor . execute ( self , query ) sqlite3 . OperationalError : table \" auth_group \" already exists 看了一下migrate的帮助文档，有一个—fake-initial参数： -- fake - initial Detect if tables already exist and fake - apply initial migrations if so . Make sure that the current database schema matches your initial migration before using this flag . Django will only check for an existing table name . 意思似乎是现有的表不迁移，所以执行： python manage . py migrate --fake-initial root @X250 : ~/ 118 / yiji . git # python manage . py migrate --fake-initial Operations to perform : Apply all migrations : admin , auth , contenttypes , easyadmin , easydict , sessions Running migrations : Applying admin .0002 _logentry ... FAKED Applying admin .0003 _logentry_user ... FAKED Applying auth .0002 _auto_20181008_1626 ... FAKED Applying auth .0003 _auto_20181020_0345 ... OK Applying auth .0004 _auto_20181028_2319 ... OK Applying easyadmin .0001 _initial ... OK ValueError : Related model 'easydict.User' cannot be resolved 好了，终于看到这个错误了！！ 单独迁移easydict试试： root @X250 : ~/ 118 / yiji . git # python manage . py migrate easydict Operations to perform : Apply all migrations : easydict Traceback ( most recent call last ) : File \"manage.py\" , line 22 , in < module > ValueError : The field admin . LogEntry . user was declared with a lazy reference to 'easydict.user' , but app 'easydict' isn ' t installed . 试了好多方法，还是这个错误，最好暴力。。。 root @ X250 : ~/ 118 / yiji . git # rm easydict / migrations / - r root @ X250 : ~/ 118 / yiji . git # python manage . py makemigrations easydict Migrations for ' easydict ' : easydict / migrations / 0001 _initial . py - Create model User - Create model ClassInSchool - Create model course_level0_table - Create model course_level1_table - Create model course_level2_table - Create model LearningRecord - Create model School - Create model UserAct - Create model Word - Add field word to learningrecord - Add field school to classinschool - Add field classInSchool to user - Add field groups to user - Add field school to user - Add field user_permissions to user 似乎ok了 启动网站，打开http://127.0.0.1:8000/admin/easydict/school/，报错： no such column : easydict_school . telephone 奇怪了，难道是数据库的easydict一直没有成功吗？打开dbshell，看一下easydict.school的定义： sqlite > select * from sqlite_master where type = 'table' and name = 'easydict_school' ; table | easydict_school | easydict_school | 28 | CREATE TABLE \"easydict_school\" ( \"id\" integer NOT NULL PRIMARY KEY AUTOINCREMENT , \"name\" varchar ( 100 ) NOT NULL , \"address\" varchar ( 200 ) NOT NULL , \"telphone\" varchar ( 20 ) NOT NULL , \"Fax\" varchar ( 20 ) NOT NULL , \"website\" varchar ( 100 ) NOT NULL , \"description\" varchar ( 100 ) NOT NULL , \"manager_id\" integer NOT NULL REFERENCES \"easydict_user\" ( \"id\" ) DEFERRABLE INITIALLY DEFERRED ) 果然，还是telphone，少了一个'e' 但是easydict/migrations/0001_initial里的定义是没错的 似乎找到一个问题, easydict 一直没有迁移成功 也就是说，之前easydict/migrations下有好多脚本，到了0006，包含了model更新的记录，删掉之后重新makemigrations生成的脚本也没有作用到数据库中. 什么原因？ 查看数据库中django_migrations表： sqlite > select * from django_migrations ; 1 | contenttypes | 0001 _initial | 2018 - 10 - 28 16 : 18 : 49 . 518411 2 | contenttypes | 0002 _remove_content_type_name | 2018 - 10 - 28 16 : 18 : 49 . 546412 3 | auth | 0001 _initial | 2018 - 10 - 28 16 : 18 : 49 . 573414 4 | auth | 0002 _alter_permission_name_max_length | 2018 - 10 - 28 16 : 18 : 49 . 590415 5 | auth | 0003 _alter_user_email_max_length | 2018 - 10 - 28 16 : 18 : 49 . 601416 6 | auth | 0004 _alter_user_username_opts | 2018 - 10 - 28 16 : 18 : 49 . 614416 7 | auth | 0005 _alter_user_last_login_null | 2018 - 10 - 28 16 : 18 : 49 . 625417 8 | auth | 0006 _require_contenttypes_0002 | 2018 - 10 - 28 16 : 18 : 49 . 629417 9 | auth | 0007 _alter_validators_add_error_messages | 2018 - 10 - 28 16 : 18 : 49 . 642418 10 | auth | 0008 _alter_user_username_max_length | 2018 - 10 - 28 16 : 18 : 49 . 653419 11 | auth | 0009 _alter_user_last_name_max_length | 2018 - 10 - 28 16 : 18 : 49 . 665419 12 | easydict | 0001 _initial | 2018 - 10 - 28 16 : 18 : 49 . 831429 13 | admin | 0001 _initial | 2018 - 10 - 28 16 : 18 : 49 . 857430 14 | admin | 0002 _logentry_remove_auto_add | 2018 - 10 - 28 16 : 18 : 49 . 884432 15 | sessions | 0001 _initial | 2018 - 10 - 28 16 : 18 : 49 . 897433 16 | admin | 0002 _logentry | 2018 - 11 - 03 13 : 24 : 52 . 145426 17 | admin | 0003 _logentry_user | 2018 - 11 - 03 13 : 24 : 52 . 163519 18 | auth | 0002 _auto_20181008_1626 | 2018 - 11 - 03 13 : 24 : 52 . 197976 19 | auth | 0003 _auto_20181020_0345 | 2018 - 11 - 03 13 : 24 : 52 . 211341 20 | auth | 0004 _auto_20181028_2319 | 2018 - 11 - 03 13 : 24 : 52 . 223982 21 | easyadmin | 0001 _initial | 2018 - 11 - 03 13 : 24 : 52 . 237841 22 | easyadmin | 0002 _charge_manageractlog | 2018 - 11 - 03 13 : 35 : 25 . 042510 23 | sessions | 0002 _auto_20181008_1626 | 2018 - 11 - 03 13 : 35 : 25 . 055024 24 | easydict | 0002 _auto_20181103_1342 | 2018 - 11 - 03 14 : 06 : 10 . 146670 也就是说，这里记录了easydict/0001_initial已经迁移过了，在migrate的时候，新makemigrations生成的0001_initial是不会执行的。 怎么解决，删掉这条记录？ root @X250 : ~/ 118 / yiji . git # python manage . py migrate easydict Traceback ( most recent call last ) : django . db . migrations . exceptions . InconsistentMigrationHistory : Migration easydict .0002 _auto_20181103_1342 is applied before its dependency easydict .0001 _initial on database 'default' . 还不行，删掉整个表数据。 然后， root @ X250 : ~/ 118 / yiji . git # python manage . py migrate easydict Operations to perform : Apply all migrations : easydict Running migrations : Applying contenttypes . 0001 _initial ... Traceback ( most recent call last ) : File \" /usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/utils.py \" , line 83 , in _execute return self . cursor . execute ( sql ) File \" /usr/local/lib/python3.6/dist-packages/Django-2.1.1-py3.6.egg/django/db/backends/sqlite3/base.py \" , line 294 , in execute return Database . Cursor . execute ( self , query ) sqlite3 . OperationalError : table \" django_content_type \" already exists 好吧，再来： root @X250 : ~/ 118 / yiji . git # python manage . py migrate easydict --fake-initial Operations to perform : Apply all migrations : easydict Running migrations : Applying contenttypes .0001 _initial ... FAKED Applying contenttypes .0002 _remove_content_type_name ... OK Applying auth .0001 _initial ... OK Applying auth .0002 _auto_20181008_1626 ... FAKED Applying auth .0003 _auto_20181020_0345 ... OK Applying auth .0004 _auto_20181028_2319 ... OK Applying easydict .0001 _initial ... FAKED Applying easydict .0002 _auto_20181103_1342 ... OK 好了，easydict总算迁移成功。… ** 为什么migrate easydict 还会迁移auth和contecttypes呢？ 可能是依赖关系导致. 等等， easydict.0001_initial是 FAKED ，也就是没有真的迁移？！ 去数据库查，果真没有更新，折腾半天都是瞎折腾。。。 试试： root @X250 : ~/ 118 / yiji . git # python manage . py migrate easydict .... django . db . utils . OperationalError : table \"easydict_user\" already exists 总结一下： 数据库已经有一个easydict_user表了，如我我们想更新这个表的定义，同时又想保留其数据，一种方法是手动修改数据库各字段定义，比如使用dbshell工具；二种方法是，使用Django的migrate机制，保留每次makemigrations产生的脚本，这样你migrate的时候就可以只更新你修改的部分，也就是要保留这个migrations脚本文件，不然就得自己写。如果不保留这个migrations脚本，每次都删掉重新makemigrations，那么Django会认为，你是要重建一个表，那就与数据库中现有的表冲突了","tags":"Django","url":"/blog/migrate-problem-when-replace-the-dbsqlite3-file.html","loc":"/blog/migrate-problem-when-replace-the-dbsqlite3-file.html"},{"title":"test post - how to set up django on ubuntu 18.04","text":"This is the content of my super blog post. title 2 item1 ** item2 *** item3 title 3 item1 ** item2 *** item3 title 4 item1 ** item2 *** item3 — test — — dassh empty item1 ** item2 *** item3","tags":"django","url":"/blog/my second post.html","loc":"/blog/my second post.html"},{"title":"build Django on Godady virtual host","text":"just get a Godady virtual host, WITHOUT pip tool, only python2.6 let's begin download source of python3.7.0 and unzip it cd python_source_dir . / configure make make install when make install , an error came out: from _ctypes import Union , Structure , Array ImportError : No module named '_ctypes' Googling it, seems that we need install libffi-dev, then download source and . / configure make make install DESTDIR =~/ software setup the LD_LIBRARY_PATH in the . bashrc and source it","tags":"life","url":"/blog/build-django-on-godady-virtual-host.html","loc":"/blog/build-django-on-godady-virtual-host.html"},{"title":"My super title","text":"This is the content of my super blog post. import time as t t . strftime () import time as t t . strftime () #include <lib.h> int main (){ }","tags":"Python","url":"/blog/my-super-title.html","loc":"/blog/my-super-title.html"}]};