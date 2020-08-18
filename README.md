# nxos-programmability

This repository contains example scripts written in Python 3.0 that work with Cisco Nexus 9000 Switches. The scripts leverage Open NX-OS capabilities on the Nexus 9000. These examples assume a minimum software release of 9.3(5) on the Nexus switches.


PyDME

PyDME is tool that provides a Python abstraction using the Cisco Data Management Engine (DME) and REST API methods. It provides API constructs to access the switch and configure it. The library is available at the repository https://github.com/CiscoDevNet/pydme.

To use PyDME, install the library onto a host that has connectivity to the switches in question. Then setup a simple script in Python such as the example here to perform the required task. The script runs on the host and uses the PyDME library to configure switches and retrieve configuration and operational data from them using REST methods.

The example pyDME-neighbor-trunk.py uses the PyDME framework for network automation that is based on the Data Management Engine (DME). We would like to detect Linux hosts connected to a switch and automatically configure the associated ports using a pre-defined template. In this scenario, we parse through the LLDP neighbors of a switch. If we find a Linux host attached to an ethernet port, we configure that port as a trunk. We use the DME model reference to identify which model to use:
https://developer.cisco.com/site/nxapi-dme-model-reference-api/?version=9.3(5)




cisco-gnmi

This is a library that wraps gNMI implementation for ease of implementation on a gNMI client using Python scripts.
https://github.com/cisco-ie/cisco-gnmi-python

The example script lldp-gnmi-getpython.py uses the cisco-gnmi library to perform Capabilities, Get and Set operations on a Cisco Nexus switch using gNMI and OpenConfig. The script first applies a gNMI Capabilities method to check if the OpenConfig model for LLDP is supported on the switch. Next, we do a gNMI Get to retrieve the state of LLDP neighbors on the switch. With this information, we can extract the interfaces where a Linux host is detected and do a gNMI Set to set our interfaces with “switchport mode trunk”. 




More information about these examples can be found in the article below:
https://blogs.cisco.com/datacenter/network-automation-and-the-ingenuity-of-data-models



