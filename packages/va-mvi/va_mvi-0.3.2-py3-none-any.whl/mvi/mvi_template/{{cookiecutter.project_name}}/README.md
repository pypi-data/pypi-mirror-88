# MVI project: {{cookiecutter.project_name}}

# Creating the service
The ```service.py``` contains an example service and shows how to use the mvi SDK.

This example shows:
 - How to initiate an mvi service
 - How to register changeable parameters
 - How to register functions as entrypoints
 - How to log from the service
 - How to send notifications from the service
 - How to start the service

If the service requires external packages, they should be specified in the `requirements.txt` file.
# Deploying the service
The service can be deployed using the mvi command-line interface:

Deploying from a local directory or tarball (.tar.gz):

```mvi deploy myservice 0.0.1 {path_to_project} ```

Deploying from a git repository:

```mvi deploy myservice 0.0.1 --git {git_url}```

# Documentation
Full documentation of the SDK and the CLI can be found here: https://vikinganalytics.github.io/mvi-docs/

# Extra
If you want to change name of the service file ```service.py```, or deploy another file as the
mvi service then you have to change the ```APP_FILE``` key in the ```.s2i/environment``` file.