#!/usr/bin/env python3
import json
import sys
from datetime import datetime

payload = json.load(sys.stdin)
tool = payload.get("toolCall", {})
args = tool.get("args", {})
command = str(args.get("CommandLine", ""))

with open("../agent.log", "a") as log:
    log.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} ran: {command}\n")

print(json.dumps({}))
