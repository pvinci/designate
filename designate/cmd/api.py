# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Author: Kiall Mac Innes <kiall@hp.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import sys

from oslo.config import cfg
from oslo_log import log as logging

from designate.openstack.common import service
from designate import rpc
from designate import utils
from designate.api import service as api_service


CONF = cfg.CONF
CONF.import_opt('workers', 'designate.api', group='service:api')


def main():
    utils.read_config('designate', sys.argv)
    logging.setup(CONF, 'designate')
    utils.setup_gmr(log_dir=cfg.CONF.log_dir)

    rpc.init(CONF)

    launcher = service.launch(api_service.Service(),
                              CONF['service:api'].workers)
    launcher.wait()
