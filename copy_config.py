#!/usr/bin/env python3
import os
import shutil
import json
import logging

# Set up extensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ovos_config_helper")

# Config file paths
minimal_conf = "/home/ovos/.config/mycroft/mycroft_minimal.conf"
mycroft_conf = "/home/ovos/.config/mycroft/mycroft.conf"

logger.info(f"Checking if {minimal_conf} exists")
if os.path.exists(minimal_conf):
    logger.info(f"Loading content from {minimal_conf}")
    with open(minimal_conf, "r") as f:
        config_content = f.read()
        logger.debug(f"Content: {config_content}")
    
    # Parse and validate the JSON
    try:
        config_data = json.loads(config_content)
        logger.info(f"Successfully parsed JSON from {minimal_conf}")
        
        # Back up the existing mycroft.conf if it exists
        if os.path.exists(mycroft_conf):
            backup_path = f"{mycroft_conf}.bak"
            logger.info(f"Backing up {mycroft_conf} to {backup_path}")
            shutil.copy2(mycroft_conf, backup_path)
        
        # Write the content to mycroft.conf
        logger.info(f"Writing content to {mycroft_conf}")
        with open(mycroft_conf, "w") as f:
            json.dump(config_data, f, indent=2)
        
        print(f"Successfully copied {minimal_conf} to {mycroft_conf}")
        print(f"Configuration now contains:")
        print(json.dumps(config_data, indent=2))
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        print(f"Error: {minimal_conf} contains invalid JSON: {e}")
else:
    logger.error(f"{minimal_conf} does not exist")
    print(f"Error: {minimal_conf} does not exist")
