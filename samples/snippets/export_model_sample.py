# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_export_model_sample]
from google.cloud import aiplatform


def export_model_sample(
    project: str,
    model_id: str,
    gcs_destination_output_uri_prefix: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
    timeout: int = 300,
):
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.ModelServiceClient(client_options=client_options)
    output_config = {
        "artifact_destination": {"output_uri_prefix": gcs_destination_output_uri_prefix}
    }
    name = client.model_path(project=project, location=location, model=model_id)
    response = client.export_model(name=name, output_config=output_config)
    print("Long running operation:", response.operation.name)
    export_model_response = response.result(timeout=timeout)
    print("export_model_response:", export_model_response)


# [END aiplatform_export_model_sample]
