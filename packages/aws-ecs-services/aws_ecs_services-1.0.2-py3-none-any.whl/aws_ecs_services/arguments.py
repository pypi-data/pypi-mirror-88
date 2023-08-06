import os
import argparse

from .environment_defaults import (
    HOME_DIR,
    CONFIG_FOLDER,
    CONFIG_FILE,
    REGION_DEFAULT,
    OUTPUT_INFO_DEFAULT,
)
from ._version import __version__


def get_cli_arguments():

    parser = argparse.ArgumentParser(
        description="Get ECS service info (e.g. EC2 instance id) by a given service name.",
        epilog="Example:\npython aws_ecs_services.py by-service-dns --region <aws_region> --cluster <ecs_cluster_name> --dns <service_dns_name> --output <output_info>",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    parser.add_argument(
        "--project",
        default="",
        help="Project to use. Requires a valid configuration in the config file.",
    )
    parser.add_argument(
        "--service",
        default="",
        help="Service name to connect to. Requires a valid configuration in the config file.",
    )
    parser.add_argument(
        "--config",
        default=os.path.join(
            os.path.join(os.path.join(HOME_DIR, ".config"), CONFIG_FOLDER),
            CONFIG_FILE,
        ),
        help="Configuration to use. Default configuration file: '~/.config/aws_tools/config'.",
    )

    # Same for all subcommnds
    config = argparse.ArgumentParser(add_help=False)

    config.add_argument(
        "-r", "--region", default=REGION_DEFAULT, help="AWS region."
    )
    config.add_argument(
        "-c",
        "--cluster",
        default="",
        help="AWS ECS cluster to get instances from.",
    )
    config.add_argument(
        "--debug", action="store_true", help="Show debug info."
    )

    subparsers = parser.add_subparsers(
        help="sub-command help", dest="subcommand"
    )
    subparsers.required = True

    # create the parser for the "a" command
    parser_dns = subparsers.add_parser(
        "by-service-dns",
        parents=[config],
        help="Get instance information by service's dns name.",
    )
    parser_dns.add_argument(
        "-d",
        "--dns",
        default="",
        help="DNS name of the service to find the instance for.",
    )
    parser_dns.add_argument(
        "-o",
        "--output",
        nargs="?",
        default=OUTPUT_INFO_DEFAULT,
        choices=["ip", "id", "all", "service"],
        help="Information to return to the user. 'ip' returns the instance's private IP. 'id' returns the instance's id. 'all' returns the former and the private DNS. 'service' returns the service's IP only.",
    )

    # By task name
    parser_task = subparsers.add_parser(
        "by-task-name",
        parents=[config],
        help="Get instance id by task's name.",
    )
    task_action = parser_task.add_mutually_exclusive_group()
    task_action.add_argument(
        "-n",
        "--name",
        default="",
        help="Name of the task to find the instance for.",
    )

    # By service name
    parser_service = subparsers.add_parser(
        "by-service-name",
        parents=[config],
        help="Get instance id by service's name.",
    )
    service_action = parser_service.add_mutually_exclusive_group()
    service_action.add_argument(
        "-n",
        "--name",
        default="",
        help="Name of the service to find the instance for.",
    )

    # Return all cluster instances
    subparsers.add_parser(
        "list-ec2-instances",
        parents=[config],
        help="Get all ec2 instances.",
    )
    # Return all clusters
    subparsers.add_parser(
        "list-clusters",
        parents=[config],
        help="Get all clusters.",
    )
    # Return all cluster instances
    subparsers.add_parser(
        "list-instances",
        parents=[config],
        help="Get all cluster instances.",
    )
    # Return all running cluster tasks.
    subparsers.add_parser(
        "list-tasks",
        parents=[config],
        help="Get all active cluster tasks.",
    )
    # Return all running cluster services.
    subparsers.add_parser(
        "list-services",
        parents=[config],
        help="Get all active cluster services.",
    )
    # Return all configured services.
    subparsers.add_parser(
        "list-configured-services",
        parents=[config],
        help="Get all configured services, in the config file.",
    )
    # Return all configured projects.
    subparsers.add_parser(
        "list-configured-projects",
        parents=[config],
        help="Get all configured projects, in the config file.",
    )

    return parser.parse_args()
