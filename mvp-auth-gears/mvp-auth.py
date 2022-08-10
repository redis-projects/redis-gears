import json

def set_objects(event):
     # transaciton log
    execute("LPUSH", "command_log", " ".join(event))
    return execute("SET", event[1], " ".join(event[2:]))

def get_objects(event):

    # get user accessible access_ids   
    access_ids = get_access_ids(event[1]);
    if not access_ids:
        return "no access compadre";

    # Capture specific nested values to extract if required
    object_ref = '$';
    if event[-1][0] == '$':
        object_ref = event[-1]
        del event[-1]

    # Get requested objects
    try:
        r_access_ids = execute('json.mget', *event[+2:], '$.meta.accessId')

        # filter list of accessible json keys
        keys = get_accessible_keys(r_access_ids, access_ids, event[+2:])

        # return an error if no keys are accessible
        if not keys: 
            return "No access to requested keys"

        object = get_json_objects(keys, object_ref)
    except:
        return 'Something went wrong..'
    
    # check obj exists
    if not object:
        return "no object compadre";

    # TODO : tailor to only successful requests.
    # push original request to transaciton log
    execute("LPUSH", "command_log", " ".join(event))
    return object

# Get Access Keys for given user token
def get_access_ids(user_token):
    return execute("LRANGE", "mvp:auth:id:" + user_token, 0, -1)

# Check user has access
def get_accessible_keys(r_access_ids, u_access_ids, r_keys):
    keys = [];
    for idx, key in enumerate(r_keys):
        if r_access_ids[idx][2:-2] in u_access_ids:
            keys.append(key)
    return keys;

def print_events(event) -> None:
    for entry in event:
        log(str(entry))

def get_json_objects(keys, obj_ref):
    command = 'json.get'
    if len(keys) > 1: 
        command = 'json.mget'
    return execute(command, *keys, obj_ref)

# register gears functions
gb = GearsBuilder('CommandReader')
gb.map(lambda x: set_objects(x))
gb.register(trigger='setobjects')

gb = GearsBuilder('CommandReader')
gb.map(lambda x: get_objects(x))
gb.register(trigger='getobjects')