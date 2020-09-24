import sys
from getpass import getpass
import json
import cisco_gnmi
from pprint import pprint
from google.protobuf import json_format
import base64
import logging
import tempfile, rrdtool

class configFunctions():

# Initialize switch credentials for gNMI including gRPC port and certificate
   def init(self):
      target = input("Switch/Port: ")
      username = input("Username: ")
      password = getpass()
      #target = '192.168.1.1:50051'
      #username = 'admin'
      #password = 'abcxyz123'
      client = (
         cisco_gnmi.ClientBuilder(target)
         .set_os('NX-OS')
         .set_secure_from_file('./gnmi.pem')
         .set_ssl_target_override()
         .set_call_authentication(username, password)
         .construct()
      )
      return client

# gNMI Capabilities to check if OpenConfig model for network-instance is supported on the switch
   def net_capability(self, nx_os):
       gnmi_json_capabilities = json.loads(json_format.MessageToJson(nx_os.capabilities()))
       models_list = gnmi_json_capabilities['supportedModels']
       list_len = len (models_list)
       for i in range(list_len):
         model = models_list[i]
         if 'network-instance' in model['name']:
            return (True)
       return (False)

   def get_gnmi_json_val(self, nx_os, xpath, dt):
       gnmi_pb2 = nx_os.get_xpaths(xpath, dt)
       val_str = gnmi_pb2.notification[0].update[0].val.json_val.decode('utf-8')
       if val_str != "":
          val_json = json.loads(val_str)
          return (val_json)
       else:
           return (val_str)

# gNMI Subscribe using OpenConfig model for network-instance to subscribe to BGP total prefixes
   def net_subscribe(self, nx_os):
       xpath = "/network-instances/network-instance/protocols/protocol/bgp/global/state/total-prefixes"
       request_mode = "STREAM"
       sub_mode = "SAMPLE"
       interval = 10
       encoding = "JSON"
       no_stop = True
       for response in nx_os.subscribe_xpaths(xpath, request_mode, sub_mode, encoding):
          if response.sync_response and not no_stop:
            logging.warning("Stopping on sync_response.")
            break
          print ('This is the raw output')
          pprint(response.update)
          message_json = json.loads(json_format.MessageToJson(response.update))
          print ('This is the output convert to JSON')
          pprint (message_json)
          if 'update' in message_json and 'val' in message_json['update'][0]:
             json_val_str = base64.b64decode(message_json['update'][0]['val']['jsonVal']).decode('utf-8')
             json_val = json.loads(json_val_str)
             print ('This is the Value decoded') 
             pprint (json_val)
             bgp_prefixes = json_val['network-instance'][0]['protocols']['protocol'][0]['bgp']['global']['state']['total-prefixes'] 
             print ('Total BGP prefixes: ' + str(bgp_prefixes))
             self.update_rrd(bgp_prefixes)
             self.display_rrd()

# Using rrdtool to graph the telemetry data 
   def create_rrd(self):
      create = rrdtool.create('bgp.rrd', '--step', '10', '--start', '0',
      'DS:prefixes:GAUGE:25:0:U',
      'RRA:LAST:0:1:2000')
      if create:
         print (rrdtool.error())
      else:
         return create

   def update_rrd(self, bgp_prefixes):
    update = rrdtool.update('bgp.rrd','N:' + str(bgp_prefixes));
    if update:
       print (rrdtool.error())

   def display_rrd(self):
      graph = rrdtool.graph( "bgp.png", "--start", "-5h", "--vertical-label=Prefixes", "--title=BGP Prefixes",
      "DEF:bgp_pref=bgp.rrd:prefixes:AVERAGE",
      "AREA:bgp_pref#00FF00:Prefixes",
      "COMMENT:Time"
      )

if  __name__ == "__main__":
    config_script = configFunctions()
    config_script.create_rrd()
    client = config_script.init()
    if config_script.net_capability(client):
       print ('openconfig-network-instance model for network-instances supported')
       net_list = config_script.net_subscribe(client)
       #pprint (net_list)
    else:
       print ('openconfig-network-instance model not supported on device')
    
