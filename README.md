Documentation
=============

## Introduction

cloudmesh.emr allows cloudmesh users to easily iteract with Amazon's Elastic Map Reduce services
with a particular focus on using Apache Spark. Users are able to manage the entire lifecycle of
Apache Spark clusters from the commandline, including uploading data and files to the cluster,
launching the analysis, and checking in on the status of tasks and clusters. The goal of
cloudmesh.emr is to abstract away a lot of the details of launching and managing a cluster
by including commonsense defaults while allowing the user the flexibility to specify different
options, if needed.

## Installation

cloudmesh.emr is best installed via git as follows:

```bash
$ git clone https://github.com/cloudmesh-community/cloudmesh.emr.git
$ cd cloudmesh.emr
$ pip install -e .
```

The only external library required is boto3, which should automatically be installed by pip.

## Commandline Usage

## OpenAPI
