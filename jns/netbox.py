import secrets
import configparser
from jns_rest_module import rest_module




def netbox_req(device):

    config = configparser.ConfigParser()
    config.read("/opt/django_framework/jns/info.ini")
    config_v = {
        "ini": [
            str(config["api"]["token"]), 
            str(config["api"]["url"]),
            str(config["api"]["url_options"]),
            str(config["api"]["server_name"]),
        ]
    }

    csrf_token = secrets.token_hex(16)
    
    url = f"{config_v['ini'][1]}{device}{config_v['ini'][2]}"
    
    headers = {
            "authorization" : f"Token {config_v['ini'][0]}",
            "accept" : "application/json",
            "X-CSRF-Token": csrf_token
            }
    
    api_data, rest_result = rest_module.rest_connect(
                                        config_v['ini'][3],
                                        url,
                                        headers)

    if rest_result:
    
        api_final = api_data["results"]
        api_list = []
        
        if len(api_final) == 0:

            return False, 0, 0
        
        device_id = api_final[0]["device"]["id"]
        
        for item in api_final:
                
            if item["connected_endpoints"] == None:
                pass
            
            else:
                api_dict = {'id_val': item["id"],
                            'display_val': item["display"],
                            'peer_val': item["connected_endpoints"][0]["device"]["name"],
                            }   
                api_list.append(api_dict)

        return True, api_list, device_id

    return False, 0, 0 