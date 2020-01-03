###############################################################
# pytest -v --capture=no tests/test_emr_manager.py
# pytest -v  tests/test_emr_manager.py
# pytest -v --capture=no -v --nocapture tests/test_emr_manager.py:Test_emr_manager.<METHODNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.util import HEADING
from cloudmesh.emr.api.manager import Manager
from cloudmesh.common.StopWatch import StopWatch
from pprint import pprint
import textwrap
import oyaml as yaml
import munch
import re

import pytest

@pytest.mark.incremental
class Test_emr_manager:

    @pytest.fixture(scope='module')
    def global_data(self):
        return {'cluster': ""}

    def test_config(self):
        config = Config()
        assert config is not None

    def test_ec2_access_id(self):
        config = Config()

        data = config['cloudmesh.cloud.aws.credentials.EC2_ACCESS_ID']

        assert data is not None
        assert data != ""

    def test_ec2_key_id(self):
        config = Config()

        data = config['cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY']

        assert data is not None
        assert data != ""

    def test_ec2_region(self):
        config = Config()

        data = config['cloudmesh.cloud.aws.credentials.EC2_SECRET_KEY']

        assert data is not None
        assert data != ""

    def test_get_client_emr(self):
        emr = Manager()

        client = emr.get_client()
        assert client is not None

    def test_get_client_s3(self):
        emr = Manager()

        client = emr.get_client('s3')
        assert client is not None

    def test_list_clusters(self):
        emr = Manager()

        args = {'status': 'all'}

        StopWatch.start("List Clusters")
        clusters = emr.list_clusters(args)
        StopWatch.stop("List Clusters")

        assert clusters is not None
        assert 'cm' in clusters[0]

    def test_start_cluster(self, global_data):
        emr = Manager()

        args = {'master': 'm4.large', 'node': 'm4.large', 'count': 2, 'NAME': 'cms-test-cluster'}

        StopWatch.start("Start Cluster")
        cluster = emr.start_cluster(args)
        StopWatch.stop("Start Cluster")

        assert cluster is not None
        assert 'cm' in cluster[0]

        global_data['cluster'] = cluster[0]['data']['cluster']

    def test_list_instances(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'status': 'all', 'type': 'all', 'CLUSTERID': global_data['cluster']}

        StopWatch.start("List Instances")
        instances = emr.list_instances(args)
        StopWatch.stop("List Instances")

        assert instances is not None
        assert 'cm' in instances[0]

    def test_describe(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster']}

        StopWatch.start("Describe Cluster")
        cluster = emr.describe_cluster(args)
        StopWatch.stop("Describe Cluster")

        assert cluster is not None
        assert 'cm' in cluster[0]

    def test_list_steps(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster'], 'state': 'all'}

        StopWatch.start("List Steps")
        steps = emr.describe_cluster(args)
        StopWatch.stop("List Steps")

        assert steps is not None
        assert 'cm' in steps[0]

    def test_copy_file(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster'], 'BUCKET': 'test', 'BUCKETNAME': 'test.py'}

        StopWatch.start("Copy File")
        file = emr.copy_file(args)
        StopWatch.stop("Copy File")

        assert file is not None
        assert 'cm' in file[0]

    def test_run(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster'], 'BUCKET': 'test', 'BUCKETNAME': 'test.py'}

        StopWatch.start("Run Program")
        step = emr.run(args)
        StopWatch.stop("Run Program")

        assert step is not None
        assert 'cm' in step[0]

    def test_stop_cluster(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster']}

        StopWatch.start("Stop Cluster")
        cluster = emr.stop_cluster(args)
        StopWatch.stop("Stop Cluster")

        assert cluster is not None
        assert 'cm' in cluster[0]
        assert cluster[0]['data']['name'] == global_data['cluster']

        global_data['cluster'] = ""

    def test_benchmark(self):
        StopWatch.benchmark()
