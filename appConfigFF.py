from azure.identity import DefaultAzureCredential
from azure.mgmt.appconfiguration import AppConfigurationManagementClient
import requests

import os
from azure.appconfiguration import AzureAppConfigurationClient, FeatureFlagConfigurationSetting
import json 
# Connection
connection_string = os.environ.get("AZURE_APPCONFIG_RW")
# print(connection_string)
client = AzureAppConfigurationClient.from_connection_string(connection_string)
class FeatureFlag: 
    def __init__(self, label=None):     
        
        self.label = label
    
    def toggleFeatureFlag(self, flag_id):
        try:
            # Get existing feature flag
            existing = client.get_configuration_setting(
                key=f".appconfig.featureflag/{flag_id}",
                label=self.label
            )
            ff = FeatureFlagConfigurationSetting.deserialize(existing)            
            print(f"Feature flag '{flag_id}' found. Enabled: {ff.enabled}")
            
            # Toggle enabled flag    
            ff.enabled = not ff.enabled

            # Apply update
            client.set_configuration_setting(ff)
            print(f"Feature flag '{flag_id}' updated. Now ENABLED: {ff.enabled}")
            # print(f"Updated flag: {json.dumps(ff.serialize(), indent=2)}")

        except Exception as e:
            print(f"Error while updating feature flag: {e}")


# from azure.identity import DefaultAzureCredential
# from azure.mgmt.appconfiguration import AppConfigurationManagementClient
# import requests

# import os
# from azure.appconfiguration import AzureAppConfigurationClient, FeatureFlagConfigurationSetting
# import json
# # Connection
# connection_string = os.environ.get("AZURE_APPCONFIG_RW")
# client = AzureAppConfigurationClient.from_connection_string(connection_string)

# ## Feature flag info
# flag_id = "9/ai"    # just the name of the flag
# label = None      

# try:
#     # Get existing feature flag
#     existing = client.get_configuration_setting(
#         key=f".appconfig.featureflag/{flag_id}",
#         label=label
#     )
#     ff = FeatureFlagConfigurationSetting.deserialize(existing)
#     # print(ff)
#     print(f"Feature flag '{flag_id}' found. Enabled: {ff.enabled}")
#     # Toggle enabled flag
#     # new_enabled_state = not ff.enabled
#     ff.enabled = not ff.enabled

#     # Reconstruct the updated feature flag setting
#     # updated_flag = FeatureFlagConfigurationSetting(
#     #     feature_id=ff.feature_id,
#     #     enabled=new_enabled_state,
#     #     filters=ff.filters,
#     #     description=ff.description,
#     #     label=label
#     # )

#     # Apply update
#     client.set_configuration_setting(ff)
#     print(f"Feature flag '{flag_id}' updated. Now ENABLED: {ff.enabled}")
#     # print(f"Updated flag: {json.dumps(ff.serialize(), indent=2)}")

# except Exception as e:
#     print(f"Error while updating feature flag: {e}")
