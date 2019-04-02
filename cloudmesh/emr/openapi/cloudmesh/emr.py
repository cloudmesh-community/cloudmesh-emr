from __future__ import print_function
from cloudmesh.emr.api.manager import Manager

'''
list_clusters - done
list_instances
list_steps
describe
stop
start
copy
run
'''

def start():
    pass

def list_clusters(status=None):
    emr = Manager()

    if status is None:
        return emr.list_clusters({'status': 'all'})
    else:
        input_status = status.split(",")
        if 'all' in input_status:
            return emr.list_clusters({'status': 'all'})
        else:
            valid_status = ['start', 'boot', 'run', 'wait', 'terminating', 'shutdown', 'error', 'all']
            check_status = []

            for status in input_status:
                if status in valid_status:
                    check_status += [status]
            return emr.list_clusters({'status': check_status})
