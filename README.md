# Cloudmesh Elastic Map Reduce 

[![Version](https://img.shields.io/pypi/v/cloudmesh-emr.svg)](https://pypi.python.org/pypi/cloudmesh-emr)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cloudmesh/cloudmesh-emr/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/cloudmesh-emr.svg)](https://pypi.python.org/pypi/cloudmesh-emr)
[![Format](https://img.shields.io/pypi/format/cloudmesh-emr.svg)](https://pypi.python.org/pypi/cloudmesh-emr)
[![Status](https://img.shields.io/pypi/status/cloudmesh-emr.svg)](https://pypi.python.org/pypi/cloudmesh-emr)
[![Travis](https://travis-ci.com/cloudmesh/cloudmesh-emr.svg?branch=master)](https://travis-ci.com/cloudmesh/cloudmesh-emr)

## Introduction

cloudmesh-emr allows cloudmesh users to easily iteract with Amazon's Elastic Map Reduce services with a particular focus
on using Apache Spark. Users are able to manage the entire lifecycle of Apache Spark clusters from the commandline, 
including uploading data and files to the cluster, launching the analysis, and checking in on the status of tasks and 
clusters. The goal of cloudmesh-emr is to abstract away a lot of the details of launching and managing a cluster by 
including commonsense defaults while allowing the user the flexibility to specify different options, if needed.

## Installation

cloudmesh-emr can either be installed via pip or, for advanced users wanting to use the development versions, via git:

### Install via pip

```bash
$ pip install cloudmesh-cmd5
$ pip install cloudmesh-sys
$ pip install cloudmesh-cloud
$ pip install cloudmesh-emr
```


### Developer Install

```bash
$ git clone https://github.com/cloudmesh/cloudmesh-emr.git
$ cd cloudmesh-emr
$ pip install -e .
```

The only external library required is boto3, which should automatically be installed by pip. Once the package is 
installed, the plugin requires the following keys to be present in the cloudmesh4.yaml file available to Cloudmesh's 
configuration utility:

* cloudmesh.cloud.aws.credentials.EC2_ACCESS_ID
* cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY
* cloudmesh.cloud.aws.credentials.region

The first two values are provided when you create a user on your AWS account's IAM management console. The third one is 
user provided and must be a valid AWS region (e.g. us-west-1, eu-west-3, etc.). A full listing of AWS regions is 
available [here](https://docs.aws.amazon.com/general/latest/gr/rande.html). Once these keys are provided, cloudmesh-emr
will be able to authenticate with the correct account and region and begin managing your EMR resources.

Finally, before beginning use of cloudmesh-emr, one must start up the local MongoDB database as cloudmesh-emr stores the
results of each query into the cloudmesh collection. You can start MongoDB by using the following command:

```bash
$ cms admin mongo start
```

If Mongo has not been installed previously, you can install it via cloudmesh by utilizing the admin command:

```bash
$ cms admin mongo install
```

## Commandline Usage

cloudmesh-emr provides a simple way for users to manage AWS EMR clusters.

### list

The list subcommand provides high level details of clusters, instances, and steps (tasks). It allows the user to quickly
examine all available clusters and nodes and to monitor their status. Keep in mind that cloudmesh only has access to the
resources associated with the AWS Access ID and Secret Key provided in the configuration file.

```bash
$ cms emr list clusters [--status=STATUS...] [--format=FORMAT]
$ cms emr list instances CLUSTERID [--status=STATUS...] [--type=TYPE...] [--format=FORMAT]
$ cms emr list steps CLUSTERID [--state=STATE...] [--format=FORMAT]
```

Valid options for the `--format` argument are: `table` (default), `csv`, `json`, `yaml`, and `dict`. The `table` option
will print a formatted table to the terminal while `dict` option will print a raw dictionary. The `csv`, `json`, and
`yaml` options will save the output to the specified file format.

Valid options for the `--status` flag when listing clusters are: `all` (default), `start`, `boot`, `run`, `wait`,
`terminating`, `shutdown`, and `error`. This option may be repeated multiple times to list a union of clusters in a
particular status. For example, `--status=start --status=boot` will list all clusters that are either booting or 
starting. If the `all` flag is present, all clusters will be listed regardless of other flags present. 

When viewing instances, the `--status` flag allows for: `all` (default), `start`, `provision`, `run`, and `down`. Like
above, the `all` option will supersede all other status flags included in the command. Otherwise, multiple status flags
may be included in order to view the union of those statuses.  

The `--type` flag in the list instances command accepts: `all`, `master`, `core`, and `task`. A master node manages core
and tasks nodes. Task nodes are unique in that they only provide worker threads to Spark and do not count as individual
data nodes. See the description
[here](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-master-core-task-nodes.html).

Finally, for the `--state` flag when viewing tasks, the following options are allowed: `all` (default), `pending`,
`canceling`, `running`, `completed`, `cancelled`, `failed`, `interrupted`.

The `CLUSTERID` is the AWS cluster ID, usually provided in the format similar to 'j-XXXXXXXXXXXXX'.

### describe

The describe command queries AWS for key characteristics of a specified cluster. The command is used as follows:

```bash
$ cms emr describe CLUSTERID [--format=FORMAT]
```

The command will provide the cluster's state, location, type, hours, and what applications are installed on teh cluster 
(typically Hadoop and Spark for EMR). As with the list command, the `CLUSTERID` is the one created by AWS to identify
your cluster. The `--format` flag allows you to print the result table to the terminal; a CSV, YAML, or JSON file; or to
the terminal as a dictionary (useful for piping to other commands).

### start

The start command is the first step when beginning an analysis. It spins up a Spark cluster using AWS's EMR service and
configures it to run PySpark applications from an S3 bucket. The command the initiate startup is:

```bash
$ cms emr start NAME [--master=MASTER] [--node=NODE] [--count=COUNT]
```

Once cloudmesh has initiated cluster startup, it'll return the cluster ID given to it from AWS. While you can name a 
cluster to keep track of them, all interactions must be done using the cluster ID rather than the name. The options for
the command are:

`--master=MASTER` tells cloudmesh what instance type to use for the master node. For a Spark cluster, there is only one
master node. A list of available node types are available [here](https://aws.amazon.com/ec2/instance-types/). By 
default, cloudmesh will spin up one m3.xlarge instance for use as the master node. Typically, this can be downscaled 
slightly when compared to the worker nodes as it is solely responsible for coordinating nodes and does not participate
in the actual processing of data.

`--node=NODE` tells cloudmesh what instance type to use for the worker nodes. By default, cloudmesh will spin up 
m3.xlarge servers to use as the worker nodes. Since these nodes drive the analysis being run, it is worthwhile to 
consider upscaling these nodes, depending on budget and predicted workload (e.g. a server that costs twice as much is
worthwhile if it does the work in a quarter of the time). Since these nodes are using Spark, which keeps data in 
memory, it is better to use nodes with lots of high bandwidth memory rather than nodes with lots of disk space. 
Additional vCores are also worthwhile to extra compute power. **Imporant**: Do not use a server type with 1 vCore. 
Spark uses one core for the node's manager thread and then creates threads to occupy the other cores. If the server 
only provides one core, then there will be no free cores to create worker threads - you end up with a useless server 
that has one thread for management and zero threads to actually do the work, which will stall work being done.

Finally, the `--count=COUNT` flag tells how many servers to provision from AWS. With 1 node being reserved for the 
master node, `COUNT`-1 nodes will be created as worker nodes. Note that `--count=1` will create one master node and 0
worker nodes - meaning there will be no servers to do the actual work of the analysis.

### upload

The upload function provides the user with the ability to upload programs and data to an S3 bucket for use in the 
analysis. This is provided as a convenience and it is recommended that the user utilize the more formal methods of
uploading files and data to S3 via the [cloudmesh-storage](https://github.com/cloudmesh/cloudmesh-storage). To use this
function, simply provide the local filename, the destination S3 bucket associated with the account, and the filename
to store the file as in the S3 bucket:

```bash
$ cms emr upload FILE BUCKET BUCKETNAME
```

Programs uploaded to S3 can be invoked via the run command while data becomes directly accessible to the Spark cluster
by utilizing 'S3://' in the path to the file.

### copy

In unusual scenarios, support files may need to be copied from S3 to the servers themselves. This may improve 
performance as local IO is faster than reading from S3 - especially for repeated accesses. To copy a file from an S3
bucket to local, use:

```bash
$ cms emr copy BUCKET BUCKETNAME
```

By default, the file will be copied from the S3 bucket given and downloaded into the master node's /home/hadoop/ folder.

### run

The run command is the primary command of cloudmesh-emr. It calls `spark-submit` on the master node of the given cluster
and points it to the program file on an S3 bucket. Essentially, it is equivalent to typing in `spark-submit 
S3://BUCKET/BUCKETNAME` on the master node. You can invoke this command using:

```bash
$ cms emr run CLUSTERID BUCKET BUCKETNAME
```

As with the above, `CLUSTERID` refers to the AWS cluster ID and the `BUCKET` and `BUCKETNAME` arguments point to an 
S3 bucket and a file in that bucket that contain the program to be run. The program then runs as any normal Spark 
application and can use any and all Python and Spark functions normally available. For convenience, AWS allows users to
use the 'S3://' file path to directly access S3 buckets - saving users from having to manually handle extracting results
from the servers to a separate storage solution.

While programs are running, their status can be checked on via the `list steps` command.

### stop

As the name suggests, the stop command will initiate a shutdown of all instances associated with a cluster ID. The 
command is invoked as:

```bash
$ cms emr stop CLUSTERID
```

Once a cluster has initiated shutdown, all instances are released, attached storage is removed, and all pending or 
running tasks are stopped. This process is **irreversible**. The cluster ID will remain associated with your account
for approximately 30 days after the cluster is terminated, after which is will be removed.

## OpenAPI

Cloudmesh-emr also provides an OpenAPI specification that allows users to run the plugin as a REST service. The server
can be started by utilizing [cloudmesh-openapi](https://github.com/cloudmesh/cloudmesh-openapi). To invoke the server,
navigate to the OpenAPI folder in the cloudmesh-emr directory and use:

```bash
$ cms openapi server start ./emr.yaml
```

to start up the server on the default address and port. From there, users can access cloudmesh-emr's functionality via
REST service calls. The functions are available as:

```
http://localhost:8080/api/list_clusters
http://localhost:8080/api/list_instances
http://localhost:8080/api/list_steps
http://localhost:8080/api/describe
http://localhost:8080/api/stop
http://localhost:8080/api/start
http://localhost:8080/api/upload
http://localhost:8080/api/copy
http://localhost:8080/api/run
```

All of the options described in the previous section are available in the OpenAPI specification as arguments. For 
example, to list all worker instances associated with a cluster, the following URL can be visited:

`http://localhost:8080/api/list_instances?clusterid=j-XXXXXXXXXXX&type=core`

The only thing to consider when using the OpenAPI server is that `upload` will behave slightly differently than 
anticipated. When utilizing that part of the service, the `file` argument will be relative to the server, not the 
client making the request.

## References

[Cloudmesh cmd5](https://github.com/cloudmesh/cloudmesh-cmd5)

[Cloudmesh cloud](https://github.com/cloudmesh/cloudmesh-cloud)

[Cloudmesh sys](https://github.com/cloudmesh/cloudmesh-sys)
