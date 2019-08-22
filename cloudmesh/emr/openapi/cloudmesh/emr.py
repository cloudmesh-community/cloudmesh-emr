from __future__ import print_function
from cloudmesh.emr.api.manager import Manager


def start():
    pass


def get_list_from_arg(arg, valid):
    """
    Helper function to that validates a list against a valid set.
    :param arg: A string to compare against valid.
    :param valid: A list of valid values.
    :return: list of validated values.
    """
    arg_split = arg.split(",")

    if 'all' in arg_split:
        return ['all']
    else:
        result = []

        for arg in arg_split:
            if arg in valid:
                result += [arg]
        return result


def list_clusters(status='all'):
    """
    Lists the clusters associated with the Amazon credentials in the cloudmesh.yaml file.
    :param status: Filters clusters by the given status.
    :return: dictionary of associated clusters.
    """
    emr = Manager()

    val_state = ['start', 'boot', 'run', 'wait', 'terminating', 'shutdown', 'error', 'all']
    states = get_list_from_arg(status, val_state)

    return emr.list_clusters({'status': states})[0]['data']


def list_instances(cluster, status='all', type='all'):
    """
    Lists the instances that are associated with a specific cluster.
    :param cluster: The cluster ID to list the instances of.
    :param status: List only instances with this status.
    :param type: List only instances of this type.
    :return: dictionary of instances.
    """
    emr = Manager()

    val_state = ['start', 'provision', 'boot', 'run', 'down']
    states = get_list_from_arg(status, val_state)

    val_type = ['master', 'core', 'task']
    types = get_list_from_arg(type, val_type)

    return emr.list_instances({'CLUSTERID': cluster, 'status': states, 'type': types})[0]['data']


def list_steps(cluster, status='all'):
    """
    Lists the steps a cluster is performing.
    :param cluster: The cluster ID to list the steps of.
    :param status: List only steps of this type.
    :return: dictionary of steps.
    """
    emr = Manager()

    val_state = ['pending', 'canceling', 'running', 'completed', 'cancelled', 'failed', 'interrupted']
    states = get_list_from_arg(status, val_state)

    return emr.list_steps({'CLUSTERID': cluster, 'state': states})[0]['data']


def describe(cluster):
    """
    Describes a specific cluster.
    :param cluster: The cluster ID to describe.
    :return: A dictionary of cluster details.
    """
    emr = Manager()

    return emr.describe_cluster({'CLUSTERID': cluster})[0]['data']


def stop(cluster):
    """
    Stops the given cluster.
    :param cluster: The cluster ID to stop.
    :return: a dictionary with the cluster that was stopped.
    """
    emr = Manager()

    return emr.stop_cluster({'CLUSTERID': cluster})[0]['data']


def start(name, master='m3.xlarge', node='m3.xlarge', count=3):
    """
    Starts a new cluster.
    :param name: The name to give the cluster.
    :param master: The server type to use for the master node. 
    :param node: The server type to use for the worker nodes.
    :param count: How many servers to start up.
    :return: A dictionary with the cluster that was created.
    """
    emr = Manager()

    return emr.start_cluster({'NAME': name, 'master': master, 'node': node, 'count': count})[0]['data']


def upload(file, bucket, bucketname):
    """
    Uploads a file from the local computer to an S3 bucket.
    :param file: The local (to the server) file to upload to an S3 bucket.
    :param bucket: The bucket to upload the file to.
    :param bucketname: The name to give to the file once it is uploaded.
    :return: A dictionary with the upload details.
    """
    emr = Manager()

    return emr.upload_file({'FILE': file, 'BUCKET': bucket, 'BUCKETNAME': bucketname})[0]['data']


def copy(cluster, bucket, bucketname):
    """
    Copies a file from S3 to the master node's /home/hadoop folder.
    :param cluster: The cluster ID to copy the file to.
    :param bucket: The S3 bucket to download the file from.
    :param bucketname: The name of the file in the S3 bucket to download.
    :return: A dictionary with the upload results.
    """
    emr = Manager()

    return emr.copy_file({'CLUSTERID': cluster, 'BUCKET': bucket, 'BUCKETNAME': bucketname})[0]['data']


def run(cluster, bucket, bucketname):
    """
    Runs a Spark Python file in an S3 bucket on the cluster.
    :param cluster: The cluster ID to run the given python file.
    :param bucket: The S3 bucket that hosts the python file to run.
    :param bucketname: The name of the python file to run.
    :return: A dictionary with the details of the cluster step created.
    """
    emr = Manager()

    return emr.run({'CLUSTERID': cluster, 'BUCKET': bucket, 'BUCKETNAME': bucketname})[0]['data']

