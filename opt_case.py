#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""
import sys
import os

import mininet.net
import mininet.node
import mininet.cli
import mininet.log
import mininet.ns3

from mininet.net import Mininet, MininetWithControlNet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info                     
from mininet.ns3 import *        

import ns.core
import ns.network
import ns.wifi
import ns.lte
import ns.csma
import ns.wimax
import ns.uan
import ns.netanim
import ns.mobility

from ns3lte import LTESegment

import time
import numpy as np
import re

from threading import Thread
urv = ns.core.UniformRandomVariable()
urv.SetAttribute("Min", ns.core.DoubleValue(5))
urv.SetAttribute("Max", ns.core.DoubleValue(20))

mininet.ns3.clear()

pos_init = [500, 500, 5]

n_cv = 10

nodes_w1=[{'name': 'w1h1', 'type': 'host', 'ip': '10.10.11.1', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h2', 'type': 'host', 'ip': '10.10.11.2', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h3', 'type': 'host', 'ip': '10.10.11.3', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h4', 'type': 'host', 'ip': '10.10.11.4', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h5', 'type': 'host', 'ip': '10.10.11.5', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h6', 'type': 'host', 'ip': '10.10.11.6', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h7', 'type': 'host', 'ip': '10.10.11.7', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h8', 'type': 'host', 'ip': '10.10.11.8', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h9', 'type': 'host', 'ip': '10.10.11.9', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1h10', 'type': 'host', 'ip': '10.10.11.10', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w1', 'type': 'switch', 'position': (100.0, 100.0, 50.0) },
         ]

nodes_w2=[{'name': 'w2h1', 'type': 'host', 'ip': '10.10.12.1', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h2', 'type': 'host', 'ip': '10.10.12.2', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h3', 'type': 'host', 'ip': '10.10.12.3', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h4', 'type': 'host', 'ip': '10.10.12.4', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h5', 'type': 'host', 'ip': '10.10.12.5', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h6', 'type': 'host', 'ip': '10.10.12.6', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h7', 'type': 'host', 'ip': '10.10.12.7', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h8', 'type': 'host', 'ip': '10.10.12.8', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h9', 'type': 'host', 'ip': '10.10.12.9', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2h10', 'type': 'host', 'ip': '10.10.12.10', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w2', 'type': 'switch', 'position': (100.0, 900.0, 50.0) },
         ]

nodes_w3=[{'name': 'w3h1', 'type': 'host', 'ip': '10.10.13.1', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h2', 'type': 'host', 'ip': '10.10.13.2', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h3', 'type': 'host', 'ip': '10.10.13.3', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h4', 'type': 'host', 'ip': '10.10.13.4', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h5', 'type': 'host', 'ip': '10.10.13.5', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h6', 'type': 'host', 'ip': '10.10.13.6', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h7', 'type': 'host', 'ip': '10.10.13.7', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h8', 'type': 'host', 'ip': '10.10.13.8', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h9', 'type': 'host', 'ip': '10.10.13.9', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3h10', 'type': 'host', 'ip': '10.10.13.10', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w3', 'type': 'switch', 'position': (900.0, 100.0, 50.0) },
         ]

nodes_w4=[{'name': 'w4h1', 'type': 'host', 'ip': '10.10.14.1', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h2', 'type': 'host', 'ip': '10.10.14.2', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h3', 'type': 'host', 'ip': '10.10.14.3', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h4', 'type': 'host', 'ip': '10.10.14.4', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h5', 'type': 'host', 'ip': '10.10.14.5', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h6', 'type': 'host', 'ip': '10.10.14.6', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h7', 'type': 'host', 'ip': '10.10.14.7', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h8', 'type': 'host', 'ip': '10.10.14.8', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h9', 'type': 'host', 'ip': '10.10.14.9', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4h10', 'type': 'host', 'ip': '10.10.14.10', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w4', 'type': 'switch', 'position': (900.0, 900.0, 50.0) },
         ]

nodes_w5=[{'name': 'w5h1', 'type': 'host', 'ip': '10.10.15.1', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h2', 'type': 'host', 'ip': '10.10.15.2', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h3', 'type': 'host', 'ip': '10.10.15.3', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h4', 'type': 'host', 'ip': '10.10.15.4', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h5', 'type': 'host', 'ip': '10.10.15.5', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h6', 'type': 'host', 'ip': '10.10.15.6', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h7', 'type': 'host', 'ip': '10.10.15.7', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h8', 'type': 'host', 'ip': '10.10.15.8', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h9', 'type': 'host', 'ip': '10.10.15.9', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5h10', 'type': 'host', 'ip': '10.10.15.10', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'w5', 'type': 'switch', 'position': (500.0, 500.0, 50.0) },
         ]

nodes_l1=[{'name': 'l1h1', 'type': 'host', 'ip': '10.10.21.1', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h2', 'type': 'host', 'ip': '10.10.21.2', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h3', 'type': 'host', 'ip': '10.10.21.3', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h4', 'type': 'host', 'ip': '10.10.21.4', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h5', 'type': 'host', 'ip': '10.10.21.5', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h6', 'type': 'host', 'ip': '10.10.21.6', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h7', 'type': 'host', 'ip': '10.10.21.7', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h8', 'type': 'host', 'ip': '10.10.21.8', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h9', 'type': 'host', 'ip': '10.10.21.9', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1h10', 'type': 'host', 'ip': '10.10.21.10', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l1', 'type': 'switch', 'position': (300.0, 500.0, 50.0) },
         ]

nodes_l2=[{'name': 'l2h1', 'type': 'host', 'ip': '10.10.22.1', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h2', 'type': 'host', 'ip': '10.10.22.2', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h3', 'type': 'host', 'ip': '10.10.22.3', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h4', 'type': 'host', 'ip': '10.10.22.4', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h5', 'type': 'host', 'ip': '10.10.22.5', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h6', 'type': 'host', 'ip': '10.10.22.6', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h7', 'type': 'host', 'ip': '10.10.22.7', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h8', 'type': 'host', 'ip': '10.10.22.8', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h9', 'type': 'host', 'ip': '10.10.22.9', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2h10', 'type': 'host', 'ip': '10.10.22.10', 'position': (pos_init[0], pos_init[1], pos_init[2])},
          {'name': 'l2', 'type': 'switch', 'position': (700.0, 500.0, 50.0) },
         ]

nodes_w99=[{'name': 'w99h1', 'type': 'host', 'ip': '10.10.20.100', 'position': (1995.0, 1995.0, 5.0)},
          {'name': 'w99', 'type': 'switch', 'position': (2000.0, 2000.0, 50.0) },
         ]

w1intfs=[{'nodename': 'w1h1', 'type': 'sta', 'channel': 1, 'ssid': 'w1s1'},
         {'nodename': 'w1h2', 'type': 'sta', 'channel': 1, 'ssid': 'w1s2'},
         {'nodename': 'w1h3', 'type': 'sta', 'channel': 1, 'ssid': 'w1s3'},
         {'nodename': 'w1h4', 'type': 'sta', 'channel': 1, 'ssid': 'w1s4'},
         {'nodename': 'w1h5', 'type': 'sta', 'channel': 1, 'ssid': 'w1s5'},
         {'nodename': 'w1h6', 'type': 'sta', 'channel': 1, 'ssid': 'w1s6'},
         {'nodename': 'w1h7', 'type': 'sta', 'channel': 1, 'ssid': 'w1s7'},
         {'nodename': 'w1h8', 'type': 'sta', 'channel': 1, 'ssid': 'w1s8'},
         {'nodename': 'w1h9', 'type': 'sta', 'channel': 1, 'ssid': 'w1s9'},
         {'nodename': 'w1h10', 'type': 'sta', 'channel': 1, 'ssid': 'w1s10'},
         {'nodename': 'w1', 'type': 'ap', 'channel': 1, 'ssid': 'ap1'},
        ]

w2intfs=[{'nodename': 'w2h1', 'type': 'sta', 'channel': 1, 'ssid': 'w2s1'},
         {'nodename': 'w2h2', 'type': 'sta', 'channel': 1, 'ssid': 'w2s2'},
         {'nodename': 'w2h3', 'type': 'sta', 'channel': 1, 'ssid': 'w2s3'},
         {'nodename': 'w2h4', 'type': 'sta', 'channel': 1, 'ssid': 'w2s4'},
         {'nodename': 'w2h5', 'type': 'sta', 'channel': 1, 'ssid': 'w2s5'},
         {'nodename': 'w2h6', 'type': 'sta', 'channel': 1, 'ssid': 'w2s6'},
         {'nodename': 'w2h7', 'type': 'sta', 'channel': 1, 'ssid': 'w2s7'},
         {'nodename': 'w2h8', 'type': 'sta', 'channel': 1, 'ssid': 'w2s8'},
         {'nodename': 'w2h9', 'type': 'sta', 'channel': 1, 'ssid': 'w2s9'},
         {'nodename': 'w2h10', 'type': 'sta', 'channel': 1, 'ssid': 'w2s10'},
         {'nodename': 'w2', 'type': 'ap', 'channel': 1, 'ssid': 'ap2'},
        ]

w3intfs=[{'nodename': 'w3h1', 'type': 'sta', 'channel': 1, 'ssid': 'w3s1'},
         {'nodename': 'w3h2', 'type': 'sta', 'channel': 1, 'ssid': 'w3s2'},
         {'nodename': 'w3h3', 'type': 'sta', 'channel': 1, 'ssid': 'w3s3'},
         {'nodename': 'w3h4', 'type': 'sta', 'channel': 1, 'ssid': 'w3s4'},
         {'nodename': 'w3h5', 'type': 'sta', 'channel': 1, 'ssid': 'w3s5'},
         {'nodename': 'w3h6', 'type': 'sta', 'channel': 1, 'ssid': 'w3s6'},
         {'nodename': 'w3h7', 'type': 'sta', 'channel': 1, 'ssid': 'w3s7'},
         {'nodename': 'w3h8', 'type': 'sta', 'channel': 1, 'ssid': 'w3s8'},
         {'nodename': 'w3h9', 'type': 'sta', 'channel': 1, 'ssid': 'w3s9'},
         {'nodename': 'w3h10', 'type': 'sta', 'channel': 1, 'ssid': 'w3s10'},
         {'nodename': 'w3', 'type': 'ap', 'channel': 1, 'ssid': 'ap3'},
        ]

w4intfs=[{'nodename': 'w4h1', 'type': 'sta', 'channel': 1, 'ssid': 'w4s1'},
         {'nodename': 'w4h2', 'type': 'sta', 'channel': 1, 'ssid': 'w4s2'},
         {'nodename': 'w4h3', 'type': 'sta', 'channel': 1, 'ssid': 'w4s3'},
         {'nodename': 'w4h4', 'type': 'sta', 'channel': 1, 'ssid': 'w4s4'},
         {'nodename': 'w4h5', 'type': 'sta', 'channel': 1, 'ssid': 'w4s5'},
         {'nodename': 'w4h6', 'type': 'sta', 'channel': 1, 'ssid': 'w4s6'},
         {'nodename': 'w4h7', 'type': 'sta', 'channel': 1, 'ssid': 'w4s7'},
         {'nodename': 'w4h8', 'type': 'sta', 'channel': 1, 'ssid': 'w4s8'},
         {'nodename': 'w4h9', 'type': 'sta', 'channel': 1, 'ssid': 'w4s9'},
         {'nodename': 'w4h10', 'type': 'sta', 'channel': 1, 'ssid': 'w4s10'},
         {'nodename': 'w4', 'type': 'ap', 'channel': 1, 'ssid': 'ap4'},
        ]

w5intfs=[{'nodename': 'w5h1', 'type': 'sta', 'channel': 1, 'ssid': 'w5s1'},
         {'nodename': 'w5h2', 'type': 'sta', 'channel': 1, 'ssid': 'w5s2'},
         {'nodename': 'w5h3', 'type': 'sta', 'channel': 1, 'ssid': 'w5s3'},
         {'nodename': 'w5h4', 'type': 'sta', 'channel': 1, 'ssid': 'w5s4'},
         {'nodename': 'w5h5', 'type': 'sta', 'channel': 1, 'ssid': 'w5s5'},
         {'nodename': 'w5h6', 'type': 'sta', 'channel': 1, 'ssid': 'w5s6'},
         {'nodename': 'w5h7', 'type': 'sta', 'channel': 1, 'ssid': 'w5s7'},
         {'nodename': 'w5h8', 'type': 'sta', 'channel': 1, 'ssid': 'w5s8'},
         {'nodename': 'w5h9', 'type': 'sta', 'channel': 1, 'ssid': 'w5s9'},
         {'nodename': 'w5h10', 'type': 'sta', 'channel': 1, 'ssid': 'w5s10'},
         {'nodename': 'w5', 'type': 'ap', 'channel': 1, 'ssid': 'ap5'},
        ]

l1intfs=[{'nodename': 'l1h1', 'type': 'sta', 'channel': 1, 'ssid': 'l1s1'},
         {'nodename': 'l1h2', 'type': 'sta', 'channel': 1, 'ssid': 'l1s2'},
         {'nodename': 'l1h3', 'type': 'sta', 'channel': 1, 'ssid': 'l1s3'},
         {'nodename': 'l1h4', 'type': 'sta', 'channel': 1, 'ssid': 'l1s4'},
         {'nodename': 'l1h5', 'type': 'sta', 'channel': 1, 'ssid': 'l1s5'},
         {'nodename': 'l1h6', 'type': 'sta', 'channel': 1, 'ssid': 'l1s6'},
         {'nodename': 'l1h7', 'type': 'sta', 'channel': 1, 'ssid': 'l1s7'},
         {'nodename': 'l1h8', 'type': 'sta', 'channel': 1, 'ssid': 'l1s8'},
         {'nodename': 'l1h9', 'type': 'sta', 'channel': 1, 'ssid': 'l1s9'},
         {'nodename': 'l1h10', 'type': 'sta', 'channel': 1, 'ssid': 'l1s10'},
         {'nodename': 'l1', 'type': 'ap', 'channel': 1, 'ssid': 'bs1'},
        ]

l2intfs=[{'nodename': 'l2h1', 'type': 'sta', 'channel': 1, 'ssid': 'l2s1'},
         {'nodename': 'l2h2', 'type': 'sta', 'channel': 1, 'ssid': 'l2s2'},
         {'nodename': 'l2h3', 'type': 'sta', 'channel': 1, 'ssid': 'l2s3'},
         {'nodename': 'l2h4', 'type': 'sta', 'channel': 1, 'ssid': 'l2s4'},
         {'nodename': 'l2h5', 'type': 'sta', 'channel': 1, 'ssid': 'l2s5'},
         {'nodename': 'l2h6', 'type': 'sta', 'channel': 1, 'ssid': 'l2s6'},
         {'nodename': 'l2h7', 'type': 'sta', 'channel': 1, 'ssid': 'l2s7'},
         {'nodename': 'l2h8', 'type': 'sta', 'channel': 1, 'ssid': 'l2s8'},
         {'nodename': 'l2h9', 'type': 'sta', 'channel': 1, 'ssid': 'l2s9'},
         {'nodename': 'l2h10', 'type': 'sta', 'channel': 1, 'ssid': 'l2s10'},
         {'nodename': 'l2', 'type': 'ap', 'channel': 1, 'ssid': 'bs2'},
        ]

w99intfs=[{'nodename': 'w99h1', 'type': 'sta', 'channel': 1, 'ssid': 'w99s1'},
         {'nodename': 'w99', 'type': 'ap', 'channel': 1, 'ssid': 'ap99'},
        ]

csmalinks = [{'nodename1': 'l1', 'nodename2': 'w99'},
             {'nodename1': 'l2', 'nodename2': 'w99'},
             {'nodename1': 'w1', 'nodename2': 'w99'},
             {'nodename1': 'w2', 'nodename2': 'w99'},
             {'nodename1': 'w3', 'nodename2': 'w99'}, 
             {'nodename1': 'w4', 'nodename2': 'w99'},
             {'nodename1': 'w5', 'nodename2': 'w99'},
            ]

def getNode( node, name ):
    for n in node:    
        if n.name == name:
            return n
    return None           

def WifiLTENet():

    "Create a Wifi+LTE network and add nodes to it."

    net = Mininet()

    info( '*** Adding controller\n' )
    net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )

    wifi1 = WifiSegment(standard = ns.wifi.WIFI_PHY_STANDARD_80211g)
    wifi2 = WifiSegment(standard = ns.wifi.WIFI_PHY_STANDARD_80211g)
    wifi3 = WifiSegment(standard = ns.wifi.WIFI_PHY_STANDARD_80211g)
    wifi4 = WifiSegment(standard = ns.wifi.WIFI_PHY_STANDARD_80211g)
    wifi5 = WifiSegment(standard = ns.wifi.WIFI_PHY_STANDARD_80211g)
    wifi99 = WifiSegment(standard = ns.wifi.WIFI_PHY_STANDARD_80211g)
    lte1 = LTESegment()
    lte2 = LTESegment()
    wifi1nodes = []
    wifi2nodes = []
    wifi3nodes = []
    wifi4nodes = []
    wifi5nodes = []
    wifi99nodes = []
    lte1nodes = []
    lte2nodes = []
    
    for n in nodes_w1:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        wifi1nodes.append (node)

    for n in nodes_w2:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        wifi2nodes.append (node)

    for n in nodes_w3:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        wifi3nodes.append (node)

    for n in nodes_w4:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        wifi4nodes.append (node)

    for n in nodes_w5:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        wifi5nodes.append (node)

    for n in nodes_w99:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        wifi99nodes.append (node)

    for n in nodes_l1:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        lte1nodes.append (node)

    for n in nodes_l2:
        nodename = n.get('name', None)
        nodetype = n.get('type', None)
        nodemob = n.get('mobility', None)
        nodepos = n.get('position', None)
        nodeip = n.get('ip', None)
        if nodetype is 'host':
            addfunc = net.addHost
            color = (255, 0, 0)
        elif nodetype is 'switch':
            addfunc = net.addSwitch
            color = (0, 0, 255)
        else:
            addfunc = None
        if nodename is None or addfunc is None: 
            continue
        node = addfunc (nodename, ip=nodeip)
        mininet.ns3.setMobilityModel (node, nodemob)
        if nodepos is not None:
            mininet.ns3.setPosition (node, nodepos[0], nodepos[1], nodepos[2])
        lte2nodes.append (node)

    print 'node creation done'

    for a in w1intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = wifi1.addSta
        elif atype is 'ap':
            addfunc = wifi1.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (wifi1nodes, anodename)
        tb = addfunc (node, achannel, assid)

    for a in w2intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = wifi2.addSta
        elif atype is 'ap':
            addfunc = wifi2.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (wifi2nodes, anodename)
        tb = addfunc (node, achannel, assid)

    for a in w3intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = wifi3.addSta
        elif atype is 'ap':
            addfunc = wifi3.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (wifi3nodes, anodename)
        tb = addfunc (node, achannel, assid)

    for a in w4intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = wifi4.addSta
        elif atype is 'ap':
            addfunc = wifi4.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (wifi4nodes, anodename)
        tb = addfunc (node, achannel, assid)

    for a in w5intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = wifi5.addSta
        elif atype is 'ap':
            addfunc = wifi5.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (wifi5nodes, anodename)
        tb = addfunc (node, achannel, assid)

    for a in w99intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = wifi99.addSta
        elif atype is 'ap':
            addfunc = wifi99.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (wifi99nodes, anodename)
        tb = addfunc (node, achannel, assid)

    for a in l1intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = lte1.addSta
        elif atype is 'ap':
            addfunc = lte1.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (lte1nodes, anodename)
        tb = addfunc (node, achannel, assid)

    for a in l2intfs:
        anodename = a.get('nodename', None)
        atype = a.get('type', None)
        achannel = a.get('channel', None)
        assid = a.get('ssid', None)
        aip = a.get('ip', None)
        if atype is 'sta':
            addfunc = lte2.addSta
        elif atype is 'ap':
            addfunc = lte2.addAp
        else:
            addfunc = None
        if anodename is None or addfunc is None or achannel is None:
            continue
        node = getNode (lte2nodes, anodename)
        tb = addfunc (node, achannel, assid)

    apnodes = [wifi1nodes[-1],wifi2nodes[-1],wifi3nodes[-1],wifi4nodes[-1],wifi5nodes[-1],lte1nodes[-1],lte2nodes[-1]]

    for cl in csmalinks:
        clnodename1 = cl.get('nodename1', None)  
        clnodename2 = cl.get('nodename2', None)
        if clnodename1 is None or clnodename2 is None:
            continue
        clnode1 = getNode (apnodes, clnodename1)
        clnode2 = getNode (wifi99nodes, clnodename2)
        if clnode1 is None or clnode2 is None:
            continue
        CSMALink( clnode1, clnode2, DataRate="54Mbps")

    print 'interface creation done'

    #anim = ns.netanim.AnimationInterface("opt_case_out.xml")
    #anim.EnablePacketMetadata (True)

    info( '*** Starting network\n' )
    net.start()
    print 'mininet started'
    mininet.ns3.start()
    print 'ns3 started'     

    info( '***Starting Simulation\n' )
    print 'starting simulation'

    time.sleep(10)

    #prev_out_ap = np.loadtxt('out_ap.csv')
    #print prev_out_ap

    fp = open('allpos.txt','r')
    lines = fp.readlines()
    fp.close()
    count = 0

    while(count<len(lines)):
        for i in range(n_cv):
            f = lines[count]
            pos = filter(None,re.split(' +', f.strip("\n").strip("[]"))) 
            pos = [float(j) for j in pos]
            pos = np.array(pos)
            count = count+1        
            mininet.ns3.setPosition(wifi2nodes[i],pos[0],pos[1],pos[2])
            mininet.ns3.setPosition(wifi3nodes[i],pos[0],pos[1],pos[2])
            mininet.ns3.setPosition(wifi4nodes[i],pos[0],pos[1],pos[2])
            mininet.ns3.setPosition(wifi5nodes[i],pos[0],pos[1],pos[2])
            mininet.ns3.setPosition(lte1nodes[i],pos[0],pos[1],pos[2])
            mininet.ns3.setPosition(lte2nodes[i],pos[0],pos[1],pos[2])        
            if(i==0): 
                with open('pos.txt','w') as f:
                    f.write(str(pos)+'\n')
            else:
                with open('pos.txt','a') as f:
                    f.write(str(pos)+'\n')

        time.sleep(0.1)

        out_ap = np.loadtxt('out_ap.csv')
        if(len(out_ap)==n_cv):
            for i in range(n_cv):
                if(out_ap[i]==1):
                    while(1):
                        sf=lte1.stas[i].nsDevice.GetPhy().IsStateSwitching()
                        sf2=wifi99.stas[0].nsDevice.GetPhy().IsStateSwitching()
                        if(sf==False and sf2==False):
                            break
                    lte1nodes[i].cmdPrint( 'ping -c 2 -s 1024 10.10.20.100 >> out_'+str('%02d' %(i+1))+'.txt' )
                elif(out_ap[i]==2):
                    while(1):
                        sf=lte2.stas[i].nsDevice.GetPhy().IsStateSwitching()
                        sf2=wifi99.stas[0].nsDevice.GetPhy().IsStateSwitching()
                        if(sf==False and sf2==False):
                            break
                    lte2nodes[i].cmdPrint( 'ping -c 2 -s 1024 10.10.20.100 >> out_'+str('%02d' %(i+1))+'.txt' )
                elif(out_ap[i]==3):
                    while(1):
                        sf=wifi1.stas[i].nsDevice.GetPhy().IsStateSwitching()
                        sf2=wifi99.stas[0].nsDevice.GetPhy().IsStateSwitching()
                        if(sf==False and sf2==False):
                            break
                    wifi1nodes[i].cmdPrint( 'ping -c 2 -s 1024 10.10.20.100 >> out_'+str('%02d' %(i+1))+'.txt' )
                elif(out_ap[i]==4):
                    while(1):
                        sf=wifi2.stas[i].nsDevice.GetPhy().IsStateSwitching()
                        sf2=wifi99.stas[0].nsDevice.GetPhy().IsStateSwitching()
                        if(sf==False and sf2==False):
                            break
                    wifi2nodes[i].cmdPrint( 'ping -c 2 -s 1024 10.10.20.100 >> out_'+str('%02d' %(i+1))+'.txt' )
                elif(out_ap[i]==5):
                    while(1):
                        sf=wifi3.stas[i].nsDevice.GetPhy().IsStateSwitching()
                        sf2=wifi99.stas[0].nsDevice.GetPhy().IsStateSwitching()
                        if(sf==False and sf2==False):
                            break
                    wifi3nodes[i].cmdPrint( 'ping -c 2 -s 1024 10.10.20.100 >> out_'+str('%02d' %(i+1))+'.txt' )
                elif(out_ap[i]==6):
                    while(1):
                        sf=wifi4.stas[i].nsDevice.GetPhy().IsStateSwitching()
                        sf2=wifi99.stas[0].nsDevice.GetPhy().IsStateSwitching()
                        if(sf==False and sf2==False):
                            break
                    wifi4nodes[i].cmdPrint( 'ping -c 2 -s 1024 10.10.20.100 >> out_'+str('%02d' %(i+1))+'.txt' )
                elif(out_ap[i]==7):
                    while(1):
                        sf=wifi5.stas[i].nsDevice.GetPhy().IsStateSwitching()
                        sf2=wifi99.stas[0].nsDevice.GetPhy().IsStateSwitching()
                        if(sf==False and sf2==False):
                            break
                    wifi5nodes[i].cmdPrint( 'ping -c 2 -s 1024 10.10.20.100 >> out_'+str('%02d' %(i+1))+'.txt' )
            time.sleep(0.1) 
            #prev_out_ap = out_ap              
    
    #CLI( net )

    info( '*** Stopping network\n' )
    mininet.ns3.stop()
    info( '*** mininet.ns3.stop()\n' )
    mininet.ns3.clear()
    info( '*** mininet.ns3.clear()\n' )
    net.stop()
    info( '*** net.stop()\n' )      

if __name__ == '__main__':
    #setLogLevel( 'info' )
    WifiLTENet()
    #sys.exit(0)
