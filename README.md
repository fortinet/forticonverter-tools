# FortiConverter tools
```
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    Usage: py fcon_meraki_backup.py [Meraki_API_key]
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
```
The **fcon_meraki_backup.py** script fetches configurations from Cisco Meraki and generates a backup file which can be input to the FortiConverter tool.

### Usage

#### Prerequisites

1. Install Python 3.7 or newer on the computer.

1. (Optional) Run Python in a virtual environment:

	1. Install Python virtual environment by command:
	
		`pip install virtualenv`

	1. Create virtual environment by command:
	
		`virtualenv [environment name]`

	1. Activate virtual environment by commands:
	
		`cd [environment name]`
		`Scripts\activate`

1. Make sure the computer has network connection and run the command below to install Meraki Dashboard API Python library:

	`pip install --upgrade meraki`

#### Input
- `[Meraki_API_key]` (Required)
The API key to access the Cisco Meraki instance. Please follow the steps in the document [Cisco Meraki Dashboard API](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API) to generate an API key.

- When the script is running, it will fetch the organizations and networks that can be accessed by the API key. Please select the organization and the network you would like to backup. If there is only one organization or one network, the script will select it automatically.

#### Output

The script generates a backup file in JSON format which includes the following content:

- Ports and VLANs
- Policy objects & groups
- Layer 3 outbound rules
- 1:1 NAT rules
- 1:Many NAT rules

### Support
Fortinet-provided scripts in this and other GitHub projects do not fall under the regular Fortinet technical support scope and are not supported by FortiCare Support Services. For direct issues, please contact `fconvert_feedback@fortinet.com`.

### License
[License](https://github.com/fortinet/forticonverter-tools/blob/main/LICENSE) © Fortinet Technologies. All rights reserved.
