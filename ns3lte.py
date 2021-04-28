from mininet.log import info, error, warn, debug
from mininet.link import Intf, Link
from mininet.node import Switch, Node
from mininet.util import quietRun, moveIntf, errRun
from mininet.ns3 import TBIntf, setAttributes

import ns.core
import ns.network
import ns.tap_bridge
import ns.csma
import ns.wifi
import ns.mobility
import ns.propagation

allNodes = []

class LTESegment( object ):
    def __init__( self, channelHelper = ns.wifi.YansWifiChannelHelper.Default(),
                        maxChannelNumber = 11, standard = ns.wifi.WIFI_PHY_STANDARD_80211g,
                        stationManager = "ns3::ArfWifiManager", **attrs):
        self.wifiHelper = ns.wifi.WifiHelper.Default ()
        self.plm = ns.propagation.ItuR1411LosPropagationLossModel()
        #self.pdm = ns.propagation.RandomPropagationDelayModel()
        self.plm.SetFrequency(1900000000)
        setAttributes (self.wifiHelper.SetRemoteStationManager, stationManager, attrs)
        self.wifiHelper.SetStandard (standard)
        self.channel = channelHelper.Create ()
        self.maxChannelNumber = maxChannelNumber
        self.baseSsid = 'ssid'
        self.channel.SetPropagationLossModel(self.plm)
        #self.channel.SetPropagationDelayModel(self.pdm)
        self.aps = []
        self.stas = []

    def __del__( self ):
        for ap in self.aps:
            del ap
        for sta in self.stas:
            del sta
        del self.aps[:]
        del self.stas[:]

    def add( self, node, phyHelper, macHelper, port=None, intfName=None ):
        if phyHelper is None or macHelper is None:
            warn( "phyHelper and macHelper must not be none.\n" )
            return None
        if hasattr( node, 'nsNode' ) and node.nsNode is not None:
            pass
        else:
            node.nsNode = ns.network.Node()
            allNodes.append( node )
        phyHelper.SetChannel (channel = self.channel)
        device = self.wifiHelper.Install (phyHelper, macHelper, node.nsNode).Get(0)
        node.nsNode.AddDevice (device)
        device.SetAddress (ns.network.Mac48Address.Allocate ())
        node.nsNode.AddDevice (device)
        if port is None:
            port = node.newPort()
        if intfName is None:
            intfName = node.name + '-eth' + repr( port )
        tb = TBIntf( intfName, node, port, node.nsNode, device)
        return tb

    def addAp( self, node, channelNumber, ssid=None, enableQos=False, port=None, intfName=None, **attrs):
        if ssid is None:
            ssid = self.baseSsid + str(len (self.aps) + 1)
        if channelNumber <= 0 or channelNumber > self.maxChannelNumber:
            channelNumber = random.randint (1, self.maxChannelNumber)
            warn("illegal channel number, choose a random channel number %s.\n", channelNumber)
        phyHelper = ns.wifi.YansWifiPhyHelper().Default()
        phyHelper.Set ("ChannelNumber", ns.core.UintegerValue(channelNumber))
        #phyHelper.Set ("Frequency", ns.core.UintegerValue(850))
        if enableQos:
            macHelper = ns.wifi.QosWifiMacHelper.Default()
        else:
            macHelper = ns.wifi.NqosWifiMacHelper.Default()

        setAttributes (macHelper.SetType, "ns3::ApWifiMac", attrs)
        tb = self.add (node, phyHelper, macHelper, port, intfName)
        if type( ssid ) is str:
            wifissid = ns.wifi.Ssid (ssid)
        else:
            wifissid = ssid
        try:
            tb.nsDevice.GetMac ().SetAttribute ("Ssid", ns.wifi.SsidValue (wifissid))
        except:
            warn("the type of wifissid isn't ssidvalue.\n")
            wifissid = ns.wifi.Ssid (self.baseSsid + str(len (self.aps) + 1))
            tb.nsDevice.GetMac ().SetAttribute ("Ssid", ns.wifi.SsidValue (wifissid))
        self.aps.append(tb)
        return tb

    def addSta( self, node, channelNumber, ssid=None, enableQos=False, enableScan = True, port=None, intfName=None, **attrs):
        if ssid is None:
            ssid = ""
        if channelNumber <= 0 or channelNumber > self.maxChannelNumber:
            channelNumber = random.randint (1, self.maxChannelNumber)
            warn("illegal channel number, choose a random channel number %s.\n", channelNumber)
        phyHelper = ns.wifi.YansWifiPhyHelper().Default()
        phyHelper.Set ("ChannelNumber", ns.core.UintegerValue(channelNumber))
        #phyHelper.Set ("Frequency", ns.core.UintegerValue(850))
        if enableQos:
            macHelper = ns.wifi.QosWifiMacHelper.Default()
        else:
            macHelper = ns.wifi.NqosWifiMacHelper.Default()
        setAttributes (macHelper.SetType, "ns3::StaWifiMac", attrs)
        tb = self.add (node, phyHelper, macHelper, port, intfName)
        if type( ssid ) is str:
            wifissid = ns.wifi.Ssid (ssid)
        else:
            wifissid = ssid
        try:
            tb.nsDevice.GetMac ().SetAttribute ("Ssid", ns.wifi.SsidValue (wifissid))
        except:
            warn("the type of wifissid isn't ssidvalue.\n")
            tb.nsDevice.GetMac ().SetAttribute ("Ssid", ns.wifi.SsidValue (""))
        if enableScan:
            tb.nsDevice.GetMac ().SetAttribute ("ScanType", ns.core.EnumValue (ns.wifi.StaWifiMac.ACTIVE))
            tb.nsDevice.GetMac ().SetAttribute ("MaxScanningChannelNumber", ns.core.UintegerValue(self.maxChannelNumber))
        else:
            tb.nsDevice.GetMac ().SetAttribute ("ScanType", ns.core.EnumValue (ns.wifi.StaWifiMac.NOTSUPPORT))
        self.stas.append(tb)
        return tb
