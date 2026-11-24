#!/usr/bin/env python3
import json
import sys

payload = json.load(sys.stdin)
tool = payload.get("toolCall", {})
args = tool.get("args", {})
command = str(args.get("CommandLine", ""))
normalized = f" {command} "

if " rm " in normalized or command.strip() == "rm" or command.strip().startswith("rm "):
    print(json.dumps({
        "decision": "deny",
        "reason": "Course hook blocks rm. Use a safer cleanup path or run rm yourself in your own terminal."
    }))
else:
    print(json.dumps({"decision": "allow"}))
