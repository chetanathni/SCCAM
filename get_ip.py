from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from oauth2client.client import AccessTokenCredentials
import urllib.request as urllib2
from urllib.parse  import urlencode
from urllib.request import Request , urlopen
from urllib.error import  HTTPError
import json
vm_instance = 'backend'
project_id =  'midyear-task-278014'
zone_name =  'us-central1-a'
credentials = GoogleCredentials.get_application_default()
compute = build('compute', 'v1', credentials=credentials)

def list_instances(compute, project, zone,instance_name):
    result = compute.instances().get(project=project, zone=zone ,instance=instance_name).execute()
    return result['networkInterfaces'][0]['accessConfigs'][0]['natIP']

ip_addr = list_instances(compute,project_id,zone_name,vm_instance)
print(ip_addr)
