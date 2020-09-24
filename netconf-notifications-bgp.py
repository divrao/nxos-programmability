#!/usr/bin/env python
  
import ncclient.manager
from ncclient.xml_ import to_ele
from ncclient import manager, operations
from getpass import getpass

#Initialize switch credentials for a connection
switchIP = input("Switch IP Address: ")
user = input("Username: ")
pwd = getpass()
#switchIP = "192.168.1.1"
#pwd = "abcxyz12345"

m = ncclient.manager.connect_ssh(host=switchIP, port=830,
                                 username=user,
                                 password=pwd,
                                 hostkey_verify=False,
                                 timeout=2000)

print ("Session id is : ", m.session_id)

#create-subscription to subscribe to BGP total prefixes in the OpenConfig network-instance model
create_filter = """
<create-subscription xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
    <stream>NETCONF</stream>
    <filter xmlns:ns1="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
         <network-instances xmlns="http://openconfig.net/yang/network-instance">
            <network-instance>
                <protocols>
                    <protocol>
                        <bgp>
                            <global>
                                <state>
                                   <total-prefixes> </total-prefixes>
                                </state>
                            </global>
                        </bgp>
                    </protocol>
                </protocols>
            </network-instance>
        </network-instances>
    </filter>
</create-subscription>
"""

print("\nThe create-subscription request is : ", create_filter)
create_reply = m.dispatch(to_ele(create_filter))
print("\nResponse for <create-subscription> : ")
print(create_reply)
print("-----------------------")

# Receiving event notifications while subscribed YANG model
while m.connected:
    response = 'notif_resp'
    print("Receiving notifications")
    n = m.take_notification(timeout = 10)
    if (n != None):
        print(n.notification_xml)
    print("-----------------------")
