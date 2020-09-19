import docker
import sys
import os

d = docker.from_env()

# Prune the system 
print("[0/10] Cleaning all docker stuff")
os.system("docker rm -f $(docker ps -aq)")
d.networks.prune()
d.containers.prune()    

# Create docker networks :)
print("[1/10] Creating networks")
d.networks.create("net1", driver="bridge")
d.networks.create("net2", driver="bridge")

# Spin up containers
print("[2/10] Creating containers...")
d.containers.run(name="terminal1", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="terminal2", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="router", detach=True, image="emane20", privileged=True, tty=True, network="none")

# Disconnect from none
print("[3/10] Removing none network...")
d.networks.get("none").disconnect("terminal1")
d.networks.get("none").disconnect("terminal2")
d.networks.get("none").disconnect("router")
 
print("[4/10] Connecting router to nets")
d.networks.get("net1").connect("router")
d.networks.get("net2").connect("router")

# OTA Channel
print("[5/10] Connecting terminals to net...")
d.networks.get("net1").connect("terminal1")
d.networks.get("net2").connect("terminal2")

print("[6/10] Set router as dg for containers...")
d.containers.get("rad2").exec_run(cmd="emane -r -d -l 0 test-radio/platform2.xml")

# App bus



# Execute..

print("[6/10] Done !.")