#!/usr/bin/env python3
"""
Patch the MessageBusClient in ovos_core to add debug logging to connection parameters
"""
import os
import sys
import time
import json
from threading import Thread, Event

# Override the import path to locate ovos_core modules
sys.path.insert(0, "/usr/local/lib/python3.11/site-packages")

# Import the original bus client and then patch it
from ovos_bus_client import MessageBusClient
from ovos_utils.log import LOG, init_service_logger

# Configure logging
init_service_logger("skills")
LOG.level = 10  # DEBUG

# Store the original constructor
original_init = MessageBusClient.__init__

# Add a monkey patch to the MessageBusClient constructor to log connection parameters
def patched_init(self, host=None, port=None, route=None, ssl=None, *args, **kwargs):
    LOG.debug(f"==== MessageBusClient INIT (Patched) ====")
    LOG.debug(f"host: {host}")
    LOG.debug(f"port: {port}")
    LOG.debug(f"route: {route}")
    LOG.debug(f"ssl: {ssl}")
    LOG.debug(f"kwargs: {kwargs}")
    LOG.debug(f"Environment MESSAGEBUS_HOST: {os.environ.get('MESSAGEBUS_HOST')}")
    LOG.debug(f"Environment MESSAGEBUS_PORT: {os.environ.get('MESSAGEBUS_PORT')}")
    LOG.debug(f"Environment MESSAGEBUS_ROUTE: {os.environ.get('MESSAGEBUS_ROUTE')}")

    # Add our route if it's not set
    if route is None and host is not None:
        route = "/core"
        LOG.debug(f"Adding missing route: {route}")

    # Call the original __init__
    original_init(self, host=host, port=port, route=route, ssl=ssl, *args, **kwargs)

# Apply the monkey patch
MessageBusClient.__init__ = patched_init

# Now run the main ovos-core __main__ script
LOG.debug("==== Starting patched ovos-core ====")
from ovos_core.__main__ import main
from ovos_core.skill_manager import on_ready, on_alive, on_started

# Create custom callback to log when skills are ready
def patched_ready_hook(*args, **kwargs):
    LOG.debug("==== Skills Ready - Custom Hook Called ====")
    return on_ready(*args, **kwargs)

# Start the main loop
try:
    LOG.debug("Starting main() with patched MessageBusClient")
    main(ready_hook=patched_ready_hook)
except Exception as e:
    LOG.exception(f"Error in main(): {e}")
