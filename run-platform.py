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
d.networks.create("ota-net", driver="bridge")
d.networks.create("p1-net", driver="bridge")
d.networks.create("p2-net", driver="bridge")

# Spin up containers
print("[2/10] Creating containers...")
d.containers.run(name="rad1", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="rad2", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="app1", detach=True, image="emane20", privileged=True, tty=True, network="none")
d.containers.run(name="app2", detach=True, image="emane20", privileged=True, tty=True, network="none")

# Disconnect from none
print("[3/10] Removing none network...")
d.networks.get("none").disconnect("rad1")
d.networks.get("none").disconnect("rad2")
d.networks.get("none").disconnect("app1")
d.networks.get("none").disconnect("app2")
 
# OTA Channel
print("[4/10] Connecting ota net...")
d.networks.get("ota-net").connect("rad1")
d.networks.get("ota-net").connect("rad2")

# App bus
print("[5/10] Connecting app busses")
d.networks.get("p1-net").connect("rad1")
d.networks.get("p1-net").connect("app1")

d.networks.get("p2-net").connect("rad2")
d.networks.get("p2-net").connect("app2")

# Execute..
print("[6/10] Starting up emane...")
d.containers.get("rad1").exec_run(cmd="emane -r -d -l 0 test-radio/platform1.xml")
d.containers.get("rad2").exec_run(cmd="emane -r -d -l 0 test-radio/platform2.xml")

print("[7/10] Done !.")