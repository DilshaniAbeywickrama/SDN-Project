import requests
from requests.auth import HTTPBasicAuth

def get_flow_data():
    
    url = f"http://10.15.3.9:8181/restconf/operational/opendaylight-inventory:nodes"

    response = requests.get(url, auth=HTTPBasicAuth("admin", "admin")).json()


    if response:
        no_of_nodes=len(response["nodes"]["node"])
        #switch_ids=[]
        flow_table=[]
        switch_names=[]
        for i in range(no_of_nodes):
            switch_id=response["nodes"]["node"][i]["id"]
            switch_names.append(switch_id)

            for j in (response["nodes"]["node"][i]["flow-node-inventory:table"]):
                if j["opendaylight-flow-table-statistics:flow-table-statistics"]["active-flows"]!=0:
                    count=0
                    for flow in j["flow"]:
                        count         =count+1
                        priority      =flow["priority"]
                        #cookie  = hex(int(flow["cookie"]))
                        packet_count  =flow["opendaylight-flow-statistics:flow-statistics"]["packet-count"]
                        byte_count    =flow["opendaylight-flow-statistics:flow-statistics"]["byte-count"]
                        src_mac_addr=""
                        dest_mac_addr=""
                        
                        if "ethernet-match" in flow["match"]:
                            if "ethernet-source" in flow["match"]["ethernet-match"]:
                                src_mac_addr = flow["match"]["ethernet-match"]["ethernet-source"]["address"]
                                print (src_mac_addr)
                            else:
                                src_mac_addr=None
                            if "ethernet-destination" in flow["match"]["ethernet-match"]:
                                dest_mac_addr = flow["match"]["ethernet-match"]["ethernet-destination"]["address"]
                                
                            else:
                                dest_mac_addr=None
                            
                        else:
                            src_mac_addr=None
                            dest_mac_addr=None
                        
            
                        actions=[]
                        try:
                        
                            for l in flow["instructions"]["instruction"][0]["apply-actions"]["action"]:
                        
                                if (l["output-action"]["output-node-connector"]).isnumeric():
                                    actions.append("s"+switch_id.split(":")[-1]+"_eth"+l["output-action"]["output-node-connector"])
                                    
                                else:
                                    actions.append(l["output-action"]["output-node-connector"])
                        except:
                            actions.append("drop")

                        action = "Send the packets to "
                        if len(actions)==1:
                            if actions[0]=='drop':
                                action= "Drop the packets"
                            else:
                                action=action+ actions[0] 
                        else:
                            action=action+actions[0]+' , '+actions[1]
                    

                        
                        flow_table.append([switch_id,priority,packet_count,byte_count,src_mac_addr,dest_mac_addr,action])
                
        switch_names.sort()

    return no_of_nodes,flow_table, switch_names
    



def get_topology():
    odl_url = f'http://10.15.3.9:8181/restconf/operational/network-topology:network-topology'
    response = requests.get(odl_url, auth=HTTPBasicAuth("admin", "admin"))
    data_set1 = response.json()

    if data_set1:
        nodesCount = len(data_set1["network-topology"]["topology"][0]["node"])
        hostDataset = []
        switchDic = {}
        switchDataset = {}

    for node in range(0,nodesCount):
        if "host" in data_set1["network-topology"]["topology"][0]["node"][node]["node-id"]:
            temp1 = data_set1["network-topology"]["topology"][0]["node"][node]['host-tracker-service:addresses'][0]['ip'].strip().split('.')
            host = "h"+ str(int(temp1[-1]))
            ip = data_set1["network-topology"]["topology"][0]["node"][node]['host-tracker-service:addresses'][0]['ip']
            mac = data_set1["network-topology"]["topology"][0]["node"][node]['host-tracker-service:addresses'][0]['mac']
            temp2 = data_set1["network-topology"]["topology"][0]["node"][node]['host-tracker-service:attachment-points'][0]['tp-id'].strip().split(':')
            port = "s"+temp2[1] +"-eth"+temp2[2]
            status = data_set1["network-topology"]["topology"][0]["node"][node]['host-tracker-service:attachment-points'][0]['active']
            if status == True:
                status = "Active"
            else:
                status = "Not-active"
            hostDataset.append([host,ip,mac,port,status])

        elif "openflow" in data_set1["network-topology"]["topology"][0]["node"][node]["node-id"]:
            temp3 = data_set1["network-topology"]["topology"][0]["node"][node]["node-id"].strip().split(':')
            key1 = "s"+temp3[-1]
            switchDataset[key1]=[]
            portCount = len(data_set1["network-topology"]["topology"][0]["node"][node]["termination-point"])
            for i in range(portCount):
                if "LOCAL" in data_set1["network-topology"]["topology"][0]["node"][node]["termination-point"][i]["tp-id"]:
                    continue
                switchDic[data_set1["network-topology"]["topology"][0]["node"][node]["termination-point"][i]["tp-id"]]="portID"

        linkCount = len(data_set1["network-topology"]["topology"][0]["link"])

        for j in range(linkCount):
            if data_set1["network-topology"]["topology"][0]["link"][j]["source"]["source-tp"] in switchDic:
                switchDic[data_set1["network-topology"]["topology"][0]["link"][j]["source"]["source-tp"]]=data_set1["network-topology"]["topology"][0]["link"][j]["destination"]["dest-node"]

    for element in switchDic:
        x=element.strip().split(':')
        if "openflow" in switchDic[element]:
            temp4 = switchDic[element].strip().split(':')
            y= "s"+temp4[-1]
        else:
            temp4 = switchDic[element]
            for i in range(len(hostDataset)):
                if temp4.strip()[5::] in hostDataset[i]: 
                    y= hostDataset[i][0]

        switchDataset["s"+x[1]].append(("s"+x[1]+"-eth"+x[2],y))

    sorted_keys = sorted(switchDataset)

    return hostDataset, switchDataset, sorted_keys
