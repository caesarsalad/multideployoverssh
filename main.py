from fabric import Connection
import os
import json

config = {}
try:
    with open('config.json') as json_file:
        config = json.load(json_file)
except FileNotFoundError:
    print("config.json not found")
    exit(1)

skipped_host_list = []
for host in config["hostList"]:
    print("working on host: " + host)
    kwargs = {"key_filename": config["privateKeyPath"], "passphrase": config["passphrase"]}
    conn = Connection(host, user=config["user"], port=config["port"], connect_kwargs=kwargs)

    try:
        for command in config["runCommands"]:
            print("working on command: " + command)
            conn.run(command)
    except Exception as e:
        print("could not execute err: ", e)

    print("\n")
    userInput = input("Continue? (yes y/a append to try again) Exit (e)")
    if userInput == "a":
        print("host: " + host + " skipped")
        skipped_host_list.append(host)
    if userInput == "e":
        print("exiting working on host: " + host)
        os._exit(0)

print("skipped host list", skipped_host_list)
print("\n", "Done!")
