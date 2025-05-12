import os
import sys
import json
import time
import logging
import importlib

try:
    # Import the skills service module
    from ovos_core.skills.service import SkillService
    print(f"Successfully imported SkillService")
except ImportError as e:
    print(f"Failed to import SkillService: {e}")
    sys.exit(1)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

print("---- OVOS SkillsService Analysis ----")

# Create a subclass of SkillService to hook into its init method
class TestSkillService(SkillService):
    def __init__(self, **kwargs):
        print("\nTestSkillService.__init__ called with:")
        for key, value in kwargs.items():
            print(f"  {key}: {value}")
        
        # Monkey patch the bus client creation to get the params
        original_create_client = self._create_bus_client
        
        def patched_create_client(host=None, port=None, route=None, **kwargs):
            print("\n_create_bus_client called with:")
            print(f"  host: {host}")
            print(f"  port: {port}")
            print(f"  route: {route}")
            print(f"  kwargs: {kwargs}")
            return original_create_client(host=host, port=port, route=route, **kwargs)
        
        self._create_bus_client = patched_create_client
        
        # Call parent init but catch any exceptions
        try:
            print("\nCalling SkillService.__init__...")
            super().__init__(**kwargs)
            print("SkillService.__init__ completed successfully")
        except Exception as e:
            print(f"Error in SkillService.__init__: {e}")
            import traceback
            traceback.print_exc()

print("\nCreating TestSkillService instance...")
try:
    service = TestSkillService(daemonic=False)
    print("TestSkillService created successfully")
except Exception as e:
    print(f"Failed to create TestSkillService: {e}")
    import traceback
    traceback.print_exc()

# Let's try to understand what config it's loading
print("\nExamining SkillService code path...")

# Check if the MYCROFT_CONF_PATH from the environment is respected
if "MYCROFT_CONF_PATH" in os.environ:
    conf_path = os.environ["MYCROFT_CONF_PATH"]
    print(f"MYCROFT_CONF_PATH is set to: {conf_path}")
    if os.path.exists(conf_path):
        print(f"  File exists")
    else:
        print(f"  File does NOT exist")

print("\nWebSocket Client Info:")
try:
    import websocket
    print(f"  websocket-client version: {websocket.__version__}")
except ImportError:
    print("  websocket-client not found!")

print("\nTest complete.")
