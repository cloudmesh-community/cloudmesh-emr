from __future__ import print_function
from cloudmesh.emr.api.manager import Manager


def start():
    pass


def get_list_from_arg(arg, valid):
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
    emr = Manager()

    val_state = ['start', 'boot', 'run', 'wait', 'terminating', 'shutdown', 'error', 'all']
    states = get_list_from_arg(status, val_state)

    return emr.list_clusters({'status': states})


def list_instances(cluster, status='all', type='all'):
    emr = Manager()

    val_state = ['start', 'provision', 'boot', 'run', 'down']
    states = get_list_from_arg(status, val_state)

    val_type = ['master', 'core', 'task']
    types = get_list_from_arg(type, val_type)

    return emr.list_instances({'CLUSTERID': cluster, 'status': states, 'type': types})


def list_steps(cluster, status='all'):
    emr = Manager()

    val_state = ['pending', 'canceling', 'running', 'completed', 'cancelled', 'failed', 'interrupted']
    states = get_list_from_arg(status, val_state)

    return emr.list_steps({'CLUSTERID': cluster, 'state': states})


def describe(cluster):
    emr = Manager()

    return emr.describe_cluster({'CLUSTERID': cluster})


def stop(cluster):
    emr = Manager()

    return emr.stop_cluster({'CLUSTERID': cluster})


def start(name, master='m3.xlarge', node='m3.xlarge', count=3):
    emr = Manager()

    return emr.start_cluster({'NAME': name, 'master': master, 'node': node, 'count': count})


def upload(file, bucket, bucketname):
    emr = Manager()

    return emr.upload_file({'FILE': file, 'BUCKET': bucket, 'BUCKETNAME': bucketname})


def copy(cluster, bucket, bucketname):
    emr = Manager()

    return emr.copy_file({'CLUSTERID': cluster, 'BUCKET': bucket, 'BUCKETNAME': bucketname})


def run(cluster, bucket, bucketname):
    emr = Manager()

    return emr.run({'CLUSTERID': cluster, 'BUCKET': bucket, 'BUCKETNAME': bucketname})

