Documentation
=============

## Introduction

cloudmesh.emr allows cloudmesh users to easily iteract with Amazon's Elastic Map Reduce services with a particular focus
on using Apache Spark. Users are able to manage the entire lifecycle of Apache Spark clusters from the commandline, 
including uploading data and files to the cluster, launching the analysis, and checking in on the status of tasks and 
clusters. The goal of cloudmesh.emr is to abstract away a lot of the details of launching and managing a cluster by 
including commonsense defaults while allowing the user the flexibility to specify different options, if needed.

## Installation

cloudmesh.emr is best installed via git and pip as follows:

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
available [here](https://docs.aws.amazon.com/general/latest/gr/rande.html). Once these keys are provided, cloudmesh.emr
will be able to authenticate with the correct account and region and begin managing your EMR resources.

## Commandline Usage

cloudmesh.emr provides a simple way for users to manage AWS EMR clusters.

### list

The list subcommand provides high level details of clusters, instances, and steps (tasks). It allows the user to quickly
examine all available clusters and nodes and to monitor their status. Keep in mind that cloudmesh only has access to the
resources associated with the AWS Access ID and Secret Key provided in the configuration file.

```bash
$ cms emr list clusters [--status=STATUS...] [--format=FORMAT]
$ cms emr list instances CLUSTERID [--status=STATUS...] [--type=TYPE...] [--format=FORMAT]
$ cms emr list steps CLUSTERID [--state=STATE...] [--format=FORMAT]
```

Valid options for the --format argument are: `table` (default), `csv`, `json`, `yaml`, and `dict`. The `table` option will print 
a formatted table to the terminal while `dict` option will print a raw dictionary. The `csv`, `json`, and `yaml`
options will save the output to the specified file format.

Valid options for the --status flag when listing clusters are: `all` (default), `start`, `boot`, `run`, `wait`,
`terminating`, `shutdown`, and `error`. This option may be repeated multiple times to list a union of clusters in a
particular status. For example, `--status=start --status=boot` will list all clusters that are either booting or 
starting. If the `all` flag is present, all clusters will be listed regardless of other flags present. 

When viewing instances, the --status flag allows for: `all` (default), `start`, `provision`, `run`, and `down`. Like
above, the `all` option will supercede all other status flags included in the command. Otherwise, multiple status flags
may be included in order to view the union of those statuses.  

The --type flag in the list instances command accepts: `all`, `master`, `core`, and `task`. A master node manages core
and tasks nodes. Task nodes are unique in that they only provide worker threads to Spark and do not count as individual
data nodes. See the description
[here](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-master-core-task-nodes.html).

Finally, for the --state flag when viewing tasks, the following options are allowed: `all` (default), `pending`,
`canceling`, `running`, `completed`, `cancelled`, `failed`, `interrupted`.

### describe




### stop

### start

### upload

### copy

### run

            emr describe CLUSTERID
                Describes a cluster. Lists its status, region, type, etc.
            emr stop CLUSTERID
                Stops a cluster. Once a shutdown is initiated, it cannot be undone.
            emr start NAME [--master=MASTER] [--node=NODE] [--count=COUNT]
                Starts a cluster with a given name, number of servers, and server type. Bootstraps with Hadoop and Spark.
            emr copy BUCKET BUCKETNAME
                Copy a file from S3 to the cluster's master node.
            emr run CLUSTERID BUCKET BUCKETNAME
                Submit a spark application stored in an S3 bucket to the spark cluster.

## OpenAPI
