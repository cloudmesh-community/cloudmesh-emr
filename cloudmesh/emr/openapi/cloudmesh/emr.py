from __future__ import print_function
from cloudmesh.emr.api.manager import Manager

'''
list_clusters - done
list_instances - done
list_steps - done
describe - done
stop
start
upload
copy
run
'''


def start():
    pass


def get_list_from_arg(arg, valid):
    if arg is None:
        return ['all']
    else:
        arg_split = arg.split(",")

        if 'all' in arg_split:
            return ['all']
        else:
            result = []

            for arg in arg_split:
                if arg in valid:
                    result += [arg]
            return result


def list_clusters(status=None):
    emr = Manager()

    val_state = ['start', 'boot', 'run', 'wait', 'terminating', 'shutdown', 'error', 'all']
    states = get_list_from_arg(status, val_state)

    return emr.list_clusters({'status': states})


def list_instances(cluster, status=None, type=None):
    emr = Manager()

    val_state = ['start', 'provision', 'boot', 'run', 'down']
    states = get_list_from_arg(status, val_state)

    val_type = ['master', 'core', 'task']
    types = get_list_from_arg(type, val_type)

    return emr.list_instances({'<CLUSTERID>': cluster, 'status': states, 'type': types})


def list_steps(cluster, status=None):
    emr = Manager()

    val_state = ['pending', 'canceling', 'running', 'completed', 'cancelled', 'failed', 'interrupted']
    states = get_list_from_arg(status, val_state)

    return emr.list_steps({'<CLUSTERID>': cluster, 'state': states})


def describe(cluster):
    emr = Manager()

    return emr.describe_cluster({'<CLUSTERID>': cluster})


def stop(cluster):
    emr = Manager()

    return emr.stop_cluster({'<CLUSTERID>': cluster})

'''

    def start_cluster(self, args):
        client = self.get_client()

        setup = {'MasterInstanceType': args['master'], 'SlaveInstanceType': args['node'],
                 'InstanceCount': int(args['count']), 'KeepJobFlowAliveWhenNoSteps': True,
                 'TerminationProtected': False}

        steps = [{'Name': 'Debugging', 'ActionOnFailure': 'TERMINATE_CLUSTER',
                 'HadoopJarStep': { 'Jar': 'command-runner.jar', 'Args': ['state-pusher-script']}}]

        results = client.run_job_flow(Name=args['<NAME>'], ReleaseLabel="emr-5.22.0", Instances=setup,
                                      Applications=[{'Name': 'Spark'}, {'Name': 'Hadoop'}], VisibleToAllUsers=True,
                                      Steps=steps, JobFlowRole='EMR_EC2_DefaultRole', ServiceRole='EMR_DefaultRole')

        return {"cloud": "aws", "kind": "emr", "cluster": results['JobFlowId'], "name": args['<NAME>'],
                "status": "Starting"}

    def upload_file(self, args):
        client = self.get_client(service='s3')
        client.upload_file(args['<FILE>'], args['<BUCKET>'], args['<BUCKETNAME>'])

        return {"cloud": "aws", "kind": "file", "bucket": args['<BUCKET>'], "file": args['<BUCKETNAME>']}

    def copy_file(self, args):
        client = self.get_client()

        s3 = 's3://' + args['<BUCKET>'] + '/' + args['<BUCKETNAME>']

        step = {'Name': 'Copy ' + args['<BUCKETNAME>'], 'ActionOnFailure': 'CANCEL_AND_WAIT',
                'HadoopJarStep': {'Jar': 'command-runner.jar', 'Args': ['aws', 's3', 'cp', s3, '/home/hadoop/']}}

        response = client.add_job_flow_steps(JobFlowId=args['<CLUSTERID>'], Steps=[step])
        return response

    def run(self, args):
        client = self.get_client()

        step = {'Name': 'Run ' + args['<BUCKETNAME>'], 'ActionOnFailure': 'CANCEL_AND_WAIT',
                'HadoopJarStep': {'Jar': 'command-runner.jar', 'Args': ['spark-submit',
                                                                        's3://' + args['<BUCKET>'] + '/' +
                                                                        args['<BUCKETNAME>']]}}

        response = client.add_job_flow_steps(JobFlowId=args['<CLUSTERID>'], Steps=[step])
        return response'''

