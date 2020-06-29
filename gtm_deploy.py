#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
  GTM Deployment 1.1

  @author Francisco Javier Pulido Piñero
"""
import os
import sys
import math
import argparse
import json
import shutil
import yaml
import time

"""
Digital Analytics Common libraries
"""
dirname, filename = os.path.split(os.path.abspath(__file__))
print "running from", dirname
print "file is", filename

sys.path.append(dirname + '/../common/')

"""
Dependencies: managed with pip requirements
"""

"""
   See Argparse Tutorial:  https://docs.python.org/2/howto/argparse.html#
"""
def parseArguments():
    parser = argparse.ArgumentParser(description="GTM Deployment")

    # Mandatory arguments
    required_named = parser.add_argument_group('Required arguments')
    required_named.add_argument("--yaml", help="yaml configuration with the list of etls to execute", required=True)

    # Optional arguments
    parser.add_argument("--dry_run", help="execution in dry run: show commands but don't launch process", action="store_true")
    return parser.parse_args()

"""
    Replace in gtm id in file
"""
def replace_gtmid_uaid_infile(ob_gtmid,ob_uaid,ob_uaid_var,app_name):
    fin = open(dirname + '/output/'+app_name+"_"+ob_gtmid+'.json', 'rt')
    data = fin.read()
    data = data.replace("{{UA-arrowhead_container-UK}}", ob_uaid_var)
    data = data.replace("UA-arrowhead_container-UK", ob_uaid_var[2:-2])
    data = data.replace("UA-115771276-12", ob_uaid)
    fin.close()

    fin = open(dirname + '/output/'+app_name+"_"+ob_gtmid+'.json', 'wt')
    fin.write(data)
    fin.close()

"""
  GTM Deployment
  ===============
  Steps:
  1. From Android Arrowhead_android extract into var:
     - UA-ID
     - GTM-ID
  2. From iOS arrowhead_container
     2.1 read arrowhead_container_android_gtmid file
     2.2 read app_gtmid file
     2.3 load arrowhead_container Android file / App file
     2.4 extract and save into var app container section
     2.5 copy arrowhead container android to output
  3. Create a copy file from iOS Arrowhead with name <GTM-Container> arrowhead_container iOS
     3.1 read app_name copied file
     3.2 load App Copyied file
     3.3 Replace container section
     3.4 Save into file
     3.5 Replace Arrowhead Container ID to App one
"""
start_time = math.trunc(time.time())

# Get Arguments
args = parseArguments()
yaml_path     = args.yaml


# Streams
stream = open(dirname + "/" + yaml_path, "r")
app_types = yaml.load_all(stream)
yaml.warnings({'YAMLLoadWarning': False})

arrowhead_android="arrowhead_container_android"
arrowhead_ios="arrowhead_container_ios"

# Note: "Arrowhead_android": is the arrowhead_container Container

# Extract from config.yaml, next elements:
for app_type in app_types:
    for index, out in enumerate(app_type['NATIVE']):
        # 1. From Android Arrowhead_android extract into var:
        #    - UA-ID
        #    - GTM-ID
        if (out['app']['app_name'] == arrowhead_android):
            arrowhead_container_android_uaid = out['app']['ua_id']
            arrowhead_container_android_gtmid = out['app']['container_id']

# Streams
stream = open(dirname + "/" + yaml_path, "r")
app_types = yaml.load_all(stream)

# Extract from config.yaml, next elements:
for app_type in app_types:
    for index, out in enumerate(app_type['NATIVE']):
        # 2. From iOS Arrohead container
        # 2.1 read arrowhead_container_android_gtmid file
        with open(dirname + '/input/'+arrowhead_container_android_gtmid+'.json', 'r') as arrowhead_container_android_file:
            arrowhead_arrowhead_container_android_gtmid_file=arrowhead_container_android_file.read()

        # 2.2 read app_gtmid file
        with open(dirname + '/input/'+out['app']['container_id']+'.json', 'r') as app_file:
            app_gtmid_file=app_file.read()

        # 2.3 load arrowhead_container Android file / App file
        arrowhead_container_android_gtmid_file_obj = json.loads(arrowhead_arrowhead_container_android_gtmid_file)
        app_gtmid_file_obj = json.loads(app_gtmid_file)

        # 2.4 extract and save into var app container section
        app_container_section = app_gtmid_file_obj['containerVersion']['container']

        # 2.5 copy arrowhead container android to output
        shutil.copyfile(dirname + '/input/'+arrowhead_container_android_gtmid+".json", dirname + '/output/'+arrowhead_container_android_gtmid+".json")

        # 3. Create a copy file from iOS Arrowhead with name <GTM-Container> arrowhead_container iOS
        shutil.copyfile(dirname + '/input/'+arrowhead_container_android_gtmid+".json", dirname + '/output/'+out['app']['app_name']+"_"+out['app']['container_id']+".json")

        # 3.1 read app_name copied file
        with open(dirname + '/output/'+out['app']['app_name']+"_"+out['app']['container_id']+'.json', 'r') as app_copied_file:
            arrowhead_container_ios_copied_gtmid_file=app_copied_file.read()

        # 3.2 load App Copyied file
        app_copied_gtmid_file_obj = json.loads(arrowhead_container_ios_copied_gtmid_file)

        # 3.3 Replace container section
        app_copied_gtmid_file_obj['containerVersion']['container'] = app_container_section

        # 3.4 Save into file
        with open(dirname + '/output/'+out['app']['app_name']+"_"+out['app']['container_id']+'.json', 'w') as app_copied_file:
            json.dump(app_copied_gtmid_file_obj,app_copied_file,indent=4)

        # 3.5 Replace Arrowhead Container ID to App one
        replace_gtmid_uaid_infile(out['app']['container_id'],out['app']['ua_id'],out['app']['ua_id_var'],out['app']['app_name'])


# Remove arrowhead
os.remove(dirname + '/output/'+arrowhead_container_android_gtmid+".json")

end_time = math.trunc(time.time())

sys.exit(0)
