Title: horovod on TH-1A works with mnist example
Slug: horovod works
Tags: horovod TH-1A
Category: note
Authors: zqlai


## step to launch the mnist training task
* 1.
```bash
login the th-es-ln0
```
* 2.
```bash
source zqlai/.bashrc
```
* 3.allocate 2 GPU nodes with 4 processes
```
yhalloc -N2 -n4 -pTH_GPU
```
* 4.check the allocated job and responsive nodes
```
yhq
```
* 5.load the task using mpirun
```bash
cd horovod
mpirun -np 4 -H gn6,gn7 python examples/tensorflow_mnist.py
```


