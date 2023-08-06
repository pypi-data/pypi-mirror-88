#!/usr/bin/env python

"""
Goal:
  * Get instance information (ip, id, dns) by a service's full DNS name or part of the service's name.
  * List all instance ids in a cluster.
  * list all services in a cluster.

python -m aws_ecs_services.aws_ecs_services by-service-name --region <aws_region> --cluster <ecs_cluster_name> --name <service_name>
How to:
  * Get help
    - aws_ecs_services.py -h
  * By service DNS name:
    - Getting information by a service's DNS name (AWS Route53), the tool gets the IP from this dns name and searches this IP in the list of private IPs in all the given cluster's instances.
    - aws_ecs_services.py by-service-dns -h
    - python aws_ecs_services.py by-service-dns --region <aws_region> --cluster <ecs_cluster_name> --dns <service_dns_name> --output <output_info>
  * By service name:
    - Getting the instance id by a service's name (ECS service), the tool connects to every cluster instance using AWS SSM (requires 'ssm-agent' on every instance, requires 'AWS Session Manager Plugin' locally) and returns the instance's id if the service can be found. The service is checked using regular expressions, so not the complete service name needs to be known, but the tool stops at the first match.
    - Services are found by checking running docker containerson the instances.
    - aws_ecs_services.py by-service-name -h
    - python aws_ecs_services.py by-service-name --region <aws_region> --cluster <ecs_cluster_name> --name <service_name>
    - The tool also can list every running service running:
    - python aws_ecs_services.py list-services --region <aws_region> --cluster <ecs_cluster_name>
  * List instance ids:
    - It's possible to list every available instance id in the cluster.
    - python aws_ecs_services.py list-instances
  * The tool should be used in combination with aws-vault. It uses boto3 and only works with valid AWS credentials.
  * The AWS region can be given as environemnt variable REGION
  * The AWS region can be given as argument (-r, --region)
  * If the AWS region is set both ways, REGION has precedence.
  * The ECS cluster can be given as environemnt variable CLUSTER_NAME
  * The ECS cluster can be given as argument (-c, --cluster)
  * If the ECS cluster is set both ways, CLUSTER_NAME has precedence.
  * The service's dns name can be given as environemnt variable SERVICE_DNS
  * The service's dns name can be given as argument (-d, --dns)
  * If the service's dns name is set both ways, SERVICE_DNS has precedence.
  * The oputput info can be given as environemnt variable OUTPUT_INFO
  * The output info can be given as argument (-o, --output)
  * If the output info  is set both ways, OUTPUT_INFO has precedence.
  * The service's name can be given as environemnt variable SERVICE_NAME
  * The service's name can be given as argument (-n, --name)
  * If the service's name is set both ways, SERVICE_NAME has precedence.
"""

import os
import socket
import logging
import sys
from time import sleep
import re
from threading import Thread
from queue import Queue
import string
import json
from typing import Dict, List, Optional

import boto3
import botocore

from .environment_defaults import (
    REGION_DEFAULT,
    OUTPUT_INFO_DEFAULT,
    IGNORED_CONTAINERS,
    IGNORED_NAMES,
)


logging.basicConfig()
logger = logging.getLogger("AwsGetInstance")
logger.setLevel(logging.INFO)

REGION = os.environ.get("AWS_REGION", REGION_DEFAULT)
CLUSTER_NAME = os.environ.get("CLUSTER_NAME", None)
SERVICE_DNS = os.environ.get("SERVICE_DNS", None)
SERVICE_NAME = os.environ.get("SERVICE_NAME", None)
OUTPUT_INFO = os.environ.get("OUTPUT_INFO", OUTPUT_INFO_DEFAULT)

container_queue = Queue()

# Function to display hostname and
# IP address
def get_host_ip(host_name=""):
    host_ip = ""
    try:
        host_ip = socket.gethostbyname(host_name)
    except (socket.error) as e:
        logger.error(f"Unable to get IP for '{host_name}': {str(e)}")
        sys.exit(1)
    return host_ip


def get_clusters(client=None, region=REGION):
    if not client:
        session = boto3.session.Session()
        client = session.client("ecs", region)
    try:
        clusters = client.list_clusters()["clusterArns"]
        return clusters
    except (botocore.exceptions.ClientError) as e:
        # https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_ListClusters.html
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


def describe_instances_with_cluster(
    container_instances: Optional[List] = None,
    cluster: str = CLUSTER_NAME,
    client=None,
    region: str = REGION,
):
    if not client:
        session = boto3.session.Session()
        client = session.client("ecs", region)
    try:
        instances = client.describe_container_instances(
            cluster=cluster, containerInstances=container_instances
        )["containerInstances"]
        instance_ids = []
        for instance in instances:
            if instance:
                instance_ids.append(instance.get("ec2InstanceId", None))
        return instance_ids
    except (botocore.exceptions.ClientError) as e:
        if e.response["Error"]["Code"] == "ClusterNotFoundException":
            logger.error(f"Cluster '{cluster}' not found: {str(e)}.")
        else:
            logger.error(f"Error: {str(e)}")
        sys.exit(1)


def get_tasks_information(
    task: str,
    list_tasks: str,
    cluster=CLUSTER_NAME,
    client=None,
    region=REGION,
):
    """Get AWS ECS task information.


    For the puspose of getting the EC2 instance id
    by a given AWS ECS task name,
    for now, only the 'containerInstanceArn' is fetched from the AWS ECS task.
    """
    if not client:
        session = boto3.session.Session()
        client = session.client("ecs", region)
    try:
        # Get all tasks in the cluster.
        cluster_tasks = client.list_tasks(cluster=cluster)["taskArns"]
        tasks = client.describe_tasks(cluster=cluster, tasks=cluster_tasks)[
            "tasks"
        ]
        # Filter for given task name.
        # Get instance id,
        container_instances = []
        task_name = ""
        for task_ in tasks:
            task_definition = task_.get("taskDefinitionArn", "")
            if list_tasks:
                container_instances.append(task_definition)
                continue
            container_instance_arn = task_.get("containerInstanceArn", None)
            if container_instance_arn:
                if not list_tasks:
                    if re.search(task, task_definition):
                        container_instances.append(container_instance_arn)
                        task_name = task_definition
                        break
                else:
                    container_instances.append(container_instance_arn)
        if list_tasks:
            return "\n".join(container_instances)
        instances = describe_instances_with_cluster(
            container_instances=container_instances,
            cluster=cluster,
            client=client,
            region=region,
        )
        if not instances:
            return ""
        logger.info(f"Instance '{instances[0]}' runs task '{task_name}'.")
        return instances[0]
    except (botocore.exceptions.ClientError) as e:
        # TODO: Check right error code.
        if e.response["Error"]["Code"] == "ClusterNotFoundException":
            logger.error(f"Cluster '{cluster}' not found: {str(e)}.")
        else:
            logger.error(f"Error: {str(e)}")
        sys.exit(1)


def get_instance_ids_from_cluster(
    cluster=CLUSTER_NAME, client=None, region=REGION
):
    if not client:
        session = boto3.session.Session()
        client = session.client("ecs", region)
    try:
        container_instances = client.list_container_instances(cluster=cluster)[
            "containerInstanceArns"
        ]
        return describe_instances_with_cluster(
            container_instances=container_instances,
            cluster=cluster,
            client=client,
            region=region,
        )
    except (botocore.exceptions.ClientError) as e:
        if e.response["Error"]["Code"] == "ClusterNotFoundException":
            logger.error(f"Cluster '{cluster}' not found: {str(e)}.")
        else:
            logger.error(f"Error: {str(e)}")
        sys.exit(1)


def get_instance_info_by_service_dns(
    instance_ids=None, service_ip="", client=None, region=REGION
):
    if not client:
        session = boto3.session.Session()
        client = session.client("ec2", region)
    instance_private_ip = instance_private_dns = instance_id = ""
    if instance_ids and service_ip:
        reservations = client.describe_instances(InstanceIds=instance_ids)[
            "Reservations"
        ]
        for reservation in reservations:
            instances = reservation["Instances"]
            for instance in instances:
                network_interfaces = instance.get("NetworkInterfaces", [])
                for eni in network_interfaces:
                    private_ip_address = eni.get("PrivateIpAddress", None)
                    if service_ip == private_ip_address:
                        instance_private_dns = instance.get(
                            "PrivateDnsName", None
                        )
                        instance_private_ip = instance.get(
                            "PrivateIpAddress", None
                        )
                        instance_id = instance.get("InstanceId", None)
                        break

    return instance_private_ip, instance_private_dns, instance_id


def get_containers(
    instance_id=None, service="", list_services=False, client=None
):
    logger.debug(f"Getting info from instance {instance_id}.")
    try:
        response = client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": ["sudo docker container ls --format '{{.Names}}'"]
            },
        )
    except (client.exceptions.InvalidInstanceId) as e:
        logger.error(
            f"Instance id '{instance_id}' not found. Is the 'ssm-agent' installed? {str(e)}"
        )
        # sys.exit(1)
        return
    except (botocore.exceptions.ClientError) as e:
        if e.response["Error"]["Code"] == "AccessDeniedException":
            logger.error(f"Check your role and permissions: {str(e)}.")
        return

    command_id = response["Command"]["CommandId"]

    # Get the result of the above command
    retries = 10
    output = None
    status = None
    while retries >= 0:
        retries -= 1
        sleep(1)
        result = client.get_command_invocation(
            InstanceId=instance_id, CommandId=command_id
        )
        output = result["StandardOutputContent"]
        status = result["Status"]

        logger.debug(
            f"Waiting for instance '{instance_id}' response. Status is '{status}'."
        )

        # Possible values for 'Status'
        # 'Pending'|'InProgress'|'Delayed'|'Success'|'Cancelled'|'TimedOut'|'Failed'|'Cancelling'
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_command_invocation
        if status == "Success":
            break

    if not status == "Success":
        logger.warning(
            f"Could not contact instance '{instance_id}', status is '{status}'. Is something wrong?"
        )
        return

    for container_name in output.split():
        ignore_container = False
        if container_name not in IGNORED_CONTAINERS:
            logger.debug(
                f"Checking container '{container_name}' on instance '{instance_id}'."
            )
            if not list_services:
                if re.search(service, container_name):
                    logger.info(
                        f"Instance '{instance_id}' runs container '{container_name}'."
                    )
                    container_queue.put(instance_id)
                    break
            else:
                for ignored_name in IGNORED_NAMES:
                    if re.search(ignored_name, container_name):
                        ignore_container = True
                if not ignore_container:
                    container_queue.put(container_name)

    return container_queue.qsize()


def get_instance_id_by_service_name(
    instance_ids=None,
    service="",
    list_services=False,
    client=None,
    region=REGION,
):
    if list_services:
        logger.info(f"List all deployed/running services.")
    else:
        logger.info(f"Get instance for service '{service}'.")

    if not client:
        session = boto3.session.Session()
        client = session.client("ssm", region)

    container_names = []

    if list_services:
        threads = []

    for instance_id in instance_ids:
        if list_services:
            # It's to start threads, since we need to check all instances.
            thread = Thread(
                target=get_containers,
                kwargs={
                    "instance_id": instance_id,
                    "service": service,
                    "list_services": list_services,
                    "client": client,
                },
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
        else:
            # Not using threaded approach, since the loop is exited as soon as the service is found.
            if get_containers(
                instance_id=instance_id,
                service=service,
                list_services=list_services,
                client=client,
            ):
                break

    if list_services:
        for thread in threads:
            thread.join()  # wait for end of threads

    while not container_queue.empty():
        container_names.append(container_queue.get())
        container_queue.task_done()

    if not container_names and not list_services:
        logger.error(f"Service '{service}' not found.")
    else:
        print("\n".join(container_names))


def replace_config(default: str, variable: str, local_vars: Dict) -> str:
    value = default
    # Get a list of parts of the given string.

    # The resulting tuples contain the formattable strings (like "{variable}").
    # The second position contains the name of the variable used with the string replacement.
    # Example: 'string.Formatter().parse("Hello {name}.") returns: '[('Hello ', 'name', '', None)]'.
    # So `[1]` returns the name of the variable to use for the string replacement.
    substitute_keys = [
        tup[1]
        for tup in string.Formatter().parse(default)
        if tup[1] is not None
    ]
    if substitute_keys:
        substitutes = {}
        try:
            for substitute in substitute_keys:
                substitutes.update({substitute: local_vars[substitute]})
            value = default.format(**substitutes)
        except (KeyError) as e:
            logger.error(
                f"Please check the variables in your configuration file. '{variable}': '{default}': {str(e)}"
            )

    return value


def main():
    """Provide cli arguments.

    When used as executable script with command line options.
    """

    # import aws_ecs_services.arguments as arguments
    from .arguments import get_cli_arguments

    # args = arguments.get_cli_arguments()
    args = get_cli_arguments()

    by_service_dns = False
    by_service_name = False
    by_task_name = False
    list_clusters = False
    only_instance_ids = False
    list_running_services = False
    list_running_tasks = False
    list_services = False
    list_projects = False
    use_config = False

    debug = args.debug
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Show DEBUG information.")
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(f"%(lineno)s: {logging.BASIC_FORMAT}")
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.propagate = False
    else:
        logger.setLevel(logging.INFO)

    # If a configuration file and a project are given,the configruation file is used.
    # Otherwise the cli ooptions are considerd.
    project = args.project
    # Variable replacement in config file uses '{service}'.
    service = args.service
    config = args.config
    if (
        os.path.exists(config)
        and project
        or args.subcommand
        in ("list-configured-projects", "list-configured-services")
    ):
        logger.info(f"Loading config from: '{config}'.")
        if not os.path.exists(config):
            logger.error(f"No config file: '{config}'.")
            return 1
        use_config = True

    if use_config:
        data = None
        try:
            with open(config, "r") as config_file:
                data = json.load(config_file)
        except (ValueError) as e:
            logger.error(
                f"Check the JSON sytanx in the config file '{config}': '{str(e)}'"
            )
            return 1
        logger.debug(f"Data: {data}")
        if not data or not isinstance(data, dict):
            logger.error(f"Could not load configuration: '{data}'.")
            return 1

    if use_config:
        region = data.get("region", args.region)
    else:
        region = args.region

    if use_config:
        projects = data.get("projects", {})
        if args.subcommand not in ("list-configured-projects"):
            if project not in projects:
                logger.error(
                    f"Missing configuration for project: '{project}'. Choose from {list(projects.keys())}."
                )
                return 1
            project_config = projects.get(project, None)
            if not project_config:
                logger.error(
                    f"Missing configuration for project: '{project}'. Choose from {list(projects.keys())}."
                )
                return 1
            region = project_config.get("region", region)
            cluster_name = project_config.get("cluster", "")
            # Variable replacement in config file uses '{cluster}'.
            cluster = cluster_name
            cluster_ = cluster

            # Get service-specific configuration.
            services = project_config.get("services", {})
            service_config = None
            if services:
                service_config = services.get(service, None)
                logger.debug(f"Service config: {service_config}")
                if service_config:
                    cluster_ = service_config.get("cluster", cluster_name)

            cluster_name = replace_config(cluster_, "cluster", locals())
    else:
        cluster_name = args.cluster

    logger.info(f"Working in: {region}")

    session = boto3.session.Session()
    ecs_client = session.client("ecs", region)
    ec2_client = session.client("ec2", region)
    ssm_client = session.client("ssm", region)

    if args.subcommand == "by-service-dns":
        by_service_dns = True
        if use_config:
            service_dns = project_config.get("dns", "")
            service_dns_ = service_dns
            if service_config:
                service_dns_ = service_config.get("dns", service_dns)
            service_dns = replace_config(service_dns_, "service_dns", locals())
        else:
            service_dns = args.dns
        if not service_dns:
            logger.error(f"DNS name missing.")
            return 1

        output_info = args.output
    elif args.subcommand == "by-service-name":
        by_service_name = True
        if use_config:
            service_name = project_config.get("name", "")
            service_name_ = service_name
            if service_config:
                service_name_ = service_config.get("name", service_name)
            service_name = replace_config(
                service_name_, "service_name", locals()
            )
            service_name = service_name if service_name else service
        else:
            service_name = args.name
    elif args.subcommand == "by-task-name":
        by_task_name = True
        if use_config:
            task_name = project_config.get("name", "")
            task_name_ = task_name
            if service_config:
                task_name_ = service_config.get("name", task_name)
            task_name = replace_config(task_name_, "task_name", locals())
            task_name = task_name if task_name else service
        else:
            task_name = args.name
    elif args.subcommand == "list-clusters":
        list_clusters = True
    elif args.subcommand == "list-instances":
        only_instance_ids = True
    elif args.subcommand == "list-services":
        list_running_services = True
        service_name = None
    elif args.subcommand == "list-tasks":
        list_running_tasks = True
        task_name = None
    elif args.subcommand == "list-configured-services":
        list_services = True
        service_name = None
    elif args.subcommand == "list-configured-projects":
        list_projects = True
        service_name = None

    if list_projects:
        if not use_config:
            logger.error("Only available when using a configuration file.")
            return 1
        if not projects:
            logger.error(
                "Could not load projects from configuration file: '{config}'."
            )
            return 1
        print(f"Found in {config}.")
        print(*list(projects.keys()), sep="\n")
        return

    # No 'cluster' necessary for 'list-clusters'.
    if not list_clusters and not cluster_name:
        logger.error(f"Cluster name missing.")
        return 1

    if list_services:
        if not use_config:
            logger.error("Only available when using a configuration file.")
            return 1
        if not services:
            logger.error(
                "Could not load services from configuration file: '{config}'."
            )
            return 1
        print(f"Found in {config}.")
        print(*services, sep="\n")
        return
    elif list_clusters:
        clusters = get_clusters(client=ecs_client)
        print("\n".join(clusters))
        return
    elif only_instance_ids:
        logger.info(f"Checking cluster: {cluster_name}")
        instance_ids = get_instance_ids_from_cluster(
            cluster=cluster_name, client=ecs_client
        )
        print(" ".join(instance_ids))
        return
    elif by_service_name or list_running_services:
        logger.info(f"Checking cluster: {cluster_name}")
        instance_ids = get_instance_ids_from_cluster(
            cluster=cluster_name, client=ecs_client
        )
        instance_id = get_instance_id_by_service_name(
            instance_ids=instance_ids,
            service=service_name,
            list_services=list_running_services,
            client=ssm_client,
            region=region,
        )

        return
    elif by_task_name or list_running_tasks:
        logger.info(f"Checking cluster: {cluster_name}")
        instance_ids = get_tasks_information(
            task=task_name,
            list_tasks=list_running_tasks,
            cluster=cluster_name,
            client=ecs_client,
        )
        print(instance_ids)

        return
    elif by_service_dns:
        logger.info(f"Checking cluster: {cluster_name}")
        service_ip = get_host_ip(host_name=service_dns)
        logger.info(f"IP of {service_dns} is {service_ip}")
        logger.debug(f"Output: {output_info}.")
        if output_info == "service":
            print(service_ip)
            return
        else:
            logger.debug(f"Get instance IDs for cluster:' {cluster_name}'.")
            instance_ids = get_instance_ids_from_cluster(
                cluster=cluster_name, client=ecs_client
            )
            logger.debug(instance_ids)
            logger.debug("Get instance details.")
            (
                instance_private_ip,
                instance_private_dns,
                instance_id,
            ) = get_instance_info_by_service_dns(
                instance_ids=instance_ids,
                service_ip=service_ip,
                client=ec2_client,
            )
            if output_info == "ip":
                print(instance_private_ip)
                return
            elif output_info == "id":
                print(instance_id)
                return
            elif output_info == "all":
                print(instance_private_ip, instance_id, instance_private_dns)
                return
    logger.error(f"Not the expected result - nothing accomplished.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
