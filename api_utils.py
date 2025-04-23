"""
API utilities module.

This module provides functions for API key verification
for various AI service providers like OpenAI and Together AI.
"""

import requests
import json

def verify_openai_key(api_key):
    """
    Verify if an OpenAI API key is valid.
    
    Args:
        api_key (str): The OpenAI API key to verify
        
    Returns:
        bool: True if the key is valid, False otherwise
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 5
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=10
        )
        if response.status_code == 200:
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error verifying OpenAI API key: {e}")
        return False

def verify_together_key(api_key):
    """
    Verify if a Together AI API key is valid.
    
    Args:
        api_key (str): The Together AI API key to verify
        
    Returns:
        bool: True if the key is valid, False otherwise
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": "Hello",
        "max_tokens": 5
    }
    try:
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers=headers,
            data=json.dumps(data),
            timeout=10
        )
        if response.status_code == 200:
            print("\n✅ API key is valid and working")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error verifying Together AI API key: {e}")
        return False
