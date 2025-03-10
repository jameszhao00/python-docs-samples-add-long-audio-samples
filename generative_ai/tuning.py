# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_sdk_tuning]
from __future__ import annotations


import pandas as pd

import vertexai
from vertexai.preview.language_models import TextGenerationModel


def tuning(
    project_id: str,
    location: str,
    training_data: pd.DataFrame | str,
    train_steps: int = 10,
):
    """Tune a new model, based on a prompt-response data.

    "training_data" can be either the GCS URI of a file formatted in JSONL format
    (for example: training_data=f'gs://{bucket}/{filename}.jsonl'), or a pandas
    DataFrame. Each training example should be JSONL record with two keys, for
    example:
      {
        "input_text": <input prompt>,
        "output_text": <associated output>
      },
    or the pandas DataFame should contain two columns:
      ['input_text', 'output_text']
    with rows for each training example.

    Args:
      project_id: GCP Project ID, used to initialize vertexai
      location: GCP Region, used to initialize vertexai
      training_data: GCS URI of training file or pandas dataframe of training data
      train_steps: Number of training steps to use when tuning the model.
    """
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@001")

    model.tune_model(
      training_data=training_data,
      # Optional:
      train_steps=train_steps,
      tuning_job_location="europe-west4",
      tuned_model_location="us-central1",
    )

    # Test the tuned model:
    response = model.predict("Tell me some ideas combining VR and fitness:")
    print(f"Response from Model: {response.text}")
# [END aiplatform_sdk_tuning]

    return response


if __name__ == "__main__":
    tuning()
