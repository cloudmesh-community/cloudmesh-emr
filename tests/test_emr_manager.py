###############################################################
# pytest -v --capture=no tests/test_emr_manager.py
# pytest -v  tests/test_emr_manager.py
# pytest -v --capture=no -v --nocapture tests/test_emr_manager.py:Test_emr_manager.<METHIDNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.util import HEADING
from cloudmesh.emr.api.manager import Manager
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

        clusters = emr.list_clusters(args)
        assert clusters is not None
        assert 'cm' in clusters[0]

    def test_start_cluster(self, global_data):
        emr = Manager()

        args = {'master': 'm4.large', 'node': 'm4.large', 'count': 2, 'NAME': 'cms-test-cluster'}

        cluster = emr.start_cluster(args)

        assert cluster is not None
        assert 'cm' in cluster[0]

        global_data['cluster'] = cluster[0]['data']['cluster']

    def test_list_instances(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'status': 'all', 'type': 'all', 'CLUSTERID': global_data['cluster']}

        instances = emr.list_instances(args)

        assert instances is not None
        assert 'cm' in instances[0]

    def test_describe(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster']}

        cluster = emr.describe_cluster(args)

        assert cluster is not None
        assert 'cm' in cluster[0]

    def test_list_steps(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster'], 'state': 'all'}

        steps = emr.describe_cluster(args)

        assert steps is not None
        assert 'cm' in steps[0]

    def test_copy_file(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster'], 'BUCKET': 'test', 'BUCKETNAME': 'test.py'}

        file = emr.copy_file(args)

        assert file is not None
        assert 'cm' in file[0]

    def test_run(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster'], 'BUCKET': 'test', 'BUCKETNAME': 'test.py'}

        step = emr.copy_file(args)

        assert step is not None
        assert 'cm' in step[0]

    def test_stop_cluster(self, global_data):
        assert global_data['cluster'] != ""

        emr = Manager()

        args = {'CLUSTERID': global_data['cluster']}

        cluster = emr.stop_cluster(args)

        assert cluster is not None
        assert 'cm' in cluster[0]
        assert cluster[0]['data']['name'] == global_data['cluster']

        global_data['cluster'] = ""

