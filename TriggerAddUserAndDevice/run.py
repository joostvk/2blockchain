import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'lib')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'env/Lib/site-packages')))
import json
from datautils import get_connection, read_config, execute_sql
from httphelper import HTTPHelper, get_param_value

UPDATE_USER_QUERY = """
UPDATE [dbo].[users] 
SET user_id = '{user_id}'
WHERE email_address = '{email_address}';
"""

UPDATE_DEVICE_QUERY = """
WITH new_entry AS (
    SELECT 
        '{user_id}' as user_id,
        '{device_id}' as device_id)
MERGE INTO [dbo].[devices] AS TARGET
USING new_entry AS SOURCE 
ON (TARGET.device_id = source.device_id)
WHEN matched THEN 
    UPDATE SET TARGET.user_id = SOURCE.user_id
WHEN NOT matched THEN
      INSERT(user_id, 
             device_id) 
      VALUES (SOURCE.user_id, 
              SOURCE.device_id);"""

http = HTTPHelper()
http_params = http.post
print "HTTP Post parameters: {}".format(http_params)

user_id = get_param_value(http_params, 'user_id', ptype=str, pmatch='^\d{13}x\d{18}$')
device_id = get_param_value(http_params, 'device_id', ptype=str, pmatch='^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$')
email_address = get_param_value(http_params, 'email_address', ptype=str, 
                                pmatch='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

config_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'app.cfg'))
config = read_config(config_path, ['alerts_db'])
with get_connection(config['alerts_db']) as conn:
    user_rowcount = execute_sql(conn, UPDATE_USER_QUERY.format(user_id=user_id,
                                                               email_address=email_address))
    device_rowcount = execute_sql(conn, UPDATE_DEVICE_QUERY.format(user_id=user_id,
                                                                   device_id=device_id))
    print 'updating {} rows in users'.format(user_rowcount)
    print 'updating {} rows in devices'.format(device_rowcount)
    
    if (user_rowcount==1) and (device_rowcount==1):
        conn.commit()
    else:
        raise Exception('Expected number of rows to be updated 1 for users and 1 for devices, observed differently.')