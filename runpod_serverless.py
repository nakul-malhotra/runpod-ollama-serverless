#! /usr/bin/env python
import runpod
import requests
import json
from typing import Dict, Any


def handler(job):
    
    old_model = "eramax/gemma-3-27b-it-qat:q4_0"
    model = "gemma3:27b"
    base_url = "http://localhost:11434"

    # Extract input parameters
    input_data = job.get("input", {})
    prompt = input_data.get("prompt", "")
    model = input_data.get("model", model)
    sampling_params = input_data.get("sampling_params", {})
    
    # Prepare payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "num_ctx": 32768,
            "num_thread": 4,
            "temperature": sampling_params.get("temperature", 0),
            "num_predict": sampling_params.get("max_tokens", 18000),
        }
    }

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
                data = json.loads(line)
                # Format response for frontend
                yield {
                    "output": data.get("response", ""),
                    "done": data.get("done", False),
                }
            except json.JSONDecodeError:
                continue


runpod.serverless.start({"handler": handler})
