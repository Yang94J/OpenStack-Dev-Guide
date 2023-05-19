# -------------------    Util Functions    ---------------------------------
# Get json data more clear
# @Input jsonIntegrate : json file needed to be parsed
# @tabnum : num of tabs
def util_jsonSplitShow(jsonIntegrate, tabnum):
    generatedStr = ""
    for key in jsonIntegrate:
        val = jsonIntegrate[key]

        # if the json is nested
        if type(val) == dict:
            generatedStr += "\t"*tabnum+key+" : "+'{\n'
            generatedStr += util_jsonSplitShow(val, tabnum+2)
            generatedStr += "\t"*tabnum+""+"}\n"
        else:
            generatedStr += "\t"*tabnum+key+" : "+val+'\n'
    return generatedStr

# -------------------    Util Functions    ---------------------------------
# Print Response Info
# Including Response Status Code, Encodings, Headers(json), Content, Text, History
# @input response, acquired via api request
def util_printResponseInfo(response):
    print('\t Response Status Code : ' + str(response.status_code))
    print('\t Response : ' + str(response))
    print('\t Response Type : ' + str(type(response)))
    print('\t Url :' + response.url)
    print('\t Encoding : '+str(response.encoding))
    print('\t Headers : \n' + util_jsonSplitShow(response.headers, 2))
    print('\t Content : ' + str(response.content))
    print('\t TEXT : '+str(response.text))
    print("\t HISTORY : "+str(response.history))