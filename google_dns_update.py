#Only uncomment the line below if you are testing this script outside of your GCP environment.
#import os
#=================
#Import required python libraries.
#=================
import json
import requests
import time
import dns.resolver
#=================
#Set GCP Project/Record information
#=================
record = 'test1.test-network.online.'
project_name = 'gcp-cloud-dns-test'
zone_name = 'test-network'
ttl = 5 * 60  #Set for 5 minutes.
#=================
#Get IP address set on Compute VM
#=================
curr_ip = dns.resolver.resolve(record, 'A')
curr_ip = curr_ip[0]
#=================
#Get Current DNS Record IP address
#=================
from google.cloud import dns
ext_ip = (json.loads(requests.get('https://ip.seeip.org/jsonip?').text)['ip'])
#Uncomment line below if you are testing this script outside of your GCP environment. 
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.\keys.json' #Only required on hosts outside of Compute Engine environment.
cloud_dns = dns.Client(project=project_name)
zone = cloud_dns.zone(zone_name, record)
#=================
# Remove Old Cloud DNS Record
#=================
record1 = zone.resource_record_set(record,'A',ttl,[f"{curr_ip}"])
changes = zone.changes()
changes.delete_record_set(record1)
changes.create()
#=================
# Wait until request is completed. 
#=================
while changes.status != 'done':
    print(f'Record Deletion Status: {changes.status}')
    time.sleep(30)     # or whatever interval is appropriate
    changes.reload()   # API request
print(f'Record Deletion Status: {changes.status}')
#=================
# Create New Cloud DNS Record
#=================
record = zone.resource_record_set('test1.test-network.online.','A',ttl,[f"{ext_ip}"])
changes = zone.changes()
changes.add_record_set(record)
changes.create()
#=================
# Wait until request is completed. 
#=================
while changes.status != 'done':
    print(f'Record Update Status: {changes.status}')
    time.sleep(30)     # or whatever interval is appropriate
    changes.reload()   # API request
print(f'Record Update Status: {changes.status}')