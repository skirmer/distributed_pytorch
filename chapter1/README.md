## Distributed Computing

* Mental model for understanding distributed computing

One computer: local machine, or single virtual machine
Cluster: multiple local or virtual machines connected and working together

Human interacts with one machine, and sends instructions/commands to the whole cluster
Distributed architecture works with storage (eg redshift or elasticsearch) or for computing (dask or spark)
Method for growing power/storage without making one big machine even bigger

* Overview of hardware

A datacenter could house a cluster of real machines that function as a distributed system
Cloud like EC2 can house real machines somewhere else for you

* Threads vs Cores vs CPUs vs GPUs

core: hardware vs thread: unit of work
CPU vs GPU: types of processor chip

* Why use cloud resources

cost - rent vs buy
"bursty" work

* Accessing a cluster

We'll look at the Saturn Cloud interface to see a way to do it
also talk about manual methods
