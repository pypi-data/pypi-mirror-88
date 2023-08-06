#!/usr/bin/env python3
import argparse
import xml.etree.ElementTree as et
import inflection
from os import path
import sys

def main():
    parser = argparse.ArgumentParser(description = 'Update ZCross XML fields')
    group_get = parser.add_argument_group('Getters')
    group_set = parser.add_argument_group('Setters')

    xsd      = et.parse('/opt/zcross/share/zcross/zcross.xsd')
    xsd_root = xsd.getroot()

    ns = {'xs':'http://www.w3.org/2001/XMLSchema', 'zc': 'https://zcross.net', '': 'https://zcross.net', }

    tag_map = {}

    def decode_xsd_type(xsd_type):
        
        if xsd_type in ('xs:string'):
            return (str, 'STRING')
        if xsd_type in ('xs:integer','xs:int'):
            return (int, 'INT')
        if xsd_type in ('xs:boolean'):
            return (bool, 'BOOL')
        if xsd_type in ('xs:double', 'xs:decimal'):
            return (float, 'FLOAT')
        if xsd_type in ('xs:dateTime'):
            return (str, 'DATETIME')
        raise ValueError(f'Unable to decode: {xsd_type}')
        
    def decode_zc_type(xsd_root, zc_type):
        
        simple_type_xsd = xsd_root.find("xs:simpleType[@name='{}']".format(zc_type.split(':')[1]), ns)
        if simple_type_xsd is not None:
            restriction_xsd = simple_type_xsd.find("xs:restriction", ns)
            if restriction_xsd is not None:
                
                parser_type, parser_metavar = decode_xsd_type(restriction_xsd.get('base'))
                
                choices = []
                
                for enumaration_xsd in restriction_xsd.findall("xs:enumeration", ns):
                    choices.append(parser_type(enumaration_xsd.get('value')))
                
                return (parser_type, parser_metavar, choices) #TODO
          
        raise ValueError(f'Unable to decode: {zc_type}')


    def parse_xsd_attribute(xsd_root, xsd_attribute, parser, span, parent):
        attr_name = xsd_attribute.get('name')
        attr_type = xsd_attribute.get('type')
        
        parm_name = '-'.join([inflection.dasherize(inflection.underscore(p)) for p in parent + [attr_name]][-span:])
        
        parm_help = 'the {} attribute'.format(inflection.dasherize(inflection.underscore(attr_name)).replace('-',' '))
        
        if (len(parent) > 1):
            parm_help += ' of the {} element'.format(parent[-1])
        
        if attr_type.startswith('zc:'):
            parser_type, parser_metavar, parser_choices = decode_zc_type(xsd_root, attr_type)
            group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar, choices = parser_choices,  help='Set ' + parm_help)
            group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
            tag_map[parm_name] = parent + ['@' + attr_name]
        else:
            parser_type, parser_metavar = decode_xsd_type(attr_type)
            group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar,    help='Set ' + parm_help)
            group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
            tag_map[parm_name] = parent + ['@' + attr_name]

    def parse_xsd_element(xsd_root, xsd_element, parser, span, parent):
        
        if xsd_element.get('ref') is not None:
            
            if xsd_element.get('ref').startswith('zc:'):
                child_name = xsd_element.get('ref').split(':')[1]
                xsd_element_new =  xsd_root.find("xs:element[@name='{}']".format(child_name), ns)
                parse_xsd(xsd_root, xsd_element_new, parser, span, parent + [child_name])
                
        elif xsd_element.get('name') is not None:
            
            elem_name = xsd_element.get('name')
            elem_type = xsd_element.get('type')
        
            parm_name = '-'.join([inflection.dasherize(inflection.underscore(p)) for p in parent + [elem_name]][-span:])
            
            parm_help = 'the {} element'.format(parm_name.replace('-',' '))
            
           
            if elem_type.startswith('zc:'):
                parser_type, parser_metavar, parser_choices = decode_zc_type(xsd_root, elem_type)
                group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar, choices = parser_choices, help='Set ' + parm_help)
                group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
                tag_map[parm_name] = parent + [elem_name]
            else:
                parser_type, parser_metavar = decode_xsd_type(elem_type)
                group_set.add_argument('--set-' + parm_name, type=parser_type, metavar=parser_metavar, help='Set ' + parm_help)
                group_get.add_argument('--get-' + parm_name, help='Get ' + parm_help, action='store_true')
                tag_map[parm_name] =  parent + [elem_name]
            
    def parse_xsd(xsd_root, xsd_element, parser, span=2, parent=[]):

        if xsd_element.get('name') not in ('reactants', 'products'):
            for xsd_attribute in xsd_element.findall("xs:complexType/xs:attribute", ns):
                parse_xsd_attribute(xsd_root, xsd_attribute, parser, span, parent)
                    
            for xsd_subelement in xsd_element.findall("xs:complexType/xs:sequence/xs:element", ns):
                parse_xsd_element(xsd_root, xsd_subelement, parser, span, parent)
                
            for xsd_subelement in xsd_element.findall("xs:complexType/xs:choice/xs:element", ns):
                parse_xsd_element(xsd_root, xsd_subelement, parser, span + 1, parent)
                    
                   
    parser.add_argument('xml')
    parser.add_argument('database_id', nargs='?')
    parser.add_argument('group_id',    nargs='?')
    parser.add_argument('process_id',  nargs='?')

    xsd_zcross = xsd_root.find("xs:element[@name='zcross']", ns)
    parse_xsd(xsd_root, xsd_zcross, parser)

    group_set.add_argument('--set-process-bullet',     metavar='SPECIE' )
    group_set.add_argument('--set-process-target',     metavar='SPECIE' )
    group_set.add_argument('--set-process-product-1',  metavar='SPECIE' )
    group_set.add_argument('--set-process-product-2',  metavar='SPECIE' )
    group_set.add_argument('--set-process-product-3',  metavar='SPECIE' )
    group_set.add_argument('--set-process-product-4',  metavar='SPECIE' )
    group_set.add_argument('--set-process-product-5',  metavar='SPECIE' )

    group_get.add_argument('--get-process-bullet',     action='store_true' )
    group_get.add_argument('--get-process-target',     action='store_true' )
    group_get.add_argument('--get-process-product-1',  action='store_true' )
    group_get.add_argument('--get-process-product-2',  action='store_true' )
    group_get.add_argument('--get-process-product-3',  action='store_true' )
    group_get.add_argument('--get-process-product-4',  action='store_true' )
    group_get.add_argument('--get-process-product-5',  action='store_true' )

    args = parser.parse_args()

    et.register_namespace('','https://zcross.net')
    et.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    has_get = False
    has_set = False

    for arg, value in vars(args).items():
        if arg.startswith('get_') and value == True:
            has_get = True
        if arg.startswith('set_') and value is not None:
            has_set = True
        
    document = None
    document_root = None

    if path.exists(args.xml):
        document      = et.parse(args.xml)
        document_root = document.getroot()
    else:
        if has_get and not has_set:
            print(f'Unable to open file: {args.xml}')
            sys.exit(1)
        else:
            document_root = et.Element('zcross')
            document = et.ElementTree(document_root)

    def generate_xpath(path):

        tokens = []
        
        for p in path:
            if not p.startswith('@'):
                token = 'zc:' + p
                if p == 'database':
                    if args.database_id is not None:
                        token += '[@id=\'{}\']'.format(args.database_id)
                    else:
                        print("ERROR: specity the database id")
                        sys.exit(1)
                        
                if p == 'group':
                    if args.group_id is not None:
                        token += '[@id=\'{}\']'.format(args.group_id)
                    else:
                        print("ERROR: specity the group id")
                        sys.exit(1)
                        
                if p == 'process':
                    if args.process_id is not None:
                        token += '[@id=\'{}\']'.format(args.process_id)
                    else:
                        print("ERROR: specity the process id")
                        sys.exit(1)
                tokens.append(token)
                
        return '/'.join(tokens )

    for arg, value in vars(args).items():
        
        
        if arg.startswith('get_') and value == True:  
            path = tag_map[arg[4:].replace('_','-')]
              
            xpath  = generate_xpath(path)
            xattr  = None if not path[-1].startswith('@') else path[-1][1:]

            element =  document_root.find(xpath, ns)
                   
            if element is not None:
                print('{:<25} : {}'.format(arg[4:].replace('_',' '), (element.text if xattr is None else element.get(xattr)) or '')) 
            else:
                print('{:<25} : '.format(arg[4:].replace('_',' ')))
                
        elif arg.startswith('set_') and value is not None:
            path = tag_map[arg[4:].replace('_','-')]
            
            for i in range(len(path)):
                
                if not path[i].startswith('@'):
                    subelement =  document_root.find(generate_xpath(path[:i+1]), ns)
                    if subelement is None:
                        parelement = document_root.find(generate_xpath(path[:i]), ns) if len(path[:i]) > 0 else document_root
                        newelement = et.SubElement(parelement, '{https://zcross.net}'+path[i])
                        
                        if path[i] == 'database':
                            newelement.set('id', args.database_id)
                        if path[i] == 'group':
                            newelement.set('id', args.group_id)
                        if path[i] == 'process':
                            newelement.set('id', args.process_id)
                       
            element = document_root.find(generate_xpath(path[:i+1]), ns)
            xattr  = None if not path[-1].startswith('@') else path[-1][1:]
           
            if xattr is None:
               element.text = str(value)
            else:
               element.set(xattr, str(value))
                  
    if has_set:
        document.write(args.xml,
            xml_declaration = True,
            encoding = 'utf-8',
            method = 'xml')

if __name__ == "__main__":
    main()
