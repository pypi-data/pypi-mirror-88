# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> AgentLifeCycle handles life cycle of Cognicept Agents

import time
import docker
import boto3
import base64
import json
import os
import subprocess
import dateutil
from datetime import datetime
import re
import glob
import requests
import botocore
import shutil
from cogniceptshell.common import bcolors
from cogniceptshell.common import generate_progress_bar
from subprocess import DEVNULL

class AgentLifeCycle:

    # default configuration of containers and images
    _docker_container_names = ["cgs_diagnostics_agent","remote_intervention_agent","cgs_diagnostics_ecs_api","cgs_diagnostics_streamer_api", "cgs_bagger_server"]
    _docker_images = {}
    _docker_images["remote_intervention_agent"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/remote_intervention_agent:latest"
    _docker_images["cgs_diagnostics_agent"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_agent:latest"
    _docker_images["cgs_diagnostics_ecs_api"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_api:latest"
    _docker_images["cgs_diagnostics_streamer_api"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_diagnostics_api:latest"
    _docker_images["orbitty"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/orbitty:latest"
    _docker_images["cgs_bagger_server"] = "412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/cognicept_rosbagger:latest"
    
    def configure_containers(object, cfg):
        if("COG_AGENT_CONTAINERS" in cfg.config and "COG_AGENT_IMAGES" in cfg.config):
            container_names = cfg.config["COG_AGENT_CONTAINERS"].split(";")
            image_names = cfg.config["COG_AGENT_IMAGES"].split(";")
            if(len(image_names) == len(container_names)):
                object._docker_container_names = container_names
                object._docker_images = {}
                i = 0
                for container_name in container_names:
                    object._docker_images[container_name] = image_names[i]
                    i = i + 1
            else:
                print("`COG_AGENT_CONTAINERS` and `COG_AGENT_IMAGES` do not coincide. Using default.")

            if("COG_ORBITTY_ENABLED" in cfg.config and "COG_ORBITTY_IMAGE" in cfg.config):
                if(bool(cfg.config["COG_ORBITTY_ENABLED"])):
                    object._docker_images["orbitty"] = cfg.config["COG_ORBITTY_IMAGE"]
        else:
            print("Undefined `COG_AGENT_CONTAINERS` or `COG_AGENT_IMAGES`. Using default.")

    def get_latest_log_loc(object, args):
        # get latest log location
        latest_log_loc_file_path = os.path.expanduser(args.path+"agent/logs/latest_log_loc.txt")
        latest_log_loc = ""
        try:
            with open(latest_log_loc_file_path) as txt_file:
                latest_log_loc_temp = txt_file.readline()
                latest_log_loc_temp = latest_log_loc_temp[:-1]
                latest_log_loc = latest_log_loc_temp.replace("/$HOME/.cognicept/","")
                latest_log_loc = latest_log_loc.replace(".cognicept/","")
        except:
            cgs_agent_status = bcolors.FAIL +  "UNKNOWN" + bcolors.ENDC

        return latest_log_loc

    def get_status(object, args):
        client = docker.from_env()
        # check status of cgs_agent
        # get latest log location
        latest_log_loc = object.get_latest_log_loc(args)
        # read latest status and set for display
        file_path = os.path.expanduser(args.path+latest_log_loc+"/logDataStatus.json")
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                period_since_update = datetime.utcnow() - dateutil.parser.parse(data["timestamp"])
                if(period_since_update.seconds < 30 and period_since_update.seconds >= 0):
                    cgs_agent_status = bcolors.OKBLUE + data["message"].upper() + bcolors.ENDC
                else:
                    cgs_agent_status = bcolors.WARNING + "STALE" + bcolors.ENDC

        except:
            cgs_agent_status = bcolors.FAIL + "Error" +  bcolors.ENDC

        

        for container_name in object._docker_container_names:
            print(container_name, end = ': ', flush=True)
            try:
                container = client.containers.get(container_name)
                if container.status != "running":
                    print(bcolors.WARNING + "OFFLINE" + bcolors.ENDC)
                else:
                    if(container_name == "cgs_agent"):
                        print(cgs_agent_status)
                    elif(container_name == "remote_intervention_agent"):
                        object.parseRemoteInterventionAgentLogs(container.logs(tail=50))
                    elif(container_name == "cgs_diagnostics_agent"):
                        print(cgs_agent_status)
                    else:
                        print(bcolors.OKBLUE + "ONLINE" + bcolors.ENDC)
            except docker.errors.NotFound:
                print(bcolors.FAIL + "CONTAINER NOT FOUND" + bcolors.ENDC)

    def get_last_event(object, args):

        # get latest log location
        latest_log_loc = object.get_latest_log_loc(args)

        # read and display latest log if any
        file_path = os.path.expanduser(args.path+latest_log_loc)
        try:
            print(bcolors.OKBLUE + "Looking for the latest event log..." + bcolors.ENDC)
            # should read only latest logData#.json file and not logDataStatus.json
            list_of_log_files = [fn for fn in glob.glob(file_path + "/*.json") \
                                    if not os.path.basename(fn).endswith("logDataStatus.json")]
            latest_log_file = max(list_of_log_files, key=os.path.getctime)

            with open(latest_log_file) as json_file:
                data = json.load(json_file)
                print(bcolors.OKGREEN+"Latest Event Log:" + bcolors.ENDC)
                print(json.dumps(data, indent=4, sort_keys=True))
        except:
            print(bcolors.WARNING + "No event logs present." + bcolors.ENDC)

    def parseRemoteInterventionAgentLogs(object, logs):
        ## Parses logs to find status of remote intervention agent
        logs_lines = logs.splitlines()
        # parse logs to get current status
        ri_agent_status = {}
        ri_agent_status["AGENT"] = ""
        ri_agent_status["WEBRTC"] = ""
        ri_agent_status["WEBSOCKET"] = ""

        # find latest status of the each module (agent, webrtc, websocket)
        for line in reversed(logs_lines):
            for key,value in ri_agent_status.items():
                if(value != ""):
                    continue
                matches = re.search('^.*{}:: STATUS:: (?P<status>.*).*$'.format(key), str(line))
                if(matches is not None):
                    ri_agent_status[key] = matches.groups(0)[0]
            if(ri_agent_status["AGENT"] != "" and ri_agent_status["WEBRTC"] != "" and ri_agent_status["WEBSOCKET"] != ""):
                continue

        output_text = bcolors.OKBLUE + "ONLINE" + bcolors.ENDC

        for key,value in ri_agent_status.items():
            if(value == ""):
                #if not found, it was not yet initialized
                output_text = bcolors.WARNING + "NOT INITIALIZED" + bcolors.ENDC
                break
            if(value != "OK"):
                output_text = bcolors.WARNING +  key + value +  bcolors.ENDC
                break
        print(output_text)

    def restart(object, args):        
        object.stop(args)
        result = object.start(args)
        return result

    def start(object, args):        
        if(args.agents or (hasattr(args, 'list') and len(args.list) > 0)):
            print("Starting agents")
            result = object.run_agents(args)
        elif(args.datadog):
            print("Starting datadog")
            result = object.run_datadog(args)
        else:
            print("Starting agents") 
            result_agents = object.run_agents(args)
            print("Starting datadog")
            result_datadog = object.run_datadog(args)
            result = result_agents and result_datadog
        
        return result


    def stop(object, args):
        
        if(args.agents or (hasattr(args, 'list') and len(args.list) > 0)):
            print("Stopping agents")
            result = object.remove_agents(args)
        elif(args.datadog):
            print("Stopping datadog")
            result = object.stop_datadog(args)
        else:
            print("Stopping agents")
            result_agents = object.remove_agents(args)
            print("Stopping datadog")
            result_datadog = object.stop_datadog(args)
            result = result_agents and result_datadog
        return result

    def status(object, args):
        object.get_status(args)
        object.status_datadog(args)
        return True

    def remove_agents(object, args):

        # if list of agents is not specified, restart all
        if(not hasattr(args, 'list') or len(args.list) == 0):
            args.list = object._docker_container_names

        client = docker.from_env()
        print("STOP: ")
        flag_success = True
        for container_name in args.list:
            print("   - " + container_name, end = ': ', flush=True)
            try:
                container = client.containers.get(container_name)
                container.stop(timeout=10)
                container.remove()
                print(bcolors.OKBLUE + "DONE" + bcolors.ENDC)
            except docker.errors.NotFound:
                print(bcolors.WARNING + "NOT FOUND" + bcolors.ENDC)
                flag_success = False
            except docker.errors.APIError:
                print(bcolors.FAIL + "ERROR" + bcolors.ENDC)
                flag_success = False
        return flag_success

    def run_agents(object, args):

        # if list of agents is not specified, restart all
        if(not hasattr(args, 'list') or len(args.list) == 0):
            args.list = object._docker_container_names

        object._agent_run_options = {}
        object._agent_run_options["cgs_agent"] = {"command": "start_cognicept_agent.py","volumes":{args.config.config_path + "agent/logs/": {"bind": "/root/.cognicept/agent/logs", "mode":"rw"}},"network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_agent"] = {"command": "rosrun error_resolution_diagnoser error_resolution_diagnoser" ,"volumes":{args.config.config_path + "agent/logs/": {"bind": "/root/.cognicept/agent/logs", "mode":"rw"}} ,"network_mode": "host"}
        object._agent_run_options["ecs_server"] = {"command": "/ecs_api_server/ecs_endpoint.py","network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_ecs_api"] = {"command": "/src/ecs_endpoint.py" ,"network_mode": "host"}
        object._agent_run_options["cgs_diagnostics_streamer_api"] = {"command": "/src/streamer_endpoint.py" ,"volumes":{args.config.config_path + "runtime.env": {"bind": "/root/.cognicept/runtime.env", "mode":"rw"}},"network_mode": "host"}
        object._agent_run_options["remote_intervention_agent"] = {"command": "rosrun remote_intervention_agent cognicept_agent_node" ,"network_mode": "host"}

        if(args.config.is_ssh_enabled()):
            object._agent_run_options["remote_intervention_agent"]["volumes"] = {args.config.config_path + "ssh/id_rsa": {"bind": "/root/.ssh/id_rsa", "mode":"rw"}}

        object._agent_run_options["rosbridge"] = {"command": "roslaunch rosbridge_server rosbridge_websocket.launch" ,"network_mode": "host"}
        object._agent_run_options["test"] = {"command": "bash"}
        object._agent_run_options["cgs_bagger_server"] = {"command": "roslaunch cognicept_rosbagger cognicept_rosbagger_server.launch" ,"volumes":{args.config.config_path + "bags/": {"bind": "/root/.cognicept/bags", "mode":"rw"}} ,"network_mode": "host"}
        object._agent_run_options["other"] = {"command": "", "network_mode": "host"}
        client = docker.from_env()
        print("RUN: ")
        success_flag = True
        for container_name in args.list:
            print("   - " + container_name, end = ': ', flush=True)
            try:
                if(container_name not in object._docker_images):
                    if("COG_AGENT_CONTAINERS" in args.config.config):
                        containers = " (configured list: " + args.config.config["COG_AGENT_CONTAINERS"] +")"
                    else:
                        containers = ""
                    print(bcolors.WARNING +  "NOT FOUND" + bcolors.ENDC + containers)
                    success_flag = False
                    continue

                if(container_name in object._agent_run_options.keys()):
                    options = object._agent_run_options[container_name]
                else:
                    options = object._agent_run_options["other"]
                options["name"] = container_name
                options["detach"] = True
                options["environment"] = args.config.config
                options["restart_policy"] = {"Name":"unless-stopped"}
                options["tty"] = True
                command = options.pop("command")
                container = client.containers.run(object._docker_images[container_name], command, **options)
                print(bcolors.OKBLUE + "DONE" + bcolors.ENDC)
            except docker.errors.ContainerError:
                print(bcolors.WARNING+ "ALREADY EXISTS" + bcolors.ENDC + " (run `cognicept update`)")
            except docker.errors.ImageNotFound:
                print(bcolors.WARNING + "IMAGE NOT FOUND" + bcolors.ENDC + " (run `cognicept update`)")
                success_flag = False
            except docker.errors.APIError:
                print(bcolors.FAIL +  "DOCKER ERROR" + bcolors.ENDC)
                success_flag = False
        return success_flag

    def stop_datadog(object, args):
        sts = subprocess.Popen(
            "systemctl stop datadog-agent", shell=True).wait()
        print("Health monitor agent stopped")
        return True

    def run_datadog(object, args):
        sts = subprocess.Popen(
            "systemctl start datadog-agent", shell=True).wait()
        print("Health monitor agent started")
        return True

    def status_datadog(object, args):
        sts = subprocess.Popen(
            ["systemctl status datadog-agent", "-p"], shell=True, stdout=DEVNULL, stderr=DEVNULL).wait()
        if sts == 0:
            print("Health monitor status:" +
                  bcolors.OKBLUE + " ACTIVE" + bcolors.ENDC)
        elif sts ==4:
            print("Health monitor status:" +
                  bcolors.FAIL + " NOT FOUND" + bcolors.ENDC)
        else:
            print("Health monitor status:" +
                  bcolors.WARNING + " INACTIVE" + bcolors.ENDC)

    def run_orbitty(object, args):
        os.system("xhost +local:root")
        client = docker.from_env()
        try:
            options = {}
            options["name"] = "orbitty"
            options["detach"] = False
            options["privileged"] = True
            options["volumes"] = {}
            options["volumes"][args.config.config_path] = {"bind": "/config", "mode":"rw"}
            options["volumes"]["/tmp/.X11-unix"] = {"bind": "/tmp/.X11-unix", "mode":"rw"}
            environment = args.config.config
            environment["QT_X11_NO_MITSHM"] = 1
            environment["DISPLAY"] = ":0"
            options["environment"] = args.config.config
            options["remove"] = True
            options["tty"] = True
            command = "roslaunch orbitty orbitty.launch"
            client.containers.run(object._docker_images["orbitty"], command, **options)
        except docker.errors.ContainerError:
            print(bcolors.WARNING + "ALREADY RUNNING" + bcolors.ENDC)
        except docker.errors.ImageNotFound:
            print(bcolors.WARNING + "IMAGE NOT FOUND" + bcolors.ENDC + " (run `cognicept update`)")
        except docker.errors.APIError:
            print(bcolors.FAIL + "DOCKER ERROR" + bcolors.ENDC)
        os.system("xhost -local:root")

    def update(object, args):

        # Attempt to login to ECR client
        login_success = object.ecr_login(args)

        # If login failed, return false
        if login_success is False:
            print("You don't seem to have ECR repository permissions. Check your AWS credentials with the Cognicept team.")
            return False
        
        print("Info: This may take a while depending on your connection.")
        images = set(object._docker_images.values())
        N = len(images)
        i = 0
        success_flag = True
        for image_name in images:
            i = i + 1
            image_name_short = image_name.replace("412284733352.dkr.ecr.ap-southeast-1.amazonaws.com/", "cognicept/")
            try:
                for status in object.docker_client.pull(image_name, stream = True, decode = True):
                    if("progress" not in status):
                        status["progress"] = ""
                    if("status" not in status):
                        status["status"] = "Error"
                    terminal_size = shutil.get_terminal_size().columns

                    progress = ""
                    if("progressDetail" in status and "total" in status["progressDetail"]):
                        progress = generate_progress_bar(status["progressDetail"]["current"], status["progressDetail"]["total"], 1 , 10)
                    status = "[" + str(i) + "/" + str(N) + "] " + image_name_short + " - " + status["status"] + " " + progress
                    print('{:{terminal_size}.{terminal_size}}'.format(status, terminal_size = terminal_size), end="\r", flush=True)
                print("[" + str(i) + "/" + str(N) + "] " + image_name_short + " - " + bcolors.OKBLUE + "OK" + bcolors.ENDC + "\033[K")
            except docker.errors.ImageNotFound:
                print("[" + str(i) + "/" + str(N) + "] " + image_name_short + " - " + bcolors.FAIL + "FAILED" + bcolors.ENDC + "\033[K")
                success_flag = False
            except:
                print("[" + str(i) + "/" + str(N) + "] " + image_name_short + " - " + bcolors.FAIL + "FAILED" + bcolors.ENDC + "\033[K")
                success_flag = False
                
        print("Info: Run `cognicept restart` to redeploy updated agents.")
        return success_flag

    def construct_ecr_client(object, config_obj):
        """
        Utility function to create ECR client based on runtime.env credentials
        """
        # Get config
        local_cfg = config_obj.config

        if 'AWS_SESSION_TOKEN' in local_cfg:
            object.ecr_client = boto3.client(
                'ecr', region_name='ap-southeast-1',
                aws_access_key_id=local_cfg['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=local_cfg['AWS_SECRET_ACCESS_KEY'],
                aws_session_token=local_cfg['AWS_SESSION_TOKEN'])
        else:
            object.ecr_client = boto3.client(
                'ecr', region_name='ap-southeast-1',
                aws_access_key_id=local_cfg['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=local_cfg['AWS_SECRET_ACCESS_KEY'])

    def ecr_login(object, args):
        """
        Utility function that is called to login to ECR
        """
        # Construct client
        object.construct_ecr_client(args.config)
        num_retries = 3

        for trial in range(num_retries):
            try:
                # Get token
                token = object.ecr_client.get_authorization_token()
                # Parse username, password
                username, password = base64.b64decode(
                    token['authorizationData'][0]['authorizationToken']).decode().split(':')
                # Get registry
                registry = token['authorizationData'][0]['proxyEndpoint']
                # Login
                object.docker_client = docker.APIClient(
                    base_url='unix://var/run/docker.sock')
                object.docker_client.login(username, password,
                                    registry=registry, reauth=True)
                # Return true for successful login
                return True
            except (docker.errors.APIError, botocore.exceptions.ClientError):
                # On failure, retry
                print('Attempt #'+ str(trial+1) + bcolors.FAIL + " FAILED" + bcolors.ENDC + "\033[K")
                # Wait for 1 second before retrying
                time.sleep(1.0)
        # If the loop is completed, login failed, so return false
        return False
