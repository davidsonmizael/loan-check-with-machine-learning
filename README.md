# Loan Eligibility check with Machine Learning

This project intent is to analyse the user appliance to a loan using face recognition and other Machine Learning models.

## Creating a virtual environment

Check if you have python 3.7 installed on your machine, if not, install it.

After that run the following commands:

```sh
$ virtualenv venv --python/usr/bin/python3.7 # or /usr/bin/python3 if that's the only python you have
$ ln -s venv/bin/activate .
$ . ./activate
$ python -m pip install --upgrade pip
$ pip install .
```

## Google Cloud <img src="https://www.gstatic.com/devrel-devsite/prod/v0e0f589edd85502a40d78d7d0825db8ea5ef3b99ab4070381ee86977c9168730/cloud/images/favicons/onecloud/favicon.ico" width="16" height="16">

Google cloud will be used here for face recognition and deploying the solution

### First setup on machine

Install gcloud on your machine and after you are done run `gcloud init` to authenticate and select the project.

### APIs to Enable on GCloud:

Enable the following APIs in order to run the project. Note: Your billing must be active.

- https://console.cloud.google.com/apis/api/cloudbilling.googleapis.com/
- https://console.cloud.google.com/apis/api/serviceusage.googleapis.com/
- https://console.cloud.google.com/apis/api/vision.googleapis.com/


## Running tests with Pytest-cov

Once in the project folder, run the following command to generate a HTML with the coverage of the tests in the project.

```sh
$ pytest --cov=core tests/ --cov-report html
```