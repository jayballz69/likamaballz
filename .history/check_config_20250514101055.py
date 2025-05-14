# See AI_CODING_BASELINE_RULES.md for required practices.
import os
from ovos_config import Configuration
import json

print('MYCROFT_CONF_PATH:', os.environ.get('MYCROFT_CONF_PATH', 'Not set'))
conf = Configuration()

print('\nMessageBusClient Configuration:')
print(json.dumps(conf.get('message_bus_client', {}), indent=2))

