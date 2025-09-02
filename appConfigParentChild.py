# To enable/disable feature flag based on the parent and child enabled/disabled status in Azure App Configuration

import os 
import json
from azure.appconfiguration import AzureAppConfigurationClient, FeatureFlagConfigurationSetting
from appConfigFF import FeatureFlag 

# ---------------------------Configuration ---------------------------
connection_string = os.environ.get("AZURE_APPCONFIG_RW")
print(connection_string)
# if not connection_string:
#     raise EnvironmentError("AZURE_APPCONFIG_RW not set in environment variables.")
 
# client = AzureAppConfigurationClient.from_connection_string(connection_string)
# featFlag = FeatureFlag(label=None)

# # --------------------------- User Input ---------------------------
# parentFeatureFlag = input("Enter the parent of the feature flag (e.g., 9/ai): ").strip().strip("/")
# childFeatureFlag = input("Enter the child of the feature flag (e.g., /pageViews): ").strip()
# childFeatureFlagFull = f"{parentFeatureFlag}{childFeatureFlag}"
# label = None  # Optional: set to "dev", "prod", etc.
 
# # --------------------------- Helper Functions ---------------------------
# def get_or_create_flag(feature_id, label=None, enabled=True, description=""):
#     key = f".appconfig.featureflag/{feature_id}"
#     try:
#         setting = client.get_configuration_setting(key=key, label=label)
#         flag = FeatureFlagConfigurationSetting.deserialize(setting)
#         print(f"Retrieved flag '{feature_id}': enabled = {flag.enabled}")
#         return flag
#     except Exception:
#         print(f"Flag '{feature_id}' not found. Creating a new one.")
#         new_flag = FeatureFlagConfigurationSetting(
#             feature_id=feature_id,
#             enabled=enabled,
#             filters=[],
#             description=description,
#             label=label
#         )
#         client.set_configuration_setting(new_flag)
#         return new_flag

# def evaluate_and_enforce_flag(parent_flag, child_flag, label=None):
#     """Apply logic: enabled only if both parent and child are enabled."""
#     effective_enabled = parent_flag.enabled and child_flag.enabled
#     print(f"\nEffective Feature Status for '{child_flag.feature_id}': {'ENABLED ' if effective_enabled else 'DISABLED '}")
#     print(f"   Parent: {parent_flag.enabled}, Child: {child_flag.enabled}")
#     return effective_enabled

# # ---------------------------Main Logic ---------------------------
# try:
#     print(f"\nChecking Parent Feature Flag: '{parentFeatureFlag}'")
#     parent_flag = get_or_create_flag(parentFeatureFlag, label, enabled=True, description="Parent Feature")

#     print(f"\nChecking Child Feature Flag: '{childFeatureFlagFull}'")
#     child_flag = get_or_create_flag(childFeatureFlagFull, label, enabled=True, description="Child Feature")

#     # Apply logic and enforce
#     evaluate_and_enforce_flag(parent_flag, child_flag, label)

# # --------------------------- Optional Toggle ---------------------------
#     enDis = input("\nDo you want to toggle any feature flags? (yes/no): ").strip().lower()
#     if enDis == "yes":
#         parFF = input("Toggle the parent feature flag? (yes/no): ").strip().lower()
#         if parFF == "yes":
#             featFlag.toggleFeatureFlag(parent_flag.feature_id)

#         childFF = input("Toggle the child feature flag? (yes/no): ").strip().lower()
#         if childFF == "yes":
#             featFlag.toggleFeatureFlag(child_flag.feature_id)

#         # Refresh and re-apply logic after toggle
#         parent_flag = get_or_create_flag(parentFeatureFlag, label)
#         child_flag = get_or_create_flag(childFeatureFlagFull, label)
#         evaluate_and_enforce_flag(parent_flag, child_flag, label)
        
# except Exception as e:
#     print(f"\nError: {e}")


# from azure.identity import DefaultAzureCredential
# from azure.mgmt.appconfiguration import AppConfigurationManagementClient
# import requests
# from azure.appconfiguration import AzureAppConfigurationClient, FeatureFlagConfigurationSetting

# import os
# from azure.appconfiguration import AzureAppConfigurationClient, FeatureFlagConfigurationSetting
# import json
# # Connection
# connection_string = os.environ.get("AZURE_APPCONFIG_RW")
# client = AzureAppConfigurationClient.from_connection_string(connection_string)

# def is_feature_enabled(feature_name, label=None):
#     try:
#         config_setting = client.get_configuration_setting(
#             key=f".appconfig.featureflag/{feature_name}",
#             label=label
#         )
#         ff = FeatureFlagConfigurationSetting.deserialize(config_setting)
#         return ff.enabled
#     except Exception as e:
#         print(f"Error fetching feature flag {feature_name}: {e}")
#         return False

# # Check both parent and child
# is_parent_enabled = is_feature_enabled("A1")
# is_child_enabled = is_feature_enabled("A1/Chat")

# # Final decision logic
# if is_parent_enabled and is_child_enabled:
#     print("Feature is AVAILABLE")
# else:
#     print("Feature is NOT available")