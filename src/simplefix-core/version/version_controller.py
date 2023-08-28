from xml.etree.ElementTree import parse, ElementTree
import os


class VersionController:
    def __init__(self, fix_version: str):
        version = fix_version.replace('.', '')
        xml_file = f'{os.getcwd()}/version/simplefix-{version}/FIX{version}.xml'
        self.xml = parse(xml_file)

    @property
    def xml_tree(self) -> ElementTree:
        return self.xml
