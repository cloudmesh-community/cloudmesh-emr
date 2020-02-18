###############################################################
# pytest -v --capture=no tests/test_emr_command.py
# pytest -v  tests/test_emr_command.py
# pytest -v --capture=no -v --nocapture tests/test_emr_command..py::Test_emr_command::<METHODNAME>
###############################################################
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.util import HEADING
from cloudmesh.emr.command.emr import EmrCommand
from pprint import pprint
import textwrap
import oyaml as yaml
import munch
import re

import pytest

@pytest.mark.incremental
class Test_emr_command:

    @pytest.fixture(scope='module')
    def global_data(self):
        return {'cluster': ""}

    def test_list_clusters(self, capsys):
        emr = EmrCommand()
        emr.do_emr("list clusters")

        result = capsys.readouterr()

        assert result.out[0] == "+"

    def test_start_cluster(self, capsys, global_data):
        emr = EmrCommand()
        emr.do_emr("start test --master=m4.large --node=m4.large --count=2")

        result = capsys.readouterr()

        assert result.out[:5] == "test:"

        global_data['cluster'] = result.out[6:-9]

    def test_list_instances(self, capsys, global_data):
        assert global_data['cluster'] != ""

        emr = EmrCommand()
        emr.do_emr("list instances {}".format(global_data['cluster']))

        result = capsys.readouterr()

        assert result.out[0] == "+" or result.out == "No instances were found.\n"

    def test_describe(self, capsys, global_data):
        assert global_data['cluster'] != ""

        emr = EmrCommand()
        emr.do_emr("describe {}".format(global_data['cluster']))

        result = capsys.readouterr()

        assert result.out[0] == "+"

    def test_list_steps(self, capsys, global_data):
        assert global_data['cluster'] != ""

        emr = EmrCommand()
        emr.do_emr("list steps {}".format(global_data['cluster']))

        result = capsys.readouterr()

        assert result.out[0] == "+"

    def test_copy_file(self, capsys, global_data):
        assert global_data['cluster'] != ""

        emr = EmrCommand()
        emr.do_emr("copy {} test test.py".format(global_data['cluster']))

        result = capsys.readouterr()

        assert result.out[:9] == "Copy step"

    def test_run(self, capsys, global_data):
        assert global_data['cluster'] != ""

        emr = EmrCommand()
        emr.do_emr("run {} test test.py".format(global_data['cluster']))

        result = capsys.readouterr()

        assert result.out[:8] == "Run step"

    def test_stop_cluster(self, capsys, global_data):
        assert global_data['cluster'] != ""

        emr = EmrCommand()
        emr.do_emr("stop {}".format(global_data['cluster']))

        result = capsys.readouterr()

        assert result.out[-9:-1] == "Stopping"

