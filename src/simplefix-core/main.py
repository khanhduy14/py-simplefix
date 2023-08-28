import xml.etree.ElementTree as ET
from version.version_controller import VersionController as VC
from dictionary import *
if __name__ == '__main__':
    dic = DataDictionary('50')
    print(dic.messages[0].fields)
    # print(lambda x: x.attrib, map(xml.getroot().findall('header')[0].findall('field')))