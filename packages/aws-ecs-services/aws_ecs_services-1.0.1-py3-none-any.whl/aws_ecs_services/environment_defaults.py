import os

REGION_DEFAULT = "eu-west-1"
OUTPUT_INFO_DEFAULT = "ip"

# Config folder
HOME_DIR = os.path.expanduser("~")
CONFIG_FOLDER = "aws_tools"
CONFIG_FILE = "config"

# By service name
IGNORED_CONTAINERS = ["ecs-agent"]  # Ignored containers
IGNORED_NAMES = ["internalecspause"]  # ignored parts of container names
