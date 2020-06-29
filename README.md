# GTM Deploy Manager

The premise is:
- You have Android and iOS GTM containers.
- You have more than one Android and iOS containers and you would like to reply the tags and triggers between containers
- You have an Android "Arrowhead" container that it will be used as template to be replicated through the script to other containers
- You will have to download the "Arrowhead" container manually
- You will upload and merge manually the output containers (in the "output" folder)

Import pip requirements:

```
pip install -r requirements.txt
```

# Deploy Instructions

1. Get Arrowhead Android and iOS Containers without "_V<NUMBER>" in the filename
2. Put the file in the folder "/input"
3. Execute the Script:

```
python gtm_deploy.py --yaml config/config.yaml
```
4. The Script will generate the containers for each App in the folder "/output".
5. Upload them to GTM manually.

# Example execution

```
python gtm_deploy.py --yaml config/config.yaml
```
