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
"""Factory to register backend classes to backends"""

from zenml.core.backends.orchestrator.beam.orchestrator_beam_backend import \
    OrchestratorBeamBackend
from zenml.core.backends.orchestrator.gcp.orchestrator_gcp_backend import \
    OrchestratorGCPBackend
from zenml.core.backends.orchestrator.kubeflow.orchestrator_kubeflow_backend \
    import OrchestratorKubeFlowBackend
from zenml.core.backends.orchestrator.kubernetes\
    .orchestrator_kubernetes_backend import \
    OrchestratorKubernetesBackend
from zenml.core.backends.orchestrator.local.orchestrator_local_backend import \
    OrchestratorLocalBackend
from zenml.core.backends.processing.processing_dataflow_backend import \
    ProcessingDataFlowBackend
from zenml.core.backends.processing.processing_local_backend import \
    ProcessingLocalBackend
from zenml.core.backends.processing.processing_spark_backend import \
    ProcessingSparkBackend
from zenml.core.backends.training.training_gcaip_backend import \
    TrainingGCAIPBackend
from zenml.core.backends.training.training_local_backend import \
    TrainingLocalBackend


class BackendFactory:
    """Definition of BackendFactory to track all backends in ZenML.

    All backends (including custom backends) are to be registered here.
    """

    def __init__(self):
        self.backends = {}

    def get_backends(self):
        return self.backends

    def register_backend(self, type_, backend):
        self.backends[type_] = backend

    def get_backend_by_type(self, type_):
        return self.backends[type_]

    def get_backend_by_key(self, key):
        all_backends = self.get_backends()
        return [b for b in all_backends if b.BACKEND_KEY == key]


# Register the injections into the factory
backend_factory = BackendFactory()
backend_factory.register_backend(OrchestratorBeamBackend.BACKEND_TYPE,
                                 OrchestratorBeamBackend)
backend_factory.register_backend(OrchestratorLocalBackend.BACKEND_TYPE,
                                 OrchestratorLocalBackend)
backend_factory.register_backend(OrchestratorGCPBackend.BACKEND_TYPE,
                                 OrchestratorGCPBackend)
backend_factory.register_backend(OrchestratorKubeFlowBackend.BACKEND_TYPE,
                                 OrchestratorKubeFlowBackend)
backend_factory.register_backend(OrchestratorKubernetesBackend.BACKEND_TYPE,
                                 OrchestratorKubernetesBackend)
backend_factory.register_backend(ProcessingDataFlowBackend.BACKEND_TYPE,
                                 ProcessingDataFlowBackend)
backend_factory.register_backend(ProcessingLocalBackend.BACKEND_TYPE,
                                 ProcessingLocalBackend)
backend_factory.register_backend(ProcessingSparkBackend.BACKEND_TYPE,
                                 ProcessingSparkBackend)
backend_factory.register_backend(TrainingGCAIPBackend.BACKEND_TYPE,
                                 TrainingGCAIPBackend)
backend_factory.register_backend(TrainingLocalBackend.BACKEND_TYPE,
                                 TrainingLocalBackend)
