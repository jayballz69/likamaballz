#!/usr/bin/env python3
import os
import sys
import time
import logging
from threading import Event

# Set up extensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ovos_test")

# Import necessary modules
try:
    from ovos_bus_client import MessageBusClient
    from ovos_bus_client.message import Message
    from ovos_config import Configuration
    print("Successfully imported required modules")
except ImportError as e:
    print(f"Failed to import: {e}")
    sys.exit(1)

# Print environment and config info
print(f"MESSAGEBUS_HOST: {os.environ.get('MESSAGEBUS_HOST', 'Not set')}")
print(f"MESSAGEBUS_PORT: {os.environ.get('MESSAGEBUS_PORT', 'Not set')}")
print(f"MESSAGEBUS_ROUTE: {os.environ.get('MESSAGEBUS_ROUTE', 'Not set')}")
print(f"MYCROFT_CONF_PATH: {os.environ.get('MYCROFT_CONF_PATH', 'Not set')}")

# Load and print configuration
conf = Configuration()
print("\nMessage bus client configuration:")
print(conf.get('message_bus_client', {}))

# Simple skill-like manager for testing
class TestSkillManager:
    def __init__(self):
        print("\nInitializing TestSkillManager with no parameters")
        # Create message bus client without explicit parameters
        # This is how ovos_core/__main__.py creates the client
        self.bus = MessageBusClient()
        print(f"MessageBusClient created")
        self.ready_event = Event()
        
        # Register a test handler
        self.bus.once('mycroft.ready', self._handle_ready)
        self.bus.on('mycroft.stop', self._handle_stop)
        
    def _handle_ready(self, message):
        print(f"Received 'mycroft.ready' message: {message}")
        self.ready_event.set()
        
    def _handle_stop(self, message):
        print(f"Received 'mycroft.stop' message: {message}")
        
    def start(self):
        print("Starting the bus client...")
        self.bus.run_in_thread()
        
        timeout = 10  # seconds
        print(f"Waiting {timeout} seconds for bus to connect...")
        start_time = time.time()
        connected = self.bus.connected_event.wait(timeout)
        elapsed = time.time() - start_time
        
        if connected:
            print(f"Bus connected after {elapsed:.2f} seconds!")
            
            # Test sending a message
            print("Sending test message...")
            self.bus.emit(Message('test.message', {"source": "test_script"}))
            
            return True
        else:
            print(f"Bus failed to connect after {elapsed:.2f} seconds!")
            return False

# Run the test
manager = TestSkillManager()
success = manager.start()

if success:
    print("\nTest PASSED: Connected to message bus!")
    
    # Keep running for a bit to see messages
    print("Waiting for 10 seconds to observe any messages...")
    time.sleep(10)
    
    print("Test complete.")
else:
    print("\nTest FAILED: Could not connect to message bus!")
