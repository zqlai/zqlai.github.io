Title: resnet on horovod with multi GPUs
Category: ML
Tags: horovod, resnet
Authors: zqlai

```
2018-11-15 23:37:49.001918: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1490] Adding visible gpu devices: 1
2018-11-15 23:37:49.001953: I tensorflow/core/common_runtime/gpu/gpu_device.cc:971] Device interconnect StreamExecutor with strength 1 edge matrix:
2018-11-15 23:37:49.001960: I tensorflow/core/common_runtime/gpu/gpu_device.cc:977]      1 
2018-11-15 23:37:49.001965: I tensorflow/core/common_runtime/gpu/gpu_device.cc:990] 1:   N 
Traceback (most recent call last):
File "cifar10_main.py", line 274, in <module>
absl_app.run(main)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/absl/app.py", line 300, in run
_run_main(main, args)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/absl/app.py", line 251, in _run_main
sys.exit(main(argv))
File "cifar10_main.py", line 268, in main
run_cifar(flags.FLAGS)
File "cifar10_main.py", line 263, in run_cifar
shape=[_HEIGHT, _WIDTH, _NUM_CHANNELS])
File "/THL5/home/wql17/zqlai/models/official/resnet/resnet_run_loop.py", line 587, in resnet_main
max_steps=flags_obj.max_train_steps)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py", line 356, in train
loss = self._train_model(input_fn, hooks, saving_listeners)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py", line 1179, in _train_model
return self._train_model_distributed(input_fn, hooks, saving_listeners)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py", line 1326, in _train_model_distributed
saving_listeners)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/estimator/estimator.py", line 1406, in _train_with_estimator_spec
log_step_count_steps=self._config.log_step_count_steps) as mon_sess:
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 504, in MonitoredTrainingSession
stop_grace_period_secs=stop_grace_period_secs)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 921, in __init__
stop_grace_period_secs=stop_grace_period_secs)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 643, in __init__
self._sess = _RecoverableSession(self._coordinated_creator)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 1107, in __init__
_WrappedSession.__init__(self, self._create_session())
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 1112, in _create_session
return self._sess_creator.create_session()
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 800, in create_session
self.tf_sess = self._session_creator.create_session()
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/monitored_session.py", line 566, in create_session
init_fn=self._scaffold.init_fn)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/session_manager.py", line 281, in prepare_session
config=config)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/training/session_manager.py", line 184, in _restore_checkpoint
sess = session.Session(self._target, graph=self._graph, config=config)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/client/session.py", line 1511, in __init__
I1115 23:37:49.481643 47000205927040 tf_logging.py:115] Running local_init_op.
super(Session, self).__init__(target, graph, config=config)
File "/THL5/home/wql17/anaconda2/lib/python2.7/site-packages/tensorflow/python/client/session.py", line 634, in __init__
self._session = tf_session.TF_NewSessionRef(self._graph._c_graph, opts)
```

