###############################################################
# pytest -v --capture=no tests/test_emr_openapi.py
# pytest -v  tests/test_emr_openapi.py
# pytest -v --capture=no -v --nocapture tests/test_emr_openapi.py:Test_emr_openapi.<METHIDNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.run.subprocess import run
from cloudmesh.emr.command.emr import EmrCommand
from pprint import pprint
import textwrap
import oyaml as yaml
import munch
import re

import pytest


@pytest.mark.incremental
class Test_emr_openapi:

    def setup(self):
        self.clusterid = ""

    def test_list_clusters(self):
        result = run(['curl', 'http://localhost:8080/api/list_clusters'], shell=False)

        assert result is not None
        assert result[0] == "["

    def test_start_cluster(self):
        result = run(['curl', 'http://localhost:8080/api/start?name=pytest-cluster&count=2'], shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = result[16:31]

    def test_list_steps(self):
        result = run(['curl', 'http://localhost:8080/api/list_steps?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_describe(self):
        result = run(['curl', 'http://localhost:8080/api/describe?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_copy(self):
        result = run(['curl','http://localhost:8080/api/copy?cluster=?{}&bucket=test&bucketname='
                             'test.py'.format(self.clusterid)], shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_run(self):
        result = run(['curl','http://localhost:8080/api/run?cluster=?{}&bucket=test&bucketname='
                             'test.py'.format(self.clusterid)], shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_list_instances(self):
        result = run(['curl', 'http://localhost:8080/api/list_instances?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

    def test_stop_cluster(self):
        result = run(['curl', 'http://localhost:8080/api/stop?cluster=?{}'.format(self.clusterid)],
                     shell=False)

        assert result is not None
        assert result[0] == "{"

        self.clusterid = ""

