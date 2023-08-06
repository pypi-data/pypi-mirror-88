#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from xml.etree import ElementTree


class XMLHelper(object):
    @staticmethod
    def build_node_from_string(xml_str):
        """Node for template.

        :param xml_str:
        :type xml_str: basestring
        :return:
        :rtype: xml.etree.ElementTree.Element
        """
        parser = ElementTree.XMLParser(encoding="utf-8")
        node = ElementTree.fromstring(xml_str, parser=parser)
        return node

    @staticmethod
    def read_template(template_path):
        """Read template from file.

        :param template_path:
        :return:
        :rtype: basestring
        """
        with open(template_path) as f:
            return f.read()

    @staticmethod
    def get_node_namespace(node):
        """Node namespace.

        :param node: xml node
        :type node: xml.etree.ElementTree.Element
        :return:
        :rtype: str
        """
        m = re.match(r"\{.*\}", node.tag)
        return m.group(0) if m else ""
