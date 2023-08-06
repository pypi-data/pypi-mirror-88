# Release history

### 0.0.7
* Add -R option for better debugging.

### 0.0.6
* Add latest boto version to tests.

### 0.0.5
* Add ability to bundle boto3 library. Simply specify
version in the constructor.

### 0.0.4
* Update Docker bundling commands. Use bash to move files between directories instead of installing with `-t` flag.
Related issue: https://github.com/pypa/pip/issues/103

### 0.0.3
* Add disclaimer that `docker` is required.

### 0.0.2
* Ensure that cdk application works by running `cdk synth` command.

### 0.0.1
* Initial build.
* Twilio SDK 6.46.0.
* Docker image for asset building: python:3.9.