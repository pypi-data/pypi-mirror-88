import xml.etree.ElementTree as ET
import requests
import dateutil.parser
from datetime import datetime

# pip requirements:
#install lxml
#install requests
#install python-dateutil

class Engine:
    #This is effectively a static in python
    ns = {'mtc': 'urn:mtconnect.com:MTConnectDevices:1.1', 's': 'urn:mtconnect.com:MTConnectStreams:1.1'}

    def __init__(self, path):
        self.url = path
        self.Devices = []
        self.__Methods = []
            
    def fromurl(path):
        engine = Engine(path);
        engine.__loadmethods(path)
        engine.__loaddevices(path)
        return engine
    
    def __loadmethods(self, path):
        # we separately load all adapter methods
        response = requests.get(path + '/agent/adapters')
        tree = ET.fromstring(response.content)
        list = []
        for a in tree.findall('Adapter'):
            deviceid = a.get('deviceID')
            # does the adapter have methods?
            methods = a.find('Methods')
            if methods:
                for m in methods.findall('Method'):
                    name = m.get('name')
                    component = m.get('component')
                    returnType = m.get('returnType')
                    adapterid = m.get('adapterName')
                    method = Method(path, adapterid, deviceid, m)
                    list.append(method)
                self.__Methods = list

    def __loaddevices(self, path):
        response = requests.get(path + '/mtc/probe')        
        tree = ET.fromstring(response.content)
        list = []
        devices = tree.find('mtc:Devices', Engine.ns)
        for device in devices.findall('mtc:Device', Engine.ns):
            d = Device(path, device)
            d._fillMethods(self.__Methods)
            list.append(d)
        self.Devices = list;

class Parameter:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Method:
    def __init__(self, path, adapterid, deviceid, element):
        self.Parameters = []
        self.name = element.get('name')
        self._path = path
        self._adapterid = adapterid

        #compose the ID
        component = element.get('component')
        if(component):
            self.parent = deviceid + '.' + component
        else:
            self.parent = deviceid

        self.id = self.parent + '.' + self.name
        self.returnType = element.get('returnType')

        #does the method have parameters?
        parameters = element.find('Parameters')
        if parameters:
            for p in parameters.findall('Parameter'):
                self.Parameters.append(Parameter(p.get('name'), p.get('type')))

    def invoke(self, params = None):
        # this is a legacy version, but allows for older Engine support
        """
        POST to [url]/agent/adapters/{adapterID}
        <CallMethod methodName="Start">
            <Parameter name="{paramName}>{paramValue}</Parameter>
        </Callmethod>
       
        """
        callnode = ET.Element('CallMethod')
        callnode.set('methodName', self.name)
        if params:
            for p in params:
                pnode = ET.SubElement(callnode, 'Parameter')
                pnode.set('name', p.name)
                pnode.text = p.value

        path = self._path + '/agent/adapters/' + self._adapterid
        data = ET.tostring(callnode)
        response = requests.put(path, data)

        #update the locally-known value on success
        if(response.status_code != 200):            
            return False
        return True


class Node:
    def __init__(self, path, element):
        self._path = path
        self.name = element.get('name')
        self.id = element.get('id')
        self.Components = []
        self.DataItems = []
        self.Methods = []

    def _getDataItems(self, path, element):
        dataitems = element.find('mtc:DataItems', Engine.ns)
        if dataitems:
            dilist = []
            for dataitem in dataitems.findall('mtc:DataItem', Engine.ns):
                dilist.append(DataItem(path, dataitem))
            self.DataItems = dilist

    def _getComponents(self, path, element):
        components = element.find('mtc:Components', Engine.ns)
        if components:
            clist = []
            for component in components.findall('mtc:Component', Engine.ns):
                clist.append(Component(path, component))
            self.Components = clist

    def _fillMethods(self, methods):
        # find all methods with us as a parent
        for m in methods:
            if self.id == m.parent:
                self.Methods.append(m)
    
    def refreshDataItems(self):
        response = requests.get(self._path + '/mtc/current?path=' + self.id)
        tree = ET.fromstring(response.content)
        streams = tree.find('s:Streams', Engine.ns)
        if streams:
            device = streams.find('s:DeviceStream', Engine.ns)
            if device:
                events = device.find('s:Events', Engine.ns)
                if events:
                    for v in events.getchildren():                        
                        diid = v.get('dataItemId')
                        for di in self.DataItems:
                            if di.id == diid:
                                di._updateValue(v.text, v.get('timestamp'))
                                break

class Device(Node):
    def __init__(self, path, element):
        super(Device, self).__init__(path, element)
        self.uuid = element.get('uuid')
        super(Device, self)._getDataItems(path, element)
        super(Device, self)._getComponents(path, element)

class Component(Node):
    def __init__(self, path, element):
        super(Component, self).__init__(path, element)
        super(Component, self)._getDataItems(path, element)
        super(Component, self)._getComponents(path, element)

class DataItem:
    def __init__(self, path, element):
        self._path = path
        self.category = element.get('category')
        self.type = element.get('type')
        self.name = element.get('name')
        self.id = element.get('id')
        self.writable = element.get('writable')
        self.valueType = element.get('valueType')

    def _updateValue(self, value, timestamp):
        if(timestamp is None):
            self.timestamp = None
        else:
            self.timestamp = dateutil.parser.parse(timestamp)

        if value is None:
            self.value = None
        else:
            if(self.valueType == 'double'):
                self.value = float(value)
            elif(self.valueType == 'boolean'):
                self.value = bool(value)
            elif(self.valueType == 'int'):
                self.value = int(value)
            elif(self.valueType == 'dateTime'):
                self.value = dateutil.parser.parse(value)
            else:
                self.value = value
    
    def setvalue(self, value):
        # this is a legacy version, but allows for older Engine support
        """
        POST to [url]/agent/data
        <DataItems>
            <DataItem dataItemId="EngineInfo.EngineLocation">
            <Value>test</Value>
            </DataItem>
        </DataItems>
        """
        if self.writable:
            datanode = ET.Element('DataItems')
            item = ET.SubElement(datanode, 'DataItem')
            item.set('dataItemId', self.id)
            valnode = ET.SubElement(item, 'Value')
            valnode.text = value

            path = self._path + '/agent/data' 
            data = ET.tostring(datanode)
            response = requests.post(path, data)

            #update the locally-known value on success
            if(response.status_code == 200):
                self.value = valnode;
                self.timestamp = datetime.now()
