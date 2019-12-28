import boto3
from cloudmesh.configuration.Config import Config
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate


class Manager(object):

    def __init__(self):
        return

    def list(self, parameter):
        print("list", parameter)

    def get_client(self, service='emr'):
        """
        Connects to AWS and cre
        :param service: The service to create a client for. Either S3 or EMR.
        :return: boto3.client
        """

        configs = Config()

        key_id = configs['cloudmesh.cloud.aws.credentials.EC2_ACCESS_ID']
        access_key = configs['cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY']
        region = configs['cloudmesh.cloud.aws.credentials.region']

        client = boto3.client(service, region_name=region,
                              aws_access_key_id=key_id,
                              aws_secret_access_key=access_key)
        return client

    def parse_options(self, options, states):
        """

        Helper function to parse the arguments passed to the various EMR
        functions. Returns 'all' if it is in the options list. Otherwise it'll
        filter the list down to the valid options passed in states.

        :param options: A list of strings. Contains the options the user entered.
        :param states: A dictionary. Contains a mapping from user values
                       (e.g. booting) to AWS values (BOOTSTRAPPING).
        :return: A list of mapped values.
        """
        result = []

        if 'all' not in options:
            for option in options:
                if option in states:
                    result += [states[option]]
        return result

    @DatabaseUpdate()
    def list_clusters(self, args):
        """
        Lists the clusters that are associated with the Amazon account in the
        cloudmesh.yaml.

        :param args: A dictionary containing a status key. The key must have a
                     list of statuses the user is requesting.
        :return: cloudmesh dict.
        """
        client = self.get_client()

        options = args['status']
        opt_states = {'start': 'STARTING',
                      'boot': 'BOOTSTRAPPING',
                      'run': 'RUNNING',
                      'wait': 'WAITING',
                      'terminating': 'TERMINATING',
                      'shutdown': 'TERMINATED',
                      'error': 'TERMINATED_WITH_ERRORS'}

        cluster_state = self.parse_options(options, opt_states)
        results = client.list_clusters(ClusterStates=cluster_state)

        return [{"cm": {"cloud": "aws",
                        "kind": "emr cluster list",
                        "name": "account"},
                 'data': results['Clusters']}]

    @DatabaseUpdate()
    def list_instances(self, args):
        """
        Lists the instances that are associated with a specific cluster.

        :param args: A dictionary containing CLUSTERID, status, and type
                     values The last two must contain valid values
                     as describe in the documentation.
        :return: cloudmesh dict.
        """
        client = self.get_client()

        options = args['status']
        opt_states = {'start': 'AWAITING_FULFILLMENT',
                      'provision': 'PROVISIONING',
                      'boot': 'BOOTSTRAPPING',
                      'run': 'RUNNING',
                      'down': 'TERMINATED'}
        instance_state = self.parse_options(options, opt_states)

        options = args['type']
        opt_types = {'master': 'MASTER',
                     'core': 'CORE',
                     'task': 'TASK'}
        instance_types = self.parse_options(options, opt_types)

        results = client.list_instances(ClusterId=args['CLUSTERID'],
                                        InstanceGroupTypes=instance_types,
                                        InstanceStates=instance_state)

        return [{"cm": {"cloud": "aws",
                        "kind": "emr instance list",
                        "name": args['CLUSTERID']},
                 'data': results['Instances']}]

    @DatabaseUpdate()
    def list_steps(self, args):
        """
        Lists the steps a cluster is performing.

        :param args: A dictionary containing keys for CLUSTERID and state.
                     The state must be a valid option from the
                     documentation.
        :return: cloudmesh dict.
        """
        client = self.get_client()

        options = args['state']
        opt_states = {'pending': 'PENDING',
                      'canceling': 'CANCEL_PENDING',
                      'running': 'RUNNING',
                      'completed': 'COMPLETED',
                      'cancelled': 'CANCELLED',
                      'failed': 'FAILED',
                      'interrupted': 'INTERRUPTED'}

        step_state = self.parse_options(options, opt_states)

        if len(step_state) != 0:
            results = client.list_steps(ClusterId=args['CLUSTERID'],
                                        StepStates=step_state)
        else:
            results = client.list_steps(ClusterId=args['CLUSTERID'])

        return [{"cm": {"cloud": "aws",
                        "kind": "emr step list",
                        "name": args['CLUSTERID']},
                 'data': results['Steps']}]

    @DatabaseUpdate()
    def describe_cluster(self, args):
        """
        Describes a specific cluster.

        :param args: A dictionary with a CLUSTERID that contains
                     the cluster ID to describe.
        :return: cloudmesh dict
        """
        client = self.get_client()
        results = client.describe_cluster(ClusterId=args['CLUSTERID'])

        return [{"cm": {"cloud": "aws",
                        "kind": "emr cluster description",
                        "name": args['CLUSTERID']},
                 'data': results['Cluster']}]

    @DatabaseUpdate()
    def stop_cluster(self, args):
        """
        Stops the given cluster.

        :param args: A dictionary with a CLUSTERID that contains the
                     cluster ID to stop.
        :return: cloudmesh dict
        """
        client = self.get_client()
        client.terminate_job_flows(JobFlowIds=[args['CLUSTERID']])

        return [{"cm": {"cloud": "aws",
                        "kind": "emr stop cluster request",
                        "name": args['CLUSTERID']},
                 'data': {"name": args['CLUSTERID']}}]

    @DatabaseUpdate()
    def start_cluster(self, args):
        """
        Starts a new cluster.

        :param args: A dictionary containing a NAME, master, node, and
                     count keys. The NAME key names the cluster while
                     the master and node types are valid AWS machine types.
                     The count is the number of clusters to create.
        :return: cloudmesh dict
        """
        client = self.get_client()

        setup = {'MasterInstanceType': args['master'],
                 'SlaveInstanceType': args['node'],
                 'InstanceCount': int(args['count']),
                 'KeepJobFlowAliveWhenNoSteps': True,
                 'TerminationProtected': False}

        steps = [{'Name': 'Debugging',
                  'ActionOnFailure': 'TERMINATE_CLUSTER',
                  'HadoopJarStep': {'Jar': 'command-runner.jar',
                                    'Args': ['state-pusher-script']}}]

        results = client.run_job_flow(Name=args['NAME'],
                                      ReleaseLabel="emr-5.22.0",
                                      Instances=setup,
                                      Applications=[{'Name': 'Spark'},
                                                    {'Name': 'Hadoop'}],
                                      VisibleToAllUsers=True,
                                      Steps=steps,
                                      JobFlowRole='EMR_EC2_DefaultRole',
                                      ServiceRole='EMR_DefaultRole')

        return [{"cm": {"cloud": "aws",
                        "kind": "emr start cluster request",
                        "name": args['NAME']},
                 'data': {"cluster": results['JobFlowId'],
                          "name": args['NAME']}}]

    @DatabaseUpdate()
    def upload_file(self, args):
        """

        :param args:
        :return: cloudmesh dict
        """
        client = self.get_client(service='s3')
        client.upload_file(args['FILE'], args['BUCKET'], args['BUCKETNAME'])

        return [{"cm": {"cloud": "aws",
                        "kind": "emr file upload",
                        "name": args['BUCKETNAME']}, 'data':
                     {'file': args['FILE'],
                      'bucket': args['BUCKET'],
                      'bucketname': args['BUCKETNAME']}}]

    @DatabaseUpdate()
    def copy_file(self, args):
        """
        Copies a file from S3 to the master node's /home/hadoop folder.

        :param args: A dictionary containing CLUSTERID, BUCKET, and
                     BUCKETNAME keys. The clusterid determines the
                     cluster to copy the file to while the BUCKET and
                     BUCKETNAME values describe the bucket and file name in that
                     bucket to download.
        :return: cloudmesh dict
        """
        client = self.get_client()

        s3 = 's3://{}/{}'.format(args['BUCKET'], args['BUCKETNAME'])

        step = {'Name': 'Copy {}'.format(args['BUCKETNAME']),
                'ActionOnFailure': 'CANCEL_AND_WAIT',
                'HadoopJarStep': {'Jar': 'command-runner.jar',
                                  'Args': ['aws', 's3', 'cp', s3,
                                           '/home/hadoop/']}}

        response = client.add_job_flow_steps(JobFlowId=args['CLUSTERID'],
                                             Steps=[step])

        return [{"cm": {"cloud": "aws", "kind": "emr copy file request",
                        "name": args['BUCKETNAME']}, 'data':
                     response}]

    @DatabaseUpdate()
    def run(self, args):
        """
        Runs a Spark Python file in an S3 bucket on the cluster.

        :param args: A dictionary containing CLUSTERID, BUCKET, and
                     BUCKETNAME keys. The clusterid determines the
                     cluster to copy the file to while the BUCKET and
                     BUCKETNAME values describe the bucket and file name in that
                     bucket to download.
        :return: cloudmesh dict
        """
        client = self.get_client()

        step = {'Name': 'Run {}'.format(args['BUCKETNAME']),
                'ActionOnFailure': 'CANCEL_AND_WAIT',
                'HadoopJarStep': {'Jar': 'command-runner.jar',
                                  'Args': ['spark-submit',
                                           's3://{}/{}'.format(args['BUCKET'],
                                                               args[
                                                                   'BUCKETNAME'])]}}

        response = client.add_job_flow_steps(JobFlowId=args['CLUSTERID'],
                                             Steps=[step])

        return [{"cm": {"cloud": "aws", "kind": "emr run file request",
                        "name": args['BUCKETNAME']}, 'data':
                     response}]
