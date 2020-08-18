import sys
from getpass import getpass
import json
import cisco_gnmi
from pprint import pprint
from google.protobuf import json_format
import base64


update_json = {
               "openconfig-interfaces:interfaces": {
                "interface" : [
                 {
                  "name": "",
                  "ethernet": {
                   "switched-vlan": {
                    "config": {
                     "access-vlan": 1,
                     "interface-mode": "TRUNK",
                     "native-vlan": 1,
                     "trunk-vlans": ["1..4094"]
                    }
                   }
                  }
                 }
                ]
               }
              }

class configFunctions():

   def init(self):
      target = input("Host/Port: ")
      username = input("Username: ")
      password = getpass()
      #target = '192.25.74.84:50051'
      #username = 'admin'
      #password = 'abcxyz12345'
      client = (
         cisco_gnmi.ClientBuilder(target)
         .set_os('NX-OS')
         .set_secure_from_file('./gnmi.pem')
         .set_ssl_target_override()
         .set_call_authentication(username, password)
         .construct()
      )
      return client

   #def show_capabilities(self, nx_os):
      #capabilities = nx_os.capabilities()
      #pprint (capabilities)

   def lldp_capability(self, nx_os):
       gnmi_pb2_capabilities = nx_os.capabilities()
       gnmi_json_capabilities_txt = json_format.MessageToJson(gnmi_pb2_capabilities)
       gnmi_json_capabilities = json.loads(gnmi_json_capabilities_txt)
       models_list = gnmi_json_capabilities['supportedModels']
       list_len = len (models_list)
       for i in range(list_len):
         model = models_list[i]
         if 'lldp' in model['name']:
            return (True)
       return (False)

   def get_gnmi_json_val(self, nx_os, xpath, dt):
       gnmi_pb2 = nx_os.get_xpaths(xpath, dt)
       #gnmi_json = json_format.MessageToJson(gnmi_pb2)
       #result_json = json.loads(gnmi_json)
       #val_str =  base64.b64decode(result_json['notification'][0]['update'][0]['val']['jsonVal']).decode('utf-8')
       #print (val_str)
       val_str = gnmi_pb2.notification[0].update[0].val.json_val.decode('utf-8')
       if val_str != "":
          val_json = json.loads(val_str)
          return (val_json)
       else:
           return (val_str)
       #return (val_str)

   def get_lldp_ifs(self, nx_os):
      xpath = "openconfig-lldp:lldp/interfaces/interface/config/name"
      dt = "CONFIG"
      lldp_ifs_json = self.get_gnmi_json_val(nx_os, xpath, dt)
      return (lldp_ifs_json)

   def gnmi_if_set(self, nx_os, interface):
       update_json["openconfig-interfaces:interfaces"]['interface'][0]['name'] = interface
       print ('Configuring ' + interface + ' as trunk')
       set_result = nx_os.set_json(update_json_configs=[update_json])
       pprint (set_result)

   def set_trunk_host(self, nx_os, interfaces):
       dt = "STATE"
       interfaces_len = len(interfaces)
       for i in range(interfaces_len):
          interface = interfaces[i]
          xpath = "openconfig-lldp:lldp/interfaces/interface[name='"+interface+"']/neighbors/neighbor/state/system-description"
          description = self.get_gnmi_json_val(nx_os, xpath, dt)
          #print (description)
          if 'Linux' in description and 'eth' in interface:
              print ('Linux host found on interface: ' + interface)
              self.gnmi_if_set(nx_os, interface)

if  __name__ == "__main__":
    config_script = configFunctions()
    client = config_script.init()
    if config_script.lldp_capability(client):
       print ('openconfig-lldp model supported on device')
       if_list = config_script.get_lldp_ifs(client)
       #print (type(if_list))
       config_script.set_trunk_host(client, if_list)
    else:
       print ('openconfig-lldp model not supported on device')

