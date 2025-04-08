import yaml
import os
from pathlib import Path

def load_config(path):
    """
    Load configuration from a YAML file.
    
    Args:
        path (str): Path to the YAML configuration file
        
    Returns:
        dict: Loaded configuration
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_default_config():
    """
    Return default configuration values.
    
    Returns:
        dict: Default configuration
    """
    return {
        "company": "Example Company",
        "logo": None,
        "version": "1.0.0",
        "date": None,
        "author": None,
        "approved_by": None,
        "comments": None,
        "title": None,
        "pdf_options": {
            "page-size": "A4",
            "margin-top": "0.75in",
            "margin-right": "0.75in",
            "margin-bottom": "0.75in",
            "margin-left": "0.75in",
        }
    }
    
def validate_config(config):
    """
    Validate configuration and set defaults for missing values.
    
    Args:
        config (dict): Configuration dictionary to validate
        
    Returns:
        dict: Validated configuration with defaults for missing values
        
    Raises:
        ValueError: If required configuration values are missing
    """
    default_config = get_default_config()
    
    # Merge with defaults for any missing values
    for key, default_value in default_config.items():
        if key not in config:
            config[key] = default_value
    
    # PDF options need special handling as it's a nested dictionary
    if "pdf_options" not in config:
        config["pdf_options"] = default_config["pdf_options"]
    else:
        for option, value in default_config["pdf_options"].items():
            if option not in config["pdf_options"]:
                config["pdf_options"][option] = value
    
    # Date should default to today if not specified
    if not config.get("date"):
        from datetime import datetime
        config["date"] = datetime.now().strftime("%Y-%m-%d")
        
    return config

