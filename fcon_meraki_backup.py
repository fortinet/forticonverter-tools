import json, datetime, sys

def print_python_setup_guide():

    print('''Please follow the steps below to install Meraki Dashboard API Python library:
          
1. Install Python 3.7 or newer on the computer.

2. (Optional) Run Python in a virtual environment:

    1) Install Python virtual environment by command:

        pip install virtualenv

    2) Create virtual environment by command:

        virtualenv [environment name]

    3) Activate virtual environment by commands:

        cd [environment name]
        Scripts\activate

3. Make sure the computer has network connection and run the command below to install Meraki Dashboard API Python library:

    pip install --upgrade meraki''')

def print_api_guide():
    
    print('''Usage: py fcon_meraki_backup.py [Meraki_API_key]

To generate a Meraki API key, please follow the steps in the link below:
    https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API''')

def select_organizations(dashboard):
    
    list_organization = dashboard.organizations.getOrganizations()
    print("The following organizations are fetched by the API key:")
    for idx in range(len(list_organization)):
        organization = list_organization[idx]
        print("{0}.\t{1}: {2}".format(idx+1, organization['id'], organization['name']))

    print("")
    select_organization = None
    if len(list_organization) == 1:
        print('Only one organization is fetched. Selecting "{0}" automatically.'.format(list_organization[0]['name']))
        select_organization = list_organization[0]
    else:
        selected = 0
        while not (0 < selected <= len(list_organization)):
            try:
                selected = int(input("Please select an organization({0}~{1}): ".format(1, len(list_organization))))
            except ValueError:
                print("Invalid input.")
        select_organization = list_organization[selected-1]

    print("")
    return select_organization

def select_network(dashboard, organization):

    list_network = dashboard.organizations.getOrganizationNetworks(organization['id'])
    print('The following networks are fetched from organization "{0}":'.format(organization['name']))
    for idx in range(len(list_network)):
        network = list_network[idx]
        print("{0}.\t{1}: {2}".format(idx+1, network['id'], network['name']))

    print("")
    selected_network = None
    if len(list_network) == 1:
        print('Only one network is fetched. Selecting "{0}" automatically.'.format(list_network[0]['name']))
        selected_network = list_network[0]    
    else:
        selected = 0
        while not (0 < selected <= len(list_network)):
            try:
                selected = int(input("Please select a network({0}~{1}): ".format(1, len(list_network))))
            except ValueError:
                print("Invalid input.")
        selected_network = list_network[selected-1]

    print("")
    return selected_network

def backup_config(dashboard, organization, network):

    org_id = organization['id']
    net_id = network['id']

    config = {}
    config['organizationName'] = organization['name']
    config['organizationId'] = org_id
    config['policyObjects'] = dashboard.organizations.getOrganizationPolicyObjects(org_id)
    config['policyObjectsGroups'] = dashboard.organizations.getOrganizationPolicyObjectsGroups(org_id)
    config['networks'] = []

    network_config = {}
    network_config['networkName'] = network['name']
    network_config['networkId'] = net_id
    
    config_success = False
    try:
        network_config['ports'] = dashboard.appliance.getNetworkAppliancePorts(networkId=net_id)
        config_success = True
    except meraki.APIError as api_error:
        print("An error occurred while retrieving ports: " + get_api_error_message(api_error))
       
    try:
        network_config['vlans'] = dashboard.appliance.getNetworkApplianceVlans(networkId=net_id)
        config_success = True
    except meraki.APIError as api_error:
        print("An error occurred while retrieving VLANs: " + get_api_error_message(api_error))
       
    try:
        network_config['l3FirewallRules'] = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(networkId=net_id)
        config_success = True
    except meraki.APIError as api_error:
        print("An error occurred while retrieving firewall rules: " + get_api_error_message(api_error))
       
    try:
        network_config['oneToOneNat'] = dashboard.appliance.getNetworkApplianceFirewallOneToOneNatRules(networkId=net_id)
        config_success = True
    except meraki.APIError as api_error:
        print("An error occurred while retrieving one-to-one NAT rules: " + get_api_error_message(api_error))
       
    try:
        network_config['oneToManyNat'] = dashboard.appliance.getNetworkApplianceFirewallOneToManyNatRules(networkId=net_id)
        config_success = True
    except meraki.APIError as api_error:
        print("An error occurred while retrieving many-to-one NAT rules: " + get_api_error_message(api_error))
       
    try:
        network_config['staticRoutes'] = dashboard.appliance.getNetworkApplianceStaticRoutes(networkId=net_id)
        config_success = True
    except meraki.APIError as api_error:
        print("An error occurred while retrieving static routes: " + get_api_error_message(api_error))

    if not config_success:
        raise Exception("No config available.")        

    config['networks'].append(network_config)
    return config

def get_api_error_message(api_error):
    if isinstance(api_error.message, str):
        return api_error.message
    elif isinstance(api_error.message, dict) and "errors" in api_error.message:
        return "\n".join(api_error.message["errors"])
    else:
        return str(api_error.message)

if __name__ == "__main__":

    print("Welcome to Meraki config backup tool for FortiConverter.")
    print("")
    try:
        import meraki

        if len(sys.argv) <= 1:
            print_api_guide()
            exit()

        api_key = sys.argv[1]
        dashboard = meraki.DashboardAPI(api_key, print_console = False)
        organization = select_organizations(dashboard)    
        network = select_network(dashboard, organization)
        config = backup_config(dashboard, organization, network)
        backup_name = "meraki_backup_{0}_{1}_{2}.json".format(organization['name'], network['name'], datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        with open(backup_name, 'w') as backup_file:
            json.dump(config, backup_file, indent=2)
        print('Backup config file is saved as "{0}".'.format(backup_name))

    except ImportError:
        print_python_setup_guide()
    except meraki.APIError as api_error:    
        print(get_api_error_message(api_error))
    except Exception as e:
        print(e)

