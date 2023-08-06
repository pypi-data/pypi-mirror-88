# Python edgegrid module
""" Copyright 2015 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.

 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import sys
import os
import requests
import logging
import json
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from .http_calls import EdgeGridHttpCaller
if sys.version_info[0] >= 3:
    # python3
    from urllib import parse
else:
    # python2.7
    import urlparse as parse

logger = logging.getLogger(__name__)

#edgerc = EdgeRc('/Users/apadmana/.edgerc')
section = 'default'
debug = False
verbose = False
#baseurl_prd = 'https://%s' % edgerc.get(section, 'host')
#session = requests.Session()
#session.auth = EdgeGridAuth.from_edgerc(edgerc, section)
#session.headers.update({'User-Agent': "AkamaiCLI"})
#prdHttpCaller = EdgeGridHttpCaller(session, debug, verbose, baseurl_prd)



class ChinaCDNManager():
    def __init__(self,edgercLocation=None,accountSwitchKey=None):
        self.icp_info = ''
        self._edgerc = ''
        self._prdHttpCaller = ''
        self._session = ''
        self._baseurl_prd = ''
        self._host = ''
        self._icp_info = ''
        self._icp_entities_info = ''
        self.accountSwitchKey = ''
        self._edgehostnames = ''
        self._groups = ''
        self._appmapping = ''
        self._legalmapping = ''

        self._edgerc = EdgeRc(edgercLocation)
        self._host = self._edgerc.get(section, 'host')
        self._baseurl_prd = 'https://%s' %self._host
        self._session = requests.Session()
        self._session.auth = EdgeGridAuth.from_edgerc(self._edgerc, section)
        self._session.headers.update({'User-Agent': "AkamaiCLI"})
        self._prdHttpCaller = EdgeGridHttpCaller(self._session, debug, verbose, self._baseurl_prd)

        icpinfoEndPoint = "/chinacdn/v1/icp-numbers"
        if accountSwitchKey:
            self.accountSwitchKey = accountSwitchKey
            params = {'accountSwitchKey':accountSwitchKey}
            headers = {"Accept": "application/vnd.akamai.chinacdn.icp-numbers.v1+json"}
            self._icp_info = self._prdHttpCaller.getResult(icpinfoEndPoint,headers,params)
        else:
            self._icp_info = self._prdHttpCaller.getResult(icpinfoEndPoint,headers)

        icpholdingEntitiesEndPoint = "/chinacdn/v1/icp-holding-entities"
        if accountSwitchKey:
            self.accountSwitchKey = accountSwitchKey
            params = {'accountSwitchKey':accountSwitchKey}
            headers = {"Accept": "application/vnd.akamai.chinacdn.icp-holding-entities.v1+json"}
            self._icp_entities_info = self._prdHttpCaller.getResult(icpholdingEntitiesEndPoint,headers,params)
        else:
            self._icp_entities_info = self._prdHttpCaller.getResult(icpholdingEntitiesEndPoint,headers)

        edgeHostNamesEndPoint = "/chinacdn/v1/edge-hostnames"
        if accountSwitchKey:
            self.accountSwitchKey = accountSwitchKey
            params = {'accountSwitchKey':accountSwitchKey}
            headers = {"Accept": "application/vnd.akamai.chinacdn.edge-hostnames.v2+json"}
            self._edgehostnames = self._prdHttpCaller.getResult(edgeHostNamesEndPoint,headers,params)
        else:
            self._edgehostnames = self._prdHttpCaller.getResult(edgeHostNamesEndPoint,headers)

        groupsEndPoint = "/chinacdn/v1/groups"
        if accountSwitchKey:
            self.accountSwitchKey = accountSwitchKey
            params = {'accountSwitchKey':accountSwitchKey}
            headers = {"Accept": "application/vnd.akamai.chinacdn.groups.v1+json"}
            self._groups = self._prdHttpCaller.getResult(groupsEndPoint,headers,params)
        else:
            self._groups = self._prdHttpCaller.getResult(groupsEndPoint,headers)

        cwd = os.path.dirname(os.path.abspath(__file__))
        app_file = os.path.join(cwd, 'application_type.json')
        legal_file = os.path.join(cwd, 'legaltype.json')
        with open(app_file) as json_file:
            self._appmapping = json.load(json_file)

        with open(legal_file) as json_file:
            self._legalmapping = json.load(json_file)

        return None

    def getICPEntities(self):
        for entities in self._icp_entities_info['icpHoldingEntities']:
            for key in self._legalmapping:
                if self._legalmapping[key] == entities['businessClassification']:
                    entities['BusinessName'] = key
                    break
        return self._icp_entities_info

    def getICPNumbers(self):
        return self._icp_info

    def getEdgeHostNames(self):
        return self._edgehostnames

    def getGroups(self):
        return self._groups

    def getProperties(self):
        listPropertiesEndPoint = '/chinacdn/v1/property-hostnames'
        headers = {"Accept": "application/vnd.akamai.chinacdn.property-hostnames.v1+json"}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            properties_info = self._prdHttpCaller.getResult(listPropertiesEndPoint,headers,params)
        else:
            properties_info = self._prdHttpCaller.getResult(listPropertiesEndPoint,headers)
        return properties_info

    def getPropertyInfo(self,hostname):
        getPropertyInfoEndPoint = '/chinacdn/v1/property-hostnames/{hostname}'.format(hostname=hostname)
        headers = {"Accept": "application/vnd.akamai.chinacdn.property-hostname.v1+json"}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            property_info = self._prdHttpCaller.getResult(getPropertyInfoEndPoint,headers,params)
        else:
            property_info = self._prdHttpCaller.getResult(getPropertyInfoEndPoint,headers)
        for key in self._appmapping:
            if self._appmapping[key] == property_info['serviceCategory']:
                property_info['serviceCategoryName'] = key
                break
        return property_info

    def getDeProvisionPolicy(self,edgeHostname):
        getDeProvisionPolicyEndPoint = '/chinacdn/v1/edge-hostnames/{edgeHostname}/deprovision-policy'.format(edgeHostname=edgeHostname)
        headers = {"Accept": "application/vnd.akamai.chinacdn.deprovision-policy.v1+json"}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            deprovision_policy_info = self._prdHttpCaller.getResult(getDeProvisionPolicyEndPoint,headers,params)
        else:
            deprovision_policy_info = self._prdHttpCaller.getResult(getDeProvisionPolicyEndPoint,headers)
        return deprovision_policy_info

    def specifyDeProvisionPolicy(self,edgeHostname):
        specifyDeProvisionPolicyEndPoint = '/chinacdn/v1/edge-hostnames/{edgeHostname}/deprovision-policy'.format(edgeHostname=edgeHostname)
        headers = {"Accept": "application/vnd.akamai.chinacdn.deprovision-policy.v1+json",
                   "Content-Type":"application/vnd.akamai.chinacdn.deprovision-policy.v1+json"}

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            specifydeprovision_policy_info = self._prdHttpCaller.putResult(specifyDeProvisionPolicyEndPoint,headers,params)
        else:
            specifydeprovision_policy_info = self._prdHttpCaller.putResult(specifyDeProvisionPolicyEndPoint,headers)
        return specifydeprovision_policy_info

    def getProvisionStateChange(self,hostname,changeId):
        getProvisionStateChangeEndPoint = '/chinacdn/v1/property-hostnames/{hostname}/provision-state-changes/{changeId}'.format(hostname=hostname,changeId=changeId)
        headers = {"Accept": "application/vnd.akamai.chinacdn.provision-state-changes.v1+json"}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            state_change_info = self._prdHttpCaller.getResult(getProvisionStateChangeEndPoint,headers,params)
        else:
            state_change_info = self._prdHttpCaller.getResult(getProvisionStateChangeEndPoint,headers)
        return state_change_info

    def getcurrentProvisionStateChange(self,hostname):
        getcurrentProvisionStateChangeEndPoint = '/chinacdn/v1/property-hostnames/{hostname}/provision-state-changes/current'.format(hostname=hostname)
        headers = {"Accept": "application/vnd.akamai.chinacdn.provision-state-changes.v1+json"}
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            currentstate_change_info = self._prdHttpCaller.getResult(getcurrentProvisionStateChangeEndPoint,headers,params)
        else:
            currentstate_change_info = self._prdHttpCaller.getResult(getcurrentProvisionStateChangeEndPoint,headers)
        return currentstate_change_info

    def getProvisionStatus(self,status_filter=None):
        getProvisionStatusEndPoint = '/chinacdn/v1/current-provision-states'
        headers = {"Accept": "application/vnd.akamai.chinacdn.provision-states.v1+json"}
        if status_filter:
            if status_filter in ['WHITELISTED','DEPROVISIONED','PROVISIONED']:
                params = {}
                params["provisionState"] = status_filter
            else:
                error_json = {"Status":"Invalid Filter"}
                return error_json

            if self.accountSwitchKey:
                params['accountSwitchKey'] = self.accountSwitchKey
            properties_info = self._prdHttpCaller.getResult(getProvisionStatusEndPoint,headers,params)

        else:
            if self.accountSwitchKey:
                params = {'accountSwitchKey':self.accountSwitchKey}
                properties_info = self._prdHttpCaller.getResult(getProvisionStatusEndPoint,headers,params)
            else:
                properties_info = self._prdHttpCaller.getResult(getProvisionStatusEndPoint,headers)

        return properties_info

    def createPropertyHostname(self,hostname,icpNumberId,serviceCategoryName,groupId):
        createPropertiesEndPoint = '/chinacdn/v1/property-hostnames/' +hostname
        headers = {"Accept": "application/vnd.akamai.chinacdn.property-hostname.v1+json",
                   "Content-Type":"application/vnd.akamai.chinacdn.property-hostname.v1+json"}

        create_body = {}
        create_body['hostname'] = hostname
        create_body['icpNumberId'] = icpNumberId
        create_body['serviceCategory'] = self._appmapping[serviceCategoryName]

        jsondata = json.dumps(create_body,sort_keys=False)

        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey,
                      'groupId':groupId}
            create_propertyInfo = self._prdHttpCaller.putResult(createPropertiesEndPoint,jsondata,headers,params)
        else:
            params = {'groupId':groupId}
            create_propertyInfo = self._prdHttpCaller.putResult(createPropertiesEndPoint,jsondata,headers,params)
        return create_propertyInfo

    def whiteList(self,hostname):
        whiteListEndPoint = '/chinacdn/v1/property-hostnames/' + hostname + '/provision-state-changes'
        headers = {"Accept": "application/vnd.akamai.chinacdn.provision-state-change.v1+json;charset=UTF-8",
                  "Content-Type":"application/vnd.akamai.chinacdn.provision-state-change.v1+json;charset=UTF-8"}

        whitelist_body = {}
        whitelist_body['hostname'] = hostname
        whitelist_body['targetState'] = "WHITELISTED"
        whitelist_body['sendEmail'] = True

        json_data = json.dumps(whitelist_body,sort_keys=False)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,version_info = self._prdHttpCaller.postResult(whiteListEndPoint,json_data,headers,params)
        else:
            status,version_info = self._prdHttpCaller.postResult(whiteListEndPoint,json_data,headers)

        return version_info
