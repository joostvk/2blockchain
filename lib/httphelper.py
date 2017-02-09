"""
    Azure Functions HTTP Helper for Python
    
    Created by Anthony Eden
    http://MediaRealm.com.au/
"""

import os
import urlparse
import re
import json

def get_param_value(param_dict, name, ptype=None, pvalues=None, pmatch=None, default=None):
    """Get parameter value from API parameter dictionary.
    
    Parameters
    ----------
    param_dict : dict 
        API parameter dict.
        
    name : string
        Parameter name.
    
    ptype : type
        Parameter type
    
    pvalues : list
        List with allowed values.
               
    pmatch : string
        Pattern value should match.    
        
    default : any
        Value to default if not present.
    
    Returns
    -------
    value
    """
    value = None
    if param_dict.has_key(name):
        value = param_dict.get(name)  # get value if present
        
        # set parameter type
        if ptype is not None:
            value = ptype(value)

        # check if value is element of pvalues
        if (pvalues is not None) and (value not in pvalues):
            msg = "Parameter {name} is not one of {vals}.".format(name=name, vals=pvalues)
            raise ValueError(msg)

        # check if in value matches pmatch
        if (pmatch is not None) and (not re.match(pmatch, value)):
            msg = "Parameter {name} does not match {patt}.".format(name=name, patt=pmatch)
            raise ValueError(msg)
    elif default is not None:
        value = default  # set to default if specified and not present
    else:
        msg = "Parameter {name} is not specified.".format(name=name)
        raise ValueError(msg)
        
    return value

class HTTPHelper(object):
    
    def __init__(self):
        self._headers = {}
        self._query = {}
        self._env = {}
        
        for x in os.environ:
            if x[:12] == "REQ_HEADERS_":
                self._headers[x[12:].lower()] = os.environ[x]
            
            elif x[:10] == "REQ_QUERY_":
                self._query[x[10:].lower()] = os.environ[x]
            
            else:
                self._env[x.lower()] = str(os.environ[x])
    
    @property
    def headers(self):
        return self._headers
    
    @property
    def get(self):
        return self._query
    
    @property
    def env(self):
        return self._env
    
    @property
    def post(self):
        postData = open(os.environ['req'], "r").read()
        print postData
        try:
            postDataParsed = json.loads(postData)
        except:
            postDataParsed = dict(urlparse.parse_qsl(postData))
        return postDataParsed