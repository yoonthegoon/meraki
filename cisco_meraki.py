import json
import meraki


DASHBOARD = meraki.DashboardAPI(json.load(open('config.json'))["MERAKI_KEY"])


def get_organization_id():
    organizations = DASHBOARD.organizations.getOrganizations()
    for organization in organizations:
        print(f'\nName: {organization["name"]}\n\tID: {organization["id"]}')
    return organizations


def get_network_id(organization_id: str):
    organization_id = str(organization_id)
    networks = DASHBOARD.organizations.getOrganizationNetworks(organization_id)
    for network in networks:
        print(f'\nName: {network["name"]}\n\tID: {network["id"]}')
    return networks


def update_device_access_points(device, address: str = None, lat: float = None, lng: float = None):
    if address:
        DASHBOARD.devices.updateDevice(
            device['serial'],
            address=address,
            lat=lat if lat else None,
            lng=lng if lng else None
        )
    
    if device['model'] in ('MR42', 'MR52', 'MR46') and 'name' in device:
        return {'name': device['name'], 'serial': device['serial']}


def update_device_management_interface(school: int, ip: int, access_point):
    DASHBOARD.devices.updateDeviceManagementInterface(
        access_point['serial'],
        wan1={
            'usingStaticIp': True,
            'staticIp': f'10.{school}.254.{ip + 40}',
            'vlan': 2254,
            'staticSubnetMask': '255.255.255.0',
            'staticGatewayIp': f'10.{school}.254.1',
            'staticDns': ['10.0.0.32', '10.0.0.33']
        }
    )


def main(network_id: str, school: int = None, address: str = None, lat: float = None, lng: float = None):
    devices = DASHBOARD.networks.getNetworkDevices(network_id)

    new_devices = [update_device_access_points(device, address, lat, lng) for device in devices]
    
    access_points = []
    for i in new_devices:
        if i != None:
            access_points.append(i)

    access_points.sort(key=lambda ap: ap['name'])

    if school:
        [update_device_management_interface(school, ip, access_point) for ip, access_point in enumerate(access_points)]
    

    # Print all devices
    devices = DASHBOARD.networks.getNetworkDevices(network_id)

    for device in devices:
        print(device)
