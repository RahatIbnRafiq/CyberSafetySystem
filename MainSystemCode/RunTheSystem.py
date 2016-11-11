

import VineAPI.VineAPI as vineapi #importing the vine api class to collect the list of apis

vine_api_class = vineapi.VineAPIClass()
vine_api_list = vine_api_class.getVineAPIList()

for vine_api in vine_api_list:
    print vine_api
