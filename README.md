# Backup Script for Cisco Meraki

The **fcon_meraki_backup.py** script fetches configurations from Cisco Meraki and generates a backup file which can be input to the FortiConverter tool.

### Usage

#### Prerequisites

1. Install Python 3.7 or newer on the computer.

1. (Optional) Run Python in a virtual environment:

	1. Install Python virtual environment by command:
	
		`pip install virtualenv`

	1. Create virtual environment by command:
	
		`virtualenv [environment_name]`

	1. Activate virtual environment by commands:
	
		`cd [environment_name]`
		`Scripts\activate`

1. Make sure the computer has network connection and run the command below to install Meraki Dashboard API Python library:

	`pip install --upgrade meraki`

#### Backup Steps

1. In a Windows command prompt, run:

	`py fcon_meraki_backup.py [Meraki_API_key]` 
 
	- `[Meraki_API_key]`
		The API key to access the Cisco Meraki instance. Please follow the steps in the document [Cisco Meraki Dashboard API](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API) to generate an API key.

1. The script will fetch the organizations that can be accessed by the API key. Please select the organization you would like to access. If there is only one organization, the script will select it automatically.

1. The script will then fetch the networks under the selected organization. Please select the network you would like to backup. If there is only one network, the script will select it automatically.

1. The script will fetch the information of the selected network and generate a backup file.

#### Output

The script generates a backup file in JSON format which includes the following content:

- Ports and VLANs
- Policy objects and groups
- Layer 3 outbound rules
- 1:1 NAT rules
- 1:Many NAT rules


# Backup Script for Lucent Brick

The **extractConfig.pl** script extracts configurations from Alcatel-Lucent Brick which FortiConverter tool requires to do the conversion.

### Usage

Visit the [Admin Guide](https://docs.fortinet.com/document/forticonverter/7.0.2/online-help/126115/saving-the-alcatel-lucent-source-configuration-file) of FortiConverter for an example backup procedure.

#### Prerequisites

1. Install Perl 5 on the computer.

1. The machine needs to have the Alcatel-Lucent CLI administration tools installed.

#### Backup Steps

1. Log on to an SMS administrator account that has access to the target group. In a Windows command prompt, run: 

	`lsmslogon [admin] [output_directory]`

	- `[admin]` 
		The administrator’s Admin ID
	
	- `[output_directory]`
		The directory in which the LSMS will store any zone assignment or policy files. This directory is created in the directory in which you installed the LSMS software. To specify a different directory, supply the complete path.

1. In the command line, run the script:

	`extractConfig.pl [group_name] [object_type]`

	- `[group_name]`
	The target group name.
	
	- `[object_type]`
	The object type you would like to take backup. It can be the following values:
	
		- `brick`
		The config under path `[group_name]/Device/Brick` in the group.
	
		- `brickruleset`
		The config under path `[group_name]/Device/Brick Zone Rulesets` in the group.
	
		- `hostgroup`
		The config under path `[group_name]/Device/Host Groups` in the group.
		
		- `servicegroup`
		The config under path `[group_name]/Device/Service Groups` in the group.
	
		- `all`
		Take the backup of all kinds of the objects listed above.

1. The script will show its progress as it extracts each objects. When it is completed, the output will be saved in the specified `[outputDirectory]`.

#### Output

In `[output_directory]`, a directory is created for each category, and each object in a category is saved to its own text file. Please compress all the directories into a ZIP file and use the ZIP as the input of FortiConverter.

### Support
Fortinet-provided scripts in this and other GitHub projects do not fall under the regular Fortinet technical support scope and are not supported by FortiCare Support Services. For direct issues, please contact `fconvert_feedback@fortinet.com`.

### License
[License](https://github.com/fortinet/forticonverter-tools/blob/main/LICENSE) © Fortinet Technologies. All rights reserved.
