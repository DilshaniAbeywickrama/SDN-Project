from requests.auth import HTTPBasicAuth
import json
import requests

def p_a_flow(p, d):
    
    f = open(str(p) + '/json/add_flow_template.json')
    j_data = json.load(f)
    f.close()
    
    add_fl = f"http://10.15.3.9:8181/restconf/operations/sal-flow:add-flow"
    head = {'Content-Type': 'application/json'}

    j_data['input'][
        "node"] = f"/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:id='{d[0]}']"

    if d[1] != "":
        j_data['input']["match"]["ethernet-match"]["ethernet-source"] = {"address": d[1]}

    if d[2] != "":
        j_data['input']["match"]["ethernet-match"]["ethernet-destination"] = {"address": d[2]}

    j_data['input']["priority"] = d[3]

    if d[4] == "allow":
        j_data['input']["instructions"]["instruction"][0]["apply-actions"]["action"] = [
            {"order": 0, "output-action": {"output-node-connector": "ALL", "max-length": 60}}]

    s_data = json.dumps(j_data)
    res = requests.post(add_fl, auth=HTTPBasicAuth('admin', 'admin'), data=s_data, headers=head)

    return res.status_code

def p_d_flow(p, d):

    f = open(str(p) + '/json/delete_flow_template.json')

    j_data = json.load(f)

    f.close()

    delete_fl = f"http://10.15.3.9:8181/restconf/operations/sal-flow:remove-flow"
    headers = {'Content-Type': 'application/json'}

    j_data['input'][
        "node"] = f"/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:id='{d[0]}']"

    if d[1] != "":
        j_data['input']["match"]["ethernet-match"]["ethernet-source"] = {"address": d[1]}

    if d[2] != "":
        j_data['input']["match"]["ethernet-match"]["ethernet-destination"] = {"address": d[2]}

    j_data['input']["priority"] = d[3]

    s_data = json.dumps(j_data)
    res = requests.post(delete_fl, auth=HTTPBasicAuth('admin', 'admin'), data=s_data, headers=headers)

    return res.status_code
