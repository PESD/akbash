"""
LDAP/Active Directory Module

Goals:
* Connect to an Active Directory server
* Query the LDAP database to see if a user exists based on Visions ID
* If the user exists, return the AD username
"""

import os
from ldap3 import Server, Connection, ALL, NTLM
from configparser import ConfigParser
from django.conf import settings

# load in private seettings from the ini file
private_config_file = os.environ.get(
    'AKBASH_CONFIG_FILE',
    os.path.join(settings.BASE_DIR, '..', 'akbash_private_settings', 'akbash.ini'))
config = ConfigParser(interpolation=None)
config.read(private_config_file)

# check visions database config for unrecognized options.
for k in config['ldap']:
    if k.upper() in (
        'LDAP_SERVER',
        'LDAP_DOMAIN',
        'LDAP_USER',
        'LDAP_PASSWORD',
        'LDAP_SEARCH_BASE',
    ):
        continue
    else:
        raise KeyError("Unrecognized ldap database option: {}".format(k))

# LDAP constants
LDAP_SERVER = config['ldap']['LDAP_SERVER']
LDAP_DOMAIN = config['ldap']['LDAP_DOMAIN']
LDAP_USER = config['ldap']['LDAP_USER']
LDAP_PASSWORD = config['ldap']['LDAP_PASSWORD']
LDAP_SEARCH_BASE = config['ldap']['LDAP_SEARCH_BASE']
LDAP_DOMAIN_USER = LDAP_DOMAIN + "\\" + LDAP_USER


def get_ad_username_from_visions_id(visions_id):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_DOMAIN_USER, password=LDAP_PASSWORD, authentication=NTLM)
    conn.bind()
    conn.search(
        LDAP_SEARCH_BASE,
        '(&(objectclass=person)(wwwhomepage={})(|(userAccountControl=512)(userAccountControl=66048)))'.format(visions_id),
        attributes=[
            'samaccountname',
        ]
    )
    if conn.entries:
        return conn.entries[0]["sAMAccountName"][0]
    return False
