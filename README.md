# nxos-programmability

This repository contains example scripts written in Python 3.0 that work with Cisco Nexus 9000 Switches. The scripts leverage Open NX-OS capabilities on the Nexus 9000. These examples assume a minimum software release of 9.3(5) on the Nexus switches.


PyDME
-----------------------------

PyDME is tool that provides a Python abstraction using the Cisco Data Management Engine (DME) and REST API methods. It provides API constructs to access the switch and configure it. The library is available at the repository https://github.com/CiscoDevNet/pydme.

To use PyDME, install the library onto a host that has connectivity to the switches in question. Then setup a simple script in Python such as the example here to perform the required task. The script runs on the host and uses the PyDME library to configure switches and retrieve configuration and operational data from them using REST methods.

The example pyDME-neighbor-trunk.py uses the PyDME framework for network automation that is based on the Data Management Engine (DME). We would like to detect Linux hosts connected to a switch and automatically configure the associated ports using a pre-defined template. In this scenario, we parse through the LLDP neighbors of a switch. If we find a Linux host attached to an ethernet port, we configure that port as a trunk. We use the DME model reference to identify which model to use:
https://developer.cisco.com/site/nxapi-dme-model-reference-api/?version=9.3(5)

More information about these examples can be found in the article below:

Network Automation and the Ingenuity of Data Models
https://blogs.cisco.com/datacenter/network-automation-and-the-ingenuity-of-data-models

gNMI Automation (Get and Set)
-----------------------------

cisco-gnmi is a library that wraps gNMI implementation for ease of implementation on a gNMI client using Python scripts.
https://github.com/cisco-ie/cisco-gnmi-python

The example script lldp-gnmi-getpython.py uses the cisco-gnmi library to perform gNMI Capabilities, Get and Set operations on a Cisco Nexus switch using gNMI and OpenConfig. The script first applies a gNMI Capabilities method to check if the OpenConfig model for LLDP is supported on the switch. Next, we do a gNMI Get to retrieve the state of LLDP neighbors on the switch. With this information, we can extract the interfaces where a Linux host is detected and do a gNMI Set to set our interfaces with “switchport mode trunk”. 


More information about these examples can be found in the article and whitepaper below:
Network Automation and the Ingenuity of Data Models
https://blogs.cisco.com/datacenter/network-automation-and-the-ingenuity-of-data-models

Data Center Telemetry and Network Automation Using gNMI and OpenConfig White Paper
https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-744191.html

Netconf Event Notifications
-----------------------------

NETCONF Event Notifications can be used to subscribe to system events on a switch or switches. Customers who are migrating from legacy SNMP-based monitoring tools can now  achieve functionality similar to SNMP traps with NETCONF notifications which uses YANG-based models. NETCONF Event Notifications are supported with OpenConfig starting with NX-OS Release 9.3(5).

The script netconf-notifications-bgp.py is used to get NETCONF event notifications for the total number of BGP prefixes in the system. The script first connects to a switch using NETCONF. We then specify an xpath within the create-subscription method. The YANG model being subscribed to could either use the device YANG or OpenConfig data model. When the switch has a system event within this model tree, a NETCONF event notification is generated. We then wait for a notification and display it. The example uses the xpath below, to subscribe to notifications in the total number of BGP prefixes:
xpath = "/network-instances/network-instance/protocols/protocol/bgp/global/state/total-prefixes"

Other examples of xpath at container level (for interfaces):

Here is an example of xpath at leaf level (specific interface):


More information on this feature can be found in the article below:
Telemetry in Action: NETCONF and gNMI with a Custom-Built Collector!
https://blogs.cisco.com/datacenter/telemetry-in-action-netconf-and-gnmi-with-a-custom-built-collector


gNMI Telemetry (Subscribe)
----------------------------

gNMI support on the Nexus 9000 Series switches includes the four gRPC operations: Capabilities, Get, Set and Subscribe. An automation example using Get and Set operations was shown in another example (see section on gNMI Automation). The script gnmi-subscribe-bgp.py includes two main modules:
1. gNMI Capabilities and gNMI Subscribe
The script consists of connecting to the Nexus 9000 Series switch using gNMI. This includes the switch IP address, username, password, gRPC port number and gNMI certificate. We are interested in subscribing to dial-in telemetry data using gNMI for the total number of BGP prefixes in the system, using OpenConfig as the underlying data model. We first use gNMI capabilities  to check whether the OpenConfig model for network-instance is supported. We then use gNMI Subscribe to subscribe to the following xpath and sample every 10 seconds.
xpath = "/network-instances/network-instance/protocols/protocol/bgp/global/state/total-prefixes"

2. A custom-built telemetry collector
Uses rrdtool to create a database for telemetry data and graph it using a PNG. Uses lighttpd to render the graph in an HTML page.

More information about this can be found in the articles and whitepaper below:
Telemetry in Action: NETCONF and gNMI with a Custom-Built Collector!
https://blogs.cisco.com/datacenter/telemetry-in-action-netconf-and-gnmi-with-a-custom-built-collector

Hot off the press: Introducing OpenConfig Telemetry on NX-OS with gNMI and Telegraf!
https://blogs.cisco.com/datacenter/hot-off-the-press-introducing-openconfig-telemetry-on-nx-os-with-gnmi-and-telegraf

Data Center Telemetry and Network Automation Using gNMI and OpenConfig White Paper
https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-744191.html
