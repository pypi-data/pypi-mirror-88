#  Copyright (c) maiot GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Orchestrator for simple GCP VM backend"""

import base64
import json
import os
import time
from typing import Dict, Any
from typing import Text

import googleapiclient.discovery
from google.oauth2 import service_account as sa

from zenml.core.backends.orchestrator.local.orchestrator_local_backend import \
    OrchestratorLocalBackend


class OrchestratorGCPBackend(OrchestratorLocalBackend):
    """Orchestrates pipeline in a VM.

    Every ZenML pipeline runs in backends.
    """
    BACKEND_TYPE = 'gcp'
    SOURCE_DISK_IMAGE = "projects/cos-cloud/global/images/cos-stable-81" \
                        "-12871-1196-0"

    def __init__(self,
                 project,
                 image: Text = None,
                 zone: Text = 'europe-west1-b',
                 instance_name: Text = str(int(time.time())),
                 machine_type: Text = 'n1-standard-4',
                 preemptible: bool = True,
                 service_account: Text = None,
                 **unused_kwargs):
        self.project = project
        self.zone = zone
        self.image = image
        self.machine_type = machine_type
        self.instance_name = instance_name
        self.preemptible = preemptible

        if service_account:
            scopes = ['https://www.googleapis.com/auth/cloud-platform']
            self.credentials = \
                sa.Credentials.from_service_account_info(
                    sa, scopes=scopes)
        else:
            self.credentials = None

        super().__init__(**unused_kwargs)
        raise NotImplementedError('Its coming soon!')

    def run(self, config: Dict[Text, Any]):
        """
        This run function essentially calls an underlying TFX orchestrator run.
        However it is meant as a higher level abstraction with some
        opinionated decisions taken.

        Args:
            config: a ZenML config dict
        """
        # Instantiate google compute service
        compute = googleapiclient.discovery.build('compute', 'v1',
                                                  credentials=self.credentials)

        # Configure the machine
        machine_type = f"zones/{self.zone}/machineTypes/{self.machine_type}"
        startup_script = open(
            os.path.join(
                os.path.dirname(__file__), 'startup-script.sh'), 'r').read()

        config_encoded = base64.b64encode(json.dumps(config).encode())
        c_params = f'run_pipeline --config_b64 {config_encoded}'

        compute_config = {
            'name': self.instance_name,
            'zone': f'projects/{self.project}/zones/{self.zone}',
            'machineType': machine_type,

            # Specify if preemtible
            'scheduling': {'preemptible': self.preemptible},

            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': self.SOURCE_DISK_IMAGE,
                        'diskSizeGb': '100'
                    }
                }
            ],

            # Specify a network interface with NAT to access the public
            # internet.
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            # Allow the instance to access cloud storage and logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    # to be refined
                    'https://www.googleapis.com/auth/cloud-platform',
                    # 'https://www.googleapis.com/auth/devstorage.read_write',
                    # 'https://www.googleapis.com/auth/logging.write'
                ]
            }],

            # Metadata is readable from the instance and allows you to
            # pass configuration from deployment scripts to instances.
            'metadata': {
                'items': [
                    {
                        # Startup script is automatically executed by the
                        # instance upon startup.
                        'key': 'startup-script',
                        'value': startup_script
                    },
                    {
                        'key': 'image_name',
                        'value': self.image,
                    },
                    {
                        'key': 'container_params',
                        'value': c_params,
                    },
                ]
            }
        }

        try:
            return compute.instances().insert(
                project=self.project,
                zone=self.zone,
                body=compute_config).execute()
        except Exception as e:
            raise AssertionError(f"GCP VM failed to launch with the following "
                                 f"error: {str(e)}")
