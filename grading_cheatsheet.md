# MLOps ZoomCamp Grading sheet
This is just to help those who are evaluating the project to help them find what they are looking for...
## Problem Description
Have a look at the [README](README.md)

## Cloud (TBB - To be built)
This will be configured to run on AWS as a lambda function

## Experiment Tracking and Model Registry (TBB - To be built)
MLFlow is used to track the models. These will be stored in a S3 bucket

## Workflow orchestration (TBB - To be built)
I've built the entire workflow in Mage, with several different pipelines
    * Data_Prep: This pipeline pulls in data that will be used to train the model
    * Model_Train: This pipeline uses the Data_Prep output to train the model.
    * Model_Predict_Full: This will predict the qualifying times and positions for every driver for a qualifying session.
    * Model_Predict_Hypothetical: Here the user can enter the values of each feature, and observe the predicted effect.

## Model deployment (TBB - To be built)
* Aim is to deploy this as a lambda function on AWS

## Model Monitoring (TBB - To be built)
I've utilised the Mage.ai dashboards
    * Data_drift: Look at the dashboard for the `Data_Prep` pipeline
    * Model_drift: Look at the dashboard for the `Model_Predict_Full` pipeline

## Reproducibility (TBB - To be built)
See the [README](README.md)

## Best Practices (TBB - To be built)
### Unit tests
* Unit tests are present in the Mage Blocks to check incoming data
* There are separate tests in the `tests/unit_tests` folder to if you want to check those instead.

### Integration tests (TBB - To be built)
* This is present in the `tests/integration_test` folder

### Linter and code-formatter
* I used Black, pylint, etc.
* Settings: TBD

### Makefile
This is located in the `tests` folder

### Pre-commit hooks
This can be seen here

### CI/CD pipeline
TBD