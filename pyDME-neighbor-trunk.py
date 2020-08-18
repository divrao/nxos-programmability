from __future__ import print_function
import json
import requests

from pydme import Node, options

host = '172.25.74.96'
username = 'admin'
password = 'cisco123'

host_url = 'https://' + host

my_switch = Node(host_url)
result = my_switch.methods.Login(username,password).POST()
#if result.status_code != requests.codes.ok:
   #break()

mit = my_switch.mit
lldp_neighbors = mit.GET(**options.subtreeClass('lldpAdjEp'))
for lldp_neighbor in lldp_neighbors:
   dn = lldp_neighbor.Dn
   lldp_if = dn[dn.find('[')+len('['):dn.rfind(']')]
   sysDesc = lldp_neighbor.sysDesc
   if 'eth' in lldp_if:
     if 'Linux' in sysDesc:
        print ('We will set ' + lldp_if + ' ' + sysDesc)
        mit = my_switch.mit
        if_status = mit.topSystem().interfaceEntity().l1PhysIf(lldp_if)
        if_status.mode = 'trunk'
        if_status.trunkVlans = '1 - 512'
        result_config = if_status.POST()
        if (result_config.status_code == requests.codes.ok):
           print (lldp_if + " has been configured as a trunk")
        else:
           print ('Error configuring '  + lldp_if + ' as trunk')
     else:
       print ('No Linux host found')
