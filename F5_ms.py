# # # # # # # # # # # # # # # # # # # # # #
# F5 Microservice definitie - BEGIN       #
# # # # # # # # # # # # # # # # # # # # # #

import json
import requests

session = requests.Session()
session.trust_env = False
session.verify = False

"""
REST API Defaults
"""
auth = ('admin','abcd1234')
headers = {'Content-Type':'application/json'}

class F5_microservice:

    """
    REST API Call functies: GET, DELETE, POST, PUT, PATCH
    """
    def get(self, url, auth, headers):
        response = session.get(url,auth=auth,headers=headers)
        return response

    def delete(self, url, auth, headers):
        response = session.delete(url,auth=auth,headers=headers)
        return response

    def post(self, url, auth, headers, payload):
        """
        create a resource
        Resource bestaat nog niet
        Maakt resource met nieuw aangeleverde data.
        """
        response = session.post(url,auth=auth,headers=headers,data=payload)
        return response

    def put(self, url, auth, headers, payload):
        """
        create/replace a resource
        Resource bestaat al.
        Vervangt betaande resource met nieuw aangeleverde data. Andere
        data verdwijnt.
        """
        response = session.put(url,auth=auth,headers=headers,data=payload)
        return response

    def patch(self, url, auth, headers, payload):
        """
        update part of a resource
        Resource bestaat al.
        Update betaande resource met nieuw aangeleverde data. Andere
        data blijft bestaan.
        """
        response = session.patch(url,auth=auth,headers=headers,data=payload)
        return response

    """
    Configuratie functies
    """
    def clusterstate(self, bigip_adres):
        """
        Functie die de clusterstate aangeeft
        Invoer  : bigip_adres = management ip adres van het F5 BIGIP device.
        Uitvoer : HA status van het device, active of standby
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/cm/device'
        result = self.get(url,auth,headers)
        lijst = result.json()['items'][0]
        return lijst['failoverState']

    def create_node(self, bigip_adres, partitie, naam, adres, omschrijving):
        """
        Functie om een node aan te maken
        Invoer  : bigip_adres  = management ip adres van het F5 BIGIP device.
                  partitie     = de administratieve partitie in de BIGIP.
                  naam         = de naam van de node in de bigip_adres.
                  adres        = het ip adres van de backend server.
                  omschrijving = Invulling van het description veld.
        Uitvoer : HTTP status code in de response.
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/node/'
        payload = '{ "name" : "' + naam + '",\
                  "partition" : "' + partitie + '",\
                  "address" : "' + adres + '" ,\
                  "description" : "' + omschrijving + '"}'
        response = self.post(url,auth,headers,payload)
        return response.status_code

    def modify_node_description_by_name(self, bigip_adres, partitie, naam,
                                        omschrijving):
        """
        Functie om een node omschrijving aan te passen
        Invoer  : bigip_adres  = management ip adres van het F5 BIGIP device.
                  partitie     = de administratieve partitie in de BIGIP.
                  naam         = de naam van de node in de bigip_adres.
                  omschrijving = Invulling van het description veld.
        Uitvoer : HTTP status code in de response.
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/node/' + \
              '~' + partitie + '~' + naam + '/'
        payload = '{ "description" : "' + omschrijving + '"}'
        response = self.patch(url,auth,headers,payload)
        return response.status_code

    def delete_node_by_name(self, bigip_adres, partitie, naam):
        """
        Functie om een node te verwijderen
        Invoer  : bigip_adres  = management ip adres van het F5 BIGIP device.
                  partitie     = de administratieve partitie in de BIGIP.
                  naam         = de naam van de node in de bigip_adres.
        Uitvoer : HTTP status code in de response.
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/node/' + \
              '~' + partitie + '~' + naam + '/'
        response = self.delete(url,auth,headers)
        return response.status_code

    def set_node_disabled_by_name(self, bigip_adres, partitie, naam, disabled):
        """
        Functie om een node te verwijderen
        Invoer  : bigip_adres  = management ip adres van het F5 BIGIP device.
                  partitie     = de administratieve partitie in de BIGIP.
                  naam         = de naam van de node in de bigip_adres.
                  disabled     = Disable node (True) of enable node (False).
        Uitvoer : HTTP status code in de response.
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/node/' + \
              '~' + partitie + '~' + naam + '/'
        if disabled:
            payload = '{ "session" : "user-disabled",\
                        "state" : "user-down"}'
        else:
            payload = '{ "session" : "user-enabled",\
                        "state" : "user-up"}'
        response = self.patch(url,auth,headers,payload)
        return response.status_code

    def create_pool(self, bigip_adres, partitie, naam, omschrijving,
                    lb_method, health_mon):
        """
        Functie om een pool aan te maken
        Invoer  : bigip_adres  = management ip adres van het F5 BIGIP device.
                  partitie     = de administratieve partitie in de BIGIP.
                  naam         = de naam van de node in de bigip_adres.
                  omschrijving = Invulling van het description veld.
                  lb_method    = load balance methode:
                                 -
        Uitvoer : HTTP status code in de response.
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/pool/'
        lb_mode = lb_method
        monitor = health_mon
        payload = '{ "name" : "' + naam + '",\
                  "partition" : "' + partitie + '",\
                  "description" : "' + omschrijving + '",\
                  "loadBalancingMode" : "' + lb_mode + '",\
                  "monitor" : "' + monitor + '"}'
        response = self.post(url,auth,headers,payload)
        return response.status_code

    def modify_pool_description_by_name(self, bigip_adres, partitie, naam,
                                        omschrijving, lb_method, health_mon):
        """
        Functie om een pool omschrijving aan te passen
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/pool/' + \
              '~' + partitie + '~' + naam + '/'
        lb_mode = lb_method
        monitor = health_mon
        payload = '{ "description" : "' + omschrijving + '",\
                  "loadBalancingMode" : "' + lb_mode + '",\
                  "monitor" : "' + monitor + '"}'
        response = self.patch(url,auth,headers,payload)
        return response.status_code

    def delete_pool_by_name(self, bigip_adres, partitie, naam):
        """
        Functie om een pool te verwijderen
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/pool/' + \
              '~' + partitie + '~' + naam + '/'
        response = self.delete(url,auth,headers)
        return response.status_code

    def add_node_to_pool(self, bigip_adres, partitie,
                         pool_naam, node_naam, port):
        """
        Functie om een node aan een pool te koppelen
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/pool/' + \
        '~' + partitie + '~' + pool_naam + '/members'
        payload = '{ "name" : "' + node_naam + ':' + port +'",\
                  "partition" : "' + partitie + '"}'
        response = self.post(url,auth,headers,payload)
        return response.status_code

    def create_vip(self, bigip_adres, partitie, naam, omschrijving,
                   ip_adres, port, protocol):
        """
        Functie om een vip aan te maken
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/virtual/'
        payload = '{ "name" : "' + naam + '",\
                  "partition" : "' + partitie + '",\
                  "description" : "' + omschrijving + '", \
                  "destination" : "' + ip_adres + ':' + port +'", \
                  "ipProtocol" : "' + protocol + '"}'
        response = self.post(url,auth,headers,payload)
        return response.status_code

    def modify_vip_description_by_name(self, bigip_adres, partitie, naam,
                                        omschrijving):
        """
        Functie om een vip omschrijving aan te passen
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/virtual/' + \
              '~' + partitie + '~' + naam + '/'
        payload = '{ "description" : "' + omschrijving + '"}'
        response = self.patch(url,auth,headers,payload)
        return response.status_code

    def modify_vip_persistence_by_name(self, bigip_adres, partitie, naam,
                                        persist, persist_partition):
        """
        Functie om de vip persistence aan te passen
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/virtual/' + \
              '~' + partitie + '~' + naam + '/'
        payload = '{ "persist" : [{"name":"' + persist + '", \
                                "partition" : "' + persist_partition + '"}]}'
        response = self.patch(url,auth,headers,payload)
        return response.status_code

    def add_pool_to_vip(self, bigip_adres, partitie, vip_naam, pool_naam):
        """
        Functie om een pool aan een vip te koppelen
        """
        url = 'https://' + bigip_adres + '/mgmt/tm/ltm/virtual/' + \
        '~' + partitie + '~' + vip_naam + '/'
        payload = '{ "pool" : "/' + partitie + '/' + pool_naam + '"}'
        response = self.patch(url,auth,headers,payload)
        return response.status_code


# # # # # # # # # # # # # # # # # # # # # #
# F5 Microservice definitie - EINDE       #
# # # # # # # # # # # # # # # # # # # # # #
