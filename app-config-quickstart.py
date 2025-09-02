from azure.appconfiguration.provider import (
    load,
    SettingSelector
)
from azure.core.exceptions import ResourceExistsError
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
import os
import json
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, Request, Form
from azure.appconfiguration.provider import load
from fastapi.staticfiles import StaticFiles


# # Connect to Azure App Configuration using a connection string.
# ## For Read-Write Access
connection_string = os.environ.get("AZURE_APPCONFIG_RW")

if not connection_string:
    raise ValueError("AZURE_APPCONFIG_CONNECTION_STRING environment variable not set.")
# ## For Read-Only Access
# connection_string_rw= os.environ.get("AZURE_APPCONFIG")

# Connect to Azure App Configuration using SettingSelector.
trimmed = {"test."}
selects = {
    SettingSelector(key_filter="*", label_filter="\0"), 
    SettingSelector(key_filter=".appconfig.featureflag/*", label_filter="\0"), 
    }  #.appconfig.featureflag/*
config = load(connection_string=connection_string, selects=selects)

# Find the key "message" and print its value.
print(config["message"])

# Find the key "my_json" and print the value for "key" from the dictionary.
print(config["my_json"]["key"])
 
# From the keys with trimmed prefixes, find a key with "message" and print its value.
print(config["message"])

# Print True or False to indicate if "message" is found in Azure App Configuration.
print("message found: " + str("message" in config))
print("test.message found: " + str("test.message" in config))

# FastAPI app
app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
print("Templates directory:", os.path.join(BASE_DIR, "templates"))


## ------------------- FastAPI app routes ------------------- ##

@app.get("/config/{key}")
async def get_config_value(key: str):
    try:
        value = config[key]
        return {"key": key, "value": value}
    except KeyError:
        return {"error": f"Key '{key}' not found in App Configuration."}

def get_app_config():
    return config

@app.get("/")
async def index(request: Request):
    try:
        print("Using connection string:", connection_string)
        client = AzureAppConfigurationClient.from_connection_string(connection_string)

        flags = []
        for item in client.list_configuration_settings(key_filter=".appconfig.featureflag/*"):
            print("Flag item:", item)
            # flag_json = json.loads(item.value)
            # flags.append({
            #     # "id": flag_json["id"],
            #     "enabled": flag_json.get("enabled", False)
            # })

        return templates.TemplateResponse("indexFeature.html", {"request": request, "flags": flags})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)})



@app.get("/debug")
async def debug_config(config = Depends(get_app_config)):
    return dict(config)
@app.get("/feature-enabled")
# # .appconfig.featureflag/Messages
async def is_feature_enabled(config = Depends(get_app_config)):
    val = []
    for key in config:        
        # val = config.get(key)
        val.append({key: config[key]})
    return {"feature": val }  #config.get("Messages", "not set")

@app.get("/setFeature")
# async def setFeature(key=None, value=None, config = Depends(get_app_config)):
async def setFeature(key: str, value: str):
    try:
        # You can use the same connection_string you've already set globally
        client = AzureAppConfigurationClient.from_connection_string(connection_string)

        # Set a new config setting
        setting =ConfigurationSetting(
            key=key, 
            value=value, 
            label=None
        )
        client.set_configuration_setting(setting)
        return {"feature": "set successfully"}
    
    except Exception as e:
        # Catch and return the actual error for debugging
        return {"error": str(e)}

@app.get("/deleteFeature")
# async def delete_feature(config = Depends(get_app_config)):
async def delete_feature(key:str):
    try:
        # You can use the same connection_string you've already set globally
        client = AzureAppConfigurationClient.from_connection_string(connection_string)

        # Set a new config setting
        client.delete_configuration_setting(key)
        return {"feature": "deleted successfully"}
    
    except Exception as e:
        # Catch and return the actual error for debugging
        return {"error": str(e)}
    

@app.get("/addFeature")
# async def delete_feature(config = Depends(get_app_config)):
async def add_feature(key:str):
    try:
        # You can use the same connection_string you've already set globally
        client = AzureAppConfigurationClient.from_connection_string(connection_string)
        setting = ConfigurationSetting(
            key=key, 
            value="", 
            label=None
        )
        # Set a new config setting
        client.add_configuration_setting(setting)
        return {"feature": "added successfully"}
    except ResourceExistsError:
        return {"error": f"Key '{key}' already exists."}
    except Exception as e:
        # Catch and return the actual error for debugging
        return {"error": str(e)}

@app.get("/getFeature")
# async def delete_feature(config = Depends(get_app_config)):
async def get_feature():
    try:
        # You can use the same connection_string you've already set globally
        client = AzureAppConfigurationClient.from_connection_string(connection_string)
        kv_pair = []
        for kv  in client.list_configuration_settings():
            kv_pair.append({kv.key: kv.value})
        # Set a new config setting
        # client.get_configuration_setting(key)
        
        # return {"feature": "retrieved successfully", "key": key, "value": client.get_configuration_setting(key).value}
        return {"feature": kv_pair}
    
    except Exception as e:
        # Catch and return the actual error for debugging
        return {"error": str(e)}

# @app.get("/enableDisableFeature")
# async def get_feature(config = Depends(get_app_config)):
#     import json
#     try:
#         # You can use the same connection_string you've already set globally
#         client = AzureAppConfigurationClient.from_connection_string(connection_string)  
#         flag_key = ".appconfig.featureflag/Messages" 
#         flag = client.get_configuration_setting(key=flag_key, label=None)
#         flag_data = json.loads(flag.value)
#         flag_data["enabled"] = True
#         updated_flag = ConfigurationSetting(
#             key=flag_key,
#             value=json.dumps(flag_data),
#             content_type="application/vnd.microsoft.appconfig.ff+json;charset=utf-8",
#             label=None
#         )
#         client.set_configuration_setting(updated_flag)    
#         return {"feature": "enabled successfully"}
    
#     except Exception as e:
#         # Catch and return the actual error for debugging
#         return {"error": str(e)}
# @app.get("/toggle")
# async def toggle_flag(flag: str, enable: bool):
#     try:
#         client = AzureAppConfigurationClient.from_connection_string(connection_string)
#         flag_key = f".appconfig.featureflag/{flag}"

#         setting = client.get_configuration_setting(key=flag_key, label=None)
#         flag_data = json.loads(setting.value)

#         flag_data["enabled"] = enable  # true or false from query param

#         updated_flag = ConfigurationSetting(
#             key=flag_key,
#             value=json.dumps(flag_data),
#             content_type="application/vnd.microsoft.appconfig.ff+json;charset=utf-8",
#             label=setting.label
#         )

#         client.set_configuration_setting(updated_flag)
#         return {"feature": flag, "enabled": enable}

#     except Exception as e:
#         return {"error": str(e)}
    
@app.get("/toggle")
async def toggle_flag(flag: str, enable: bool):
    try:
        client = AzureAppConfigurationClient.from_connection_string(connection_string)
        flag_key = f".appconfig.featureflag/{flag}"

        try:
            # Try to get the feature flag setting
            setting = client.get_configuration_setting(key=flag_key, label=None)
            flag_data = json.loads(setting.value)

            # Only update if needed
            if flag_data["enabled"] != enable:
                flag_data["enabled"] = enable
                updated_flag = ConfigurationSetting(
                    key=flag_key,
                    value=json.dumps(flag_data),
                    content_type="application/vnd.microsoft.appconfig.ff+json;charset=utf-8",
                    label=setting.label
                )
                client.set_configuration_setting(updated_flag)
                return {
                    "feature": flag,
                    "type": "feature_flag",
                    "enabled": enable,
                    "message": "Feature flag updated."
                }
            else:
                return {
                    "feature": flag,
                    "type": "feature_flag",
                    "enabled": enable,
                    "message": "No update needed. Already in desired state."
                }

        except Exception:
            # Not a feature flag — assume config key
            try:
                setting = client.get_configuration_setting(key=flag, label=None)
                current_value = setting.value.lower() == "true"

                if current_value != enable:
                    updated_setting = ConfigurationSetting(
                        key=flag,
                        value=str(enable).lower(),
                        label=setting.label
                    )
                    client.set_configuration_setting(updated_setting)
                    return {
                        "feature": flag,
                        "type": "config",
                        "value": str(enable).lower(),
                        "message": "Config setting updated."
                    }
                else:
                    return {
                        "feature": flag,
                        "type": "config",
                        "value": str(enable).lower(),
                        "message": "No update needed. Already in desired state."
                    }

            except Exception as inner_e:
                return {"error": f"Key not found or error toggling: {inner_e}"}

    except Exception as e:  
        return {"error": str(e)}



# @app.get("/getFeatureFlagStatus")
# async def get_feature_flag_status(key: str):
#     try:
#         client = AzureAppConfigurationClient.from_connection_string(connection_string)

#         # Construct the feature flag key format
#         flag_key = f".appconfig.featureflag/{key}"

#         # Get the feature flag setting
#         setting = client.get_configuration_setting(key=flag_key, label=None)
#         flag_data = json.loads(setting.value)

#         # Return the 'enabled' status
#         return {
#             "feature": flag_data["id"],
#             "enabled": flag_data["enabled"]
#         }

#     except Exception as e:
#         return {"error": str(e)}

@app.get("/getFeatureFlagStatus")
async def get_feature_flag_status(key: str):
    try:
        client = AzureAppConfigurationClient.from_connection_string(connection_string)

        # Try feature flag format first
        feature_flag_key = f".appconfig.featureflag/{key}"
        try:
            setting = client.get_configuration_setting(key=feature_flag_key, label=None)
            flag_data = json.loads(setting.value)

            return {
                "feature": flag_data.get("id", key),
                "type": "feature_flag",
                "enabled": flag_data.get("enabled", False),
                "description": flag_data.get("description"),
                "conditions": flag_data.get("conditions", {}),
                "raw_value": flag_data
            }

        except Exception:
            # If not a feature flag, treat as regular config setting
            setting = client.get_configuration_setting(key=key, label=None)
            value = setting.value

            # Try parsing value as JSON
            try:
                parsed_value = json.loads(value)
            except Exception:
                parsed_value = value  # plain string

            return {
                "feature": key,
                "type": "config",
                "value": parsed_value
            }

    except KeyError:
        return {"error": f"Key '{key}' not found in App Configuration."}
    except Exception as e:
        return {"error": str(e)}

