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

from zenml.utils.source_utils import load_source_path_class


def preprocessing_fn(inputs, custom_config):
    c = load_source_path_class(custom_config['source'])

    if 'features' in custom_config['args']:
        features = custom_config['args']['features']
    else:
        features = None

    if 'labels' in custom_config['args']:
        labels = custom_config['args']['labels']
    else:
        labels = None

    if 'overwrite' in custom_config['args']:
        overwrite = custom_config['args']['overwrite']
    else:
        overwrite = None

    # TODO: decide what to do with the additional params
    return c(features=features,
             labels=labels,
             overwrite=overwrite).get_preprocessing_fn()(inputs)
