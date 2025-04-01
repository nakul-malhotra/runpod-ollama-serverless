#! /usr/bin/env python
import runpod
import requests


def handler(job):
    base_url = "http://localhost:11434"
    payload = job["input"]["payload"]

    # Enable streaming for better performance
    # payload["stream"] = True

    resp = requests.post(
        url=f"{base_url}/api/{job['input']['method_name']}/",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    resp.encoding = "utf-8"

    return resp.json()


runpod.serverless.start({"handler": handler})
