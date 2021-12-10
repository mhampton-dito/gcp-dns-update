#import os
import json
import requests
import time
import dns.resolver
curr_ip = dns.resolver.resolve('test1.test-network.online.', 'A')
curr_ip = curr_ip[0]
#print(curr_ip)
from google.cloud import dns
ttl = 5 * 60  # seconds
ext_ip = (json.loads(requests.get('https://ip.seeip.org/jsonip?').text)['ip'])

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '.\keys.json'
cloud_dns = dns.Client(project='gcp-cloud-dns-test')
zone = cloud_dns.zone('test-network', 'test-network.online.')

# Remove Old Record
record1 = zone.resource_record_set('test1.test-network.online.','A',ttl,[f"{curr_ip}"])
changes = zone.changes()
changes.delete_record_set(record1)
changes.create()
while changes.status != 'done':
    print(f'Record Deletion Status: {changes.status}')
    time.sleep(30)     # or whatever interval is appropriate
    changes.reload()   # API request
print(f'Record Deletion Status: {changes.status}')
# Create New Record
record = zone.resource_record_set('test1.test-network.online.','A',ttl,[f"{ext_ip}"])
changes = zone.changes()
changes.add_record_set(record)
changes.create()
while changes.status != 'done':
    print(f'Record Update Status: {changes.status}')
    time.sleep(30)     # or whatever interval is appropriate
    changes.reload()   # API request
print(f'Record Update Status: {changes.status}')