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

import os
import uuid

from google.cloud import aiplatform
import pytest

import create_data_labeling_job_active_learning_sample
import helpers

API_ENDPOINT = os.getenv("DATA_LABELING_API_ENDPOINT")
PROJECT_ID = os.getenv("BUILD_SPECIFIC_GCLOUD_PROJECT")
LOCATION = "us-central1"
DATASET_ID = "1905673553261363200"
INPUTS_SCHEMA_URI = "gs://google-cloud-aiplatform/schema/datalabelingjob/inputs/image_classification_1.0.0.yaml"
DISPLAY_NAME = f"temp_create_data_labeling_job_active_learning_test_{uuid.uuid4()}"

INSTRUCTIONS_GCS_URI = (
    "gs://ucaip-sample-resources/images/datalabeling_instructions.pdf"
)
ANNOTATION_SPEC = "rose"


@pytest.fixture
def shared_state():
    state = {}
    yield state


@pytest.fixture
def job_client():
    client_options = {"api_endpoint": API_ENDPOINT}
    job_client = aiplatform.gapic.JobServiceClient(client_options=client_options)
    yield job_client


@pytest.fixture(scope="function", autouse=True)
def teardown(capsys, shared_state, job_client):
    yield

    job_client.cancel_data_labeling_job(name=shared_state["data_labeling_job_name"])

    # Verify Data Labelling Job is cancelled, or timeout after 400 seconds
    helpers.wait_for_job_state(
        get_job_method=job_client.get_data_labeling_job,
        name=shared_state["data_labeling_job_name"],
        timeout=400,
        freq=10,
    )

    # Delete the data labeling job
    response = job_client.delete_data_labeling_job(
        name=shared_state["data_labeling_job_name"]
    )

    print("Delete LRO:", response.operation.name)
    delete_data_labeling_job_response = response.result(timeout=300)
    print("delete_data_labeling_job_response", delete_data_labeling_job_response)

    out, _ = capsys.readouterr()
    assert "delete_data_labeling_job_response" in out


# Creating a data labeling job for images
def test_create_data_labeling_job_active_learning_sample(capsys, shared_state):

    create_data_labeling_job_active_learning_sample.create_data_labeling_job_active_learning_sample(
        project=PROJECT_ID,
        display_name=DISPLAY_NAME,
        dataset=f"projects/{PROJECT_ID}/locations/{LOCATION}/datasets/{DATASET_ID}",
        instruction_uri=INSTRUCTIONS_GCS_URI,
        inputs_schema_uri=INPUTS_SCHEMA_URI,
        annotation_spec=ANNOTATION_SPEC,
        api_endpoint=API_ENDPOINT,
    )

    out, _ = capsys.readouterr()

    # Save resource name of the newly created data labeing job
    shared_state["data_labeling_job_name"] = helpers.get_name(out)
