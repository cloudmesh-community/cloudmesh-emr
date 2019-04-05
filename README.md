Documentation
=============

## Introduction

cloudmesh.emr allows cloudmesh users to easily iteract with Amazon's Elastic Map
Reduce services with a particular focus on using Apache Spark. Users are able to
manage the entire lifecycle of Apache Spark clusters from the commandline,
including uploading data and files to the cluster, launching the analysis, and
checking in on the status of tasks and clusters. The goal of cloudmesh.emr is to
abstract away a lot of the details of launching and managing a cluster by
including commonsense defaults while allowing the user the flexibility to
specify different options, if needed.

## Installation

cloudmesh.emr is best installed via git as follows:

```bash
$ git clone https://github.com/cloudmesh-community/cloudmesh.emr.git
$ cd cloudmesh.emr
$ pip install -e .
```

The only external library required is boto3, which should automatically be
installed by pip. Once the package is installed, the cloudmesh4.yaml file
requires the following keys to be filled out by the enduser:



## Commandline Usage

cloudmesh.emr provides functions to manage AWS EMR clusters. Their usage is described below.

### list

The list subcommand provides high level details of clusters, instances, and steps (tasks). It
allows the user to quickly examine all available clusters and nodes and to monitor thier status.

To list clusters associated with the AWS account, use:

```bash
$ cms emr list clusters [--status=STATUS...] [--format=FORMAT]
```




### describe

### stop

### start

### upload

### copy

### run

## OpenAPI
