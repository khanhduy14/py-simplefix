import xml.etree.ElementTree as ET
from version.version_controller import VersionController as VC
if __name__ == '__main__':
    xml = VC('40').xml_tree
    # print(tree.getroot().attrib.get('major'))
    print(xml.getroot().findall('header')[0].findall('field')[0].attrib.get('123'))


