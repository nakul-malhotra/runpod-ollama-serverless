#! /usr/bin/env python
import runpod
import requests
import json


def handler(job):
    base_url = "http://localhost:11434"
    payload = job["input"]["payload"]

    resp = requests.post(
        url=f"{base_url}/api/{job['input']['method_name']}/",
        headers={"Content-Type": "application/json"},
        json=payload,
        stream=True
    )
    resp.encoding = "utf-8"

    # Forward streaming response directly
    for line in resp.iter_lines():
        if line:
            try:
                chunk = json.loads(line)
                yield chunk
            except json.JSONDecodeError:
                continue


runpod.serverless.start({"handler": handler})
