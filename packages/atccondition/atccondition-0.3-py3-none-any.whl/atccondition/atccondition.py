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

class ATCCondition():
    def __init__(self,edgercLocation,accountSwitchKey=None):
        self._edgerc = ''
        self._prdHttpCaller = ''
        self._session = ''
        self._baseurl_prd = ''
        self._host = ''
        self.accountSwitchKey = ''
        self._hasvaluecondition = ''
        self._hasvaluecondition  = {"condition": {"conditionNodeId": 1,"values": ["HeaderVariable"],
                                        "conditionNode": {"conditionNodeId": 4,"values": ["headerVariableName"],
                                        "conditionNode": {"conditionNodeId": 5,"values": ["has_a_value"],
                                        "conditionNode": {"conditionNodeId": 7,"values": ["begin_with"],
                                        "conditionNode": {"conditionNodeId": 4,"values": ["headerVariableName"] } } } }}}

        self.accountSwitchKey = accountSwitchKey
        self._edgerc = EdgeRc(edgercLocation)
        self._host = self._edgerc.get(section, 'host')
        self._baseurl_prd = 'https://%s' %self._host
        self._session = requests.Session()
        self._session.auth = EdgeGridAuth.from_edgerc(self._edgerc, section)
        self._session.headers.update({'User-Agent': "AkamaiCLI"})
        self._prdHttpCaller = EdgeGridHttpCaller(self._session, debug, verbose, self._baseurl_prd)

    def createCondition(self,conditionJson):
        conditionEndPoint = '/test-management/v2/functional/test-catalog/conditions'
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            status,response = self._prdHttpCaller.postResult(conditionEndPoint,conditionJson,params=params)
        else:
            status,response = self._prdHttpCaller.postResult(conditionEndPoint,conditionJson)
        if status == 400:
            #Already Existing
            if 'existingEntities' in response['errors'][0]:
                return response['errors'][0]['existingEntities'][0]['conditionId']
        elif status == 201:
            return response['conditionId']
        else:
        	failedReason = response['errors'][0]['title']
        	print("CP Code Condition Failed..! Reason: " + failedReason)
        return 0

    def listConditions(self):
        listConditionsEndPoint = "/test-management/v2/functional/test-catalog/conditions"
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            conditionListJson = self._prdHttpCaller.getResult(listConditionsEndPoint,params)
        else:
            conditionListJson = self._prdHttpCaller.getResult(listConditionsEndPoint)
        return conditionListJson

    def deleteCondition(self,conditionId):
        deleteConditionEndPoint = "/test-management/v2/functional/test-catalog/conditions/{conditionId}".format(conditionId=conditionId)
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            deleteConditionJson = self._prdHttpCaller.deleteResult(deleteConditionEndPoint,params)
        else:
            deleteConditionJson = self._prdHttpCaller.deleteResult(deleteConditionEndPoint)
        print(deleteConditionJson)
        return deleteConditionJson

    def deleteAllConditions(self):
        listConditionsEndPoint = "/test-management/v2/functional/test-catalog/conditions"
        if self.accountSwitchKey:
            params = {'accountSwitchKey':self.accountSwitchKey}
            print(params)
            conditionListJson = self._prdHttpCaller.getResult(listConditionsEndPoint,params)
        else:
            conditionListJson = self._prdHttpCaller.getResult(listConditionsEndPoint)
        for condition in conditionListJson:
            print("Deleting:",condition['conditionId'])
            #self.deleteCondition(condition['conditionId'])


    def responseCode(self,responsecodelist):
        responsecode={"condition":{"conditionNodeId":1,
                            "values":["response_code"],
                            "conditionNode":{"conditionNodeId":2,"values":["is_one_of"],
                                            "conditionNode":{"conditionNodeId":3,"values":responsecodelist
                                                            }
                                            }
                            }
                }
        response_code=json.dumps(responsecode)
        return response_code

    def redirect(self,redirect_code_list,location):
        redirect_code = { "condition": { "conditionNodeId": 1,
                                        "values": ["redirect"],
                                        "conditionNode": {"conditionNodeId": 2,"values": ["is_one_of"],
                                        "conditionNode": {"conditionNodeId": 13,"values": redirect_code_list,
                                        "conditionNode": {"conditionNodeId": 18,"values": ["location"],
                                        "conditionNode": {"conditionNodeId": 23,"values": ["is"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [location]}
                        }}}}}}
        redirectresponse_code=json.dumps(redirect_code,indent=4)
        return redirectresponse_code

    def sureroute(self,isenabled):
        value = "is_not_enabled"
        if isenabled == True:
            value = "is_enabled"
        sr_condition = {"condition": {"conditionNodeId": 1,"values": ["sure_route"],
                                        "conditionNode": {"conditionNodeId": 14,"values": [value]}}}
        sr_condition = json.dumps(sr_condition,indent=4)
        return sr_condition

    def tieredDistribution(self,isenabled):
        value = "is_not_enabled"
        if isenabled == True:
            value = "is_enabled"
        td_condition = {"condition": {"conditionNodeId": 1,"values": ["tiered_distribution"],
                                        "conditionNode": {"conditionNodeId": 14,"values": [value]}}}
        td_condition = json.dumps(td_condition,indent=4)
        return td_condition

    def logHeader(self,headerName,isenabled):
        value = "is_not_logged"
        if isenabled == True:
            value = "is_logged"
        if headerName in ['host','referrer','accept_language','user_agent']:
            headerName = headerName + '_header'
            log_condition = {"condition": {"conditionNodeId": 1,"values": ["log_request_details"],
                                                  "conditionNode": {"conditionNodeId": 15,"values": [headerName],
                                                  "conditionNode": {"conditionNodeId": 16,"values": [value]}}}}
            log_condition = json.dumps(log_condition,indent=4)
        return log_condition

    def cookiesLogged(self,isenabled,cookieName=None):
        if isenabled == False:
            value = "not_logged"
            cookie_log_condition = {"condition": {"conditionNodeId": 1,"values": ["log_request_details"],
                                                  "conditionNode": {"conditionNodeId": 15,"values": ["cookies"],
                                                  "conditionNode": {"conditionNodeId": 24,"values": [value]}}}}
        if isenabled == True:
            value = "logged"
            cookie_log_condition = {"condition": {"conditionNodeId": 1,"values": ["log_request_details"],
                                                  "conditionNode": {"conditionNodeId": 15,"values": ["cookies"],
                                                  "conditionNode": {"conditionNodeId": 24,"values": [value],
                                                  "conditionNode": {"conditionNodeId": 17,"values": [cookieName]}}}}}
        cookie_log_condition = json.dumps(cookie_log_condition,indent=4)
        return cookie_log_condition

    def customDataLogged(self,isenabled,customData=None):
        if isenabled == False:
            value = "is_not_logged"
            customdata_log_condition = {"condition": {"conditionNodeId": 1,"values": ["log_request_details"],
                                                  "conditionNode": {"conditionNodeId": 15,"values": ["custom_data"],
                                                  "conditionNode": {"conditionNodeId": 16,"values": [value]}}}}
        if isenabled == True:
            value = "is_logged"
            customdata_log_condition = {"condition": {"conditionNodeId": 1,"values": ["log_request_details"],
                                                  "conditionNode": {"conditionNodeId": 15,"values": ["custom_data"],
                                                  "conditionNode": {"conditionNodeId": 16,"values": [value],
                                                  "conditionNode": {"conditionNodeId": 6,"values": ["value"],
                                                  "conditionNode": {"conditionNodeId": 23,"values": ["is"],
                                                  "conditionNode": {"conditionNodeId": 4,"values": [customData]}}}}}}}
        customdata_log_condition = json.dumps(customdata_log_condition,indent=4)
        print(customdata_log_condition
        )
        return customdata_log_condition

    def lastMileAcceleration(self,isgzipped):
        value = "is_not_gzipped"
        if isgzipped == True:
            value = "is_gzipped"
        lma_condition = {"condition": {"conditionNodeId": 1,"values": ["last_mile_acceleration"],
                                        "conditionNode": {"conditionNodeId": 22,"values": [value]}}}
        lma_condition = json.dumps(lma_condition,indent=4)
        return lma_condition

    def ignoreCaseinCacheKey(self,isenabled):
        value = "is_not_enabled"
        if isenabled == True:
            value = "is_enabled"
        ignore_condition = {"condition": {"conditionNodeId": 1,"values": ["ignore_case_in_cache_key"],
                                        "conditionNode": {"conditionNodeId": 14,"values": [value]}}}
        ignore_condition = json.dumps(ignore_condition,indent=4)
        return ignore_condition

    def prefetch(self,istriggered):
        value = "is_not_triggered"
        if istriggered == True:
            value = "is_triggered"
        prefetch_condition = {"condition": {"conditionNodeId": 1,"values": ["prefetch_objects"],
                                        "conditionNode": {"conditionNodeId": 20,"values": [value]}}}
        prefetch_condition = json.dumps(prefetch_condition,indent=4)
        return prefetch_condition

    def cpcode(self,cpcode):
        cpcode_condition = {"condition": {"conditionNodeId": 1,"values": ["cp_code"],
                                        "conditionNode": {"conditionNodeId": 23,"values": ["is"],
                                        "conditionNode": {"conditionNodeId": 9,"values": [cpcode] } } } }
        cpcode_condition = json.dumps(cpcode_condition)
        return cpcode_condition

    def cacheKeyQueryParams(self,isincluded,list=None):
        if isincluded == True:
            cachekeyQP_condition = {"condition": {"conditionNodeId": 1,"values": ["cache_key_query_parameters"],
                                                  "conditionNode": {"conditionNodeId": 19,"values": ["included"],
                                                  "conditionNode": {"conditionNodeId": 25,"values": list}}}}
        else:
            cachekeyQP_condition = {"condition": {"conditionNodeId": 1,"values": ["cache_key_query_parameters"],
                                                  "conditionNode": {"conditionNodeId": 19,"values": ["not_included"]}}}
        cachekeyQP_condition = json.dumps(cachekeyQP_condition,indent=4)
        return cachekeyQP_condition

    def cache(self,option,ttl=None):
        if option == 'no-store' or option == 'NO-CACHE':
            cache_condition = {"condition": {"conditionNodeId": 1,"values": ["caching_option"],
                                            "conditionNode": {"conditionNodeId": 23,"values": ["is"],
                                            "conditionNode": {"conditionNodeId": 10,"values": ["no-store"]}}}}
        elif option == 'bypass-cache' or option == 'BYPASS_CACHE':
            cache_condition = {"condition": {"conditionNodeId": 1,"values": ["caching_option"],
                                             "conditionNode": {"conditionNodeId": 23,"values": ["is"],
                                             "conditionNode": {"conditionNodeId": 10,"values": ["bypass-cache"]}}}}
        elif option == 'cache':
            unit = ttl[-1:]
            time = int(ttl[:-1])
            if unit == 's':
                duration = 'seconds'
            elif unit == 'h':
                duration = 'hours'
            elif unit == 'd':
                duration = 'days'
            elif unit == 'm':
                duration = 'minutes'
            cache_condition = {"condition": {"conditionNodeId": 1,"values": ["caching_option"],
                                             "conditionNode": {"conditionNodeId": 23,"values": ["is"],
                                             "conditionNode": {"conditionNodeId": 10,"values": ["cache"],
                                             "conditionNode": {"conditionNodeId": 11,"values": [duration],
                                             "conditionNode": {"conditionNodeId": 9,"values": [time]}}}}}}
        cache_condition = json.dumps(cache_condition,indent=4)
        return cache_condition

    def originServerCacheKeyHostName(self,cacheKey):
        originServerCK_condition = {"condition": {"conditionNodeId": 1,"values": ["origin_server_cache_key_hostname"],
                                        "conditionNode": {"conditionNodeId": 23,"values": ["is"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [cacheKey] } } } }
        originServerCK_condition = json.dumps(originServerCK_condition,indent=4)
        print(originServerCK_condition)
        return originServerCK_condition


    def responseHeaderExists(self,headerName):
        resheader_condition = {"condition": {"conditionNodeId": 1,"values": ["response_header"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [headerName],
                                        "conditionNode": {"conditionNodeId": 5,"values": ["exists"] } } } }
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderDoesNotExist(self,headerName):
        resheader_condition = {"condition": {"conditionNodeId": 1,"values": ["response_header"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [headerName],
                                        "conditionNode": {"conditionNodeId": 5,"values": ["does_not_exist"] } } } }
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderHasNoValue(self,headerName):
        resheader_condition = {"condition": {"conditionNodeId": 1,"values": ["response_header"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [headerName],
                                        "conditionNode": {"conditionNodeId": 5,"values": ["has_no_value"] } } } }
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def getHasValueCondition(self,isHeader,varname,operator,varvalue):
        resheader_condition = self._hasvaluecondition.copy()
        if isHeader == True:
            resheader_condition["condition"]["values"] = ["response_header"]
        else:
            resheader_condition["condition"]["values"] = ["variable"]
        resheader_condition["condition"]["conditionNode"]["values"] = [varname]
        resheader_condition["condition"]["conditionNode"]["conditionNode"]["conditionNode"]["values"] = [operator]
        resheader_condition["condition"]["conditionNode"]["conditionNode"]["conditionNode"]["conditionNode"]["values"] = [varvalue]
        return resheader_condition

    def responseHeaderBeginsWith(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"begins_with",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderDoesntNotBeginWith(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"does_not_begin_with",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderEndsWith(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"ends_with",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderDoesNotEndWith(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"does_not_end_with",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderEquals(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"equals",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderNotEquals(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"does_not_equal",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderContains(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"contains",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderDoesNotContain(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"does_not_contain",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderMatchesRegex(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"matches_regex",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def responseHeaderDoesntMatchRegex(self,headerName,headerValue):
        resheader_condition = self.getHasValueCondition(True,headerName,"does_not_match_regex",headerValue)
        resheader_condition = json.dumps(resheader_condition,indent=4)
        return resheader_condition

    def variableExists(self,variableName):
        variable_condition = {"condition": {"conditionNodeId": 1,"values": ["variable"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [variableName],
                                        "conditionNode": {"conditionNodeId": 5,"values": ["exists"] } } } }
        variable_condition = json.dumps(variable_condition,indent=4)
        return variable_condition

    def variableDoesNotExist(self,variableName):
        variable_condition = {"condition": {"conditionNodeId": 1,"values": ["variable"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [variableName],
                                        "conditionNode": {"conditionNodeId": 5,"values": ["does_not_exist"] } } } }
        variable_condition = json.dumps(variable_condition,indent=4)
        return variable_condition

    def variableHasNoValue(self,variableName):
        variable_condition = {"condition": {"conditionNodeId": 1,"values": ["variable"],
                                        "conditionNode": {"conditionNodeId": 4,"values": [variableName],
                                        "conditionNode": {"conditionNodeId": 5,"values": ["has_no_value"] } } } }
        variable_condition = json.dumps(variable_condition,indent=4)
        return variable_condition

    def variableBeginsWith(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"begins_with",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableDoesntNotBeginWith(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"does_not_begin_with",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableEndsWith(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"ends_with",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableDoesNotEndWith(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"does_not_end_with",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableEquals(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"equals",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableNotEquals(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"does_not_equal",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableContains(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"contains",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableDoesNotContain(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"does_not_contain",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableMatchesRegex(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"matches_regex",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition

    def variableDoesntMatchRegex(self,variableName,variableValue):
        variablehas_condition = self.getHasValueCondition(False,variableName,"does_not_match_regex",variableValue)
        variablehas_condition = json.dumps(variablehas_condition,indent=4)
        return variablehas_condition
