import requests
import json
import logging
import pymssql  
from datetime import datetime
import ConfigParser
import os

def read_config(file_path, items):
    """Read config file.
    
    Parameters
    ----------
    file_path : string 
        File path string.
    
    items : list
        List of config items.
    
    Returns
    -------
    configs dict
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open(file_path))
    return {item: dict(config.items(item)) for item in items}

def get_connection(conf_dict):
    """Get mssql db connection.
    
    Parameters
    ----------
    conf_dict : dict 
        Dict with config parameters.
    
    Returns
    -------
    db connection
    """
    if os.name=='posix':
        os.environ['TDSVER']='7.0'
    return pymssql.connect(**conf_dict)

def read_sql(conn, query, out_format='dict_list'):
    """Execute sql query and read results.
    
    Parameters
    ----------
    conn : dict 
        An open db connection.
        
    query : string
        SQL query string.
        
    out_format : string, default 'dict_list'
        Output format either dict of lists or list of dicts.
    
    Returns
    -------
    data dict
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        if out_format=='dict_list':
            result = dict(zip([column[0] for column in cursor.description],
                              [list(el) for el in zip(*[row for row in cursor.fetchall()])]))
        elif out_format=='list_dict':
            result = [dict(zip([column[0] 
                                for column in cursor.description], 
                               row)) 
                      for row in cursor.fetchall()]
        elif out_format=='dict_row':
            result = {'row_{}'.format(idx):list(row) for idx,row in enumerate(cursor.fetchall())}
            result['col_names'] = [column[0] for column in cursor.description]
    return result

def sql_fetchone(conn, query):
    """Execute sql query and read results one-by-one.
    
    Parameters
    ----------
    conn : dict 
        An open db connection.
        
    query : string
        SQL query string.
    
    Returns
    -------
    row iterator
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        result = cursor.fetchone()
        while result is not None:
            row = dict(zip(columns,result))
            yield row
            result = cursor.fetchone()
            
def execute_sql(conn, query):
    """Execute sql query without result set.
    
    Parameters
    ----------
    conn : dict 
        An open db connection.
        
    query : string
        SQL query string.
    
    Returns
    -------
    rowcount
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        rowcount = cursor.rowcount
    return rowcount

def json_text_formatter(obj):
    """JSON serializer for objects not serializable by default json code.
    
    Parameters
    ----------
    obj : obj 
        The obj to be serialized.
        
    Returns
    -------
    serial
    """
    try:
        serial = '{}'.format(obj)
        return serial
    except:
        raise TypeError ("Type not serializable")

def to_bubble(contents, user_id, view_id, end_point, config_dict):
    headers = {'Authorization': config_dict['key'], 
               'Content-Type': 'application/x-www-form-urlencoded'}
    
    # convert values to json strings (always a list)
    data = {key: json.dumps(value, default=json_text_formatter) for key, value in contents.iteritems()}
    
    # add view_id and user_id
    data['view_id'] = view_id
    data['user_id'] = user_id
    
    # send post request to bubble
    r = requests.post(config_dict['base_url'].format(end_point), 
                      headers=headers, data=data)
    return r.status_code

def to_onesignal(contents, device_id, config_dict, url=None):
    headers = {'Authorization': config_dict['key'], 'Content-Type': 'application/json'}
    data = {
        "app_id": config_dict['app_id'],
        "include_player_ids": [device_id],
        "contents": {"en": contents},
    }
    
    # add url if supplied
    if url is not None:
        data['url'] = url

    r = requests.post(config_dict['url'], headers=headers, json=data)
    # assert r.status_code == 200
    return r