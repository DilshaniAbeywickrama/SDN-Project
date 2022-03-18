from distutils.log import error
from flask import Flask, render_template, request, redirect, url_for
import os
#import json
#import requests
from requests.auth import HTTPBasicAuth

from main.get_data import get_flow_data,  get_topology 
#from main.load_file import add_flow_template, delete_flow_template
from main.post_data import p_a_flow, p_d_flow


app = Flask(__name__)

@app.route('/')
def index():
    d = ["Opendaylight", "mininet", "python", "SDN"]
    return render_template('index.html', details=d)


@app.route('/flow_table', methods=['GET', 'POST'])
def flow_table():
    no_of_nodes, flow_table_data = get_flow_data()[0:2] 
    return render_template('flow_table.html', num_switches=no_of_nodes, flow_table=flow_table_data)

@app.route('/add_flow')
def add_flow():
    switch_names = get_flow_data()[2] 
    return render_template('add_flow.html', switch_data=switch_names)


@app.route('/delete_flow')
def delete_flow():
    switch_names = get_flow_data()[2]
    return render_template('delete_flow.html', switch_data=switch_names)


@app.route('/add_flow_show', methods=['POST'])
def add_flow_show():
    switch_names = get_flow_data()[2]
    flow_config_data = request.form
    mac_address_sr, mac_address_ds = flow_config_data["mac_address_sr"], flow_config_data["mac_address_ds"]
    switch, priority, action = flow_config_data["switch"], flow_config_data["priority"], flow_config_data["action"]

    if not priority or action == "0" or (
             not mac_address_ds) or switch == "0":
        error_statement = 'Switch, priority and action are compulsory fields. One of IP addresses and MAC addresses ' \
                          'should be filled.'
        return render_template('add_flow.html',
                               error_statement=error_statement,
                               switch=switch,
                               mac_address_sr=mac_address_sr,
                               mac_address_ds=mac_address_ds,
                               priority=priority,
                               action=action,
                               switch_data=switch_names)

    d = [switch,  mac_address_sr, mac_address_ds, priority, action]

    p=os.getcwd()
    res = p_a_flow(p, d)

    if res == 200:
        return render_template('add_flow_show.html', details=d)
    else:
        error_statement = res
        return render_template('add_flow.html',
                               error_statement=error_statement,
                               switch=switch,
                               mac_address_sr=mac_address_sr,
                               mac_address_ds=mac_address_ds,
                               priority=priority,
                               action=action,
                               switch_data=switch_names)



@app.route('/delete_flow_show', methods=['POST'])
def delete_flow_show():
    switch_names = get_flow_data()[2]
    flow_config_data = request.form
    mac_address_sr, mac_address_ds = flow_config_data["mac_address_sr"], flow_config_data["mac_address_ds"]
    switch, priority = flow_config_data["switch"], flow_config_data["priority"]

    if not priority or (
             not mac_address_ds) or switch == "0":
        error_statement = 'Switch, priority are compulsory fields. One of IP addresses and MAC addresses ' \
                          'should be filled.'
        return render_template('delete_flow_show.html',
                               error_statement=error_statement,
                               switch=switch,
                               mac_address_sr=mac_address_sr,
                               mac_address_ds=mac_address_ds,
                               priority=priority,
                               switch_data=switch_names)

    d = [switch,  mac_address_sr, mac_address_ds, priority] 

    p=os.getcwd()
    res = p_d_flow(p, d)

    if res == 200:
        return render_template('delete_flow_show.html', details=d)
    else:
        error_statement = res
        return render_template('delete_flow.html',
                               error_statement=error_statement,
                               switch=switch,
                               mac_address_sr=mac_address_sr,
                               mac_address_ds=mac_address_ds,
                               priority=priority,
                               switch_data=switch_names)

@app.route('/topology')
def topology():
    host_dataset, switch_dataset, sorted_keys = get_topology()
    return render_template('topology.html', nodes=host_dataset, switch=switch_dataset, keys=sorted_keys)

@app.route('/login', methods=['GET'])
def login():
    print ("login")
    return render_template('login.html', error = False)

@app.route('/login_check', methods=['POST'])
def login_check():
    print ("kaushan")
    username = request.form['username']
    password = request.form['password']
    if username == 'Mora' and password == '123':
        d = ["Opendaylight", "mininet", "python", "SDN"]

        return redirect (url_for('index'))

    print(username)
    print(password)
    return render_template('login.html', error = True)


if __name__ == '__main__':
    app.run(debug=True)



