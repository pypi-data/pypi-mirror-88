#!/usr/bin/env python
from client.ClientAuth import ClientAuth
from discovery import discovery_service_proxy

FICUS_APP_NAME = "sobeyficus"


def do_service(service="", return_type="json", app_name=FICUS_APP_NAME,
               prefer_ip=False, prefer_https=False,
               method="GET", headers=None, params=None,
               data=None, timeout=None, auth=True):
    return discovery_service_proxy().do_service(service, return_type, app_name, prefer_ip, prefer_https, method,
                                                headers, params, data, timeout, auth)


def check_instance_avaliable(app_name=FICUS_APP_NAME):
    discovery_service_proxy().check_instance_available(app_name)


from .ComputeExecutionClient import *
from .DataAlgorithmClient import *
from .DataCrawlClient import *
from .FactDatasourceClient import *
from .HandlerLogClient import *
from .JobScheduleClient import *
from .ScheduleCacheClient import *
from .ScheduleJobTaskLogClient import *
from .FactDatasourceManageClient import *
