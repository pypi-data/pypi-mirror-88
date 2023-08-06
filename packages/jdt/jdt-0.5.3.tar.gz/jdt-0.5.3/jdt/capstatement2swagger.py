#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# Alan Viars

import argparse
import json
from collections import OrderedDict

def capstatement2swagger(input_capability_statement_file):
    error_list = []
    result = OrderedDict()
    # Open and read in the CS
    fh = open(input_capability_statement_file, 'rU')
    j = fh.read()
    j = json.loads(j, object_pairs_hook=OrderedDict)

    # Make sure it is what we are looking for
    if not isinstance(j, type(OrderedDict())):
        error_message = "File " + \
                str(input_capability_statement_file) + " did not contain a JSON object, i.e. {}."
        error_list.append(error_message)
    else:
        print(str(input_capability_statement_file), "open and loaded.")
    

    restpart = j['CapabilityStatement']['rest']
    print(json.dumps(restpart, indent=4))

    
    
    result['errors'] = error_list
    return result
    



if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser(description='Load in Capability Statement')
    parser.add_argument(
        dest='input_capability_statement_file',
        action='store',
        help='Input the Capability Statement file to load here')
    parser.add_argument(
        dest='output_openapi_file',
        action='store',
        help="Enter the output filename.  This is the openapi document suitable for Swagger.")
    args = parser.parse_args()

    result = capstatement2swagger(args.input_capability_statement_file)



    # output the summary
    print(json.dumps(result, indent=4))
