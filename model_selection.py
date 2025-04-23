"""
Model selection module.

This module provides functions for listing and selecting AI models
from Together AI and the curated list of famous models.
"""

import requests
import json
from tabulate import tabulate
from models_config import FAMOUS_MODELS

def list_together_models(api_key):
    """
    List available models from Together AI with pricing information.
    
    Args:
        api_key (str): The Together AI API key
        
    Returns:
        dict: A dictionary containing model information
    """
    print("\nSearching for available models on Together AI...")
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    try:
        # Use the /models endpoint as specified in the OpenAPI spec
        response = requests.get(
            "https://api.together.xyz/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            models_data = response.json()
            if isinstance(models_data, list) and len(models_data) > 0:
                # Process and categorize models
                free_models = []
                paid_models = []
                model_details = {}
                
                for model in models_data:
                    model_id = model.get("id", "Unknown")
                    pricing = model.get("pricing", {})
                    
                    # Determine if model is free or paid
                    is_free = True
                    if pricing:
                        # Check if any pricing field is non-zero
                        for price_type, price in pricing.items():
                            if isinstance(price, (int, float)) and price > 0:
                                is_free = False
                                break
                    
                    # Store model details
                    model_details[model_id] = {
                        "id": model_id,
                        "display_name": model.get("display_name", model_id),
                        "type": model.get("type", "Unknown"),
                        "is_free": is_free,
                        "context_length": model.get("context_length", "Unknown"),
                        "pricing": pricing
                    }
                    
                    # Add to appropriate list
                    if is_free:
                        free_models.append(model_id)
                    else:
                        paid_models.append(model_id)
                
                # Display models in a tabular format
                print("\n=== FREE MODELS ===")
                free_table_data = []
                for i, model_id in enumerate(free_models, 1):
                    details = model_details[model_id]
                    free_table_data.append([
                        i, 
                        model_id, 
                        details["display_name"], 
                        details["type"],
                        details["context_length"]
                    ])
                
                print(tabulate(
                    free_table_data, 
                    headers=["#", "Model ID", "Display Name", "Type", "Context Length"],
                    tablefmt="grid"
                ))
                
                print("\n=== PAID MODELS ===")
                paid_table_data = []
                for i, model_id in enumerate(paid_models, len(free_models) + 1):
                    details = model_details[model_id]
                    pricing_info = details["pricing"]
                    price_str = ""
                    if pricing_info:
                        if "input" in pricing_info and pricing_info["input"] > 0:
                            price_str += f"Input: ${pricing_info['input']} "
                        if "output" in pricing_info and pricing_info["output"] > 0:
                            price_str += f"Output: ${pricing_info['output']}"
                    
                    paid_table_data.append([
                        i, 
                        model_id, 
                        details["display_name"], 
                        details["type"],
                        details["context_length"],
                        price_str
                    ])
                
                print(tabulate(
                    paid_table_data, 
                    headers=["#", "Model ID", "Display Name", "Type", "Context Length", "Pricing"],
                    tablefmt="grid"
                ))
                
                # Add special model
                special_model = "coursconnecte/meta-llama-meta-bcdb7"
                print(f"\n=== SPECIAL MODEL ===")
                print(f"{len(free_models) + len(paid_models) + 1}. {special_model}")
                
                # Combine all models for selection
                all_models = free_models + paid_models + [special_model]
                
                return {
                    "all_models": all_models,
                    "free_models": free_models,
                    "paid_models": paid_models,
                    "model_details": model_details
                }
            else:
                print("No models found in the response.")
        else:
            print(f"Error listing models: {response.status_code} - {response.text}")
        
        # If the first attempt fails, return a list of known working models
        print("\nCould not retrieve models list. Using known working models:")
        known_models = [
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "meta-llama/Llama-3-8b-chat-hf",
            "meta-llama/Llama-3-70b-chat-hf"
        ]
        
        # Create a simple fallback structure
        model_data = {
            "all_models": known_models + ["coursconnecte/meta-llama-meta-bcdb7"],
            "free_models": known_models,
            "paid_models": [],
            "model_details": {}
        }
        
        for i, model in enumerate(known_models, 1):
            print(f"{i}. {model} (Free - Fallback)")
            model_data["model_details"][model] = {
                "id": model,
                "display_name": model,
                "type": "Unknown",
                "is_free": True,
                "context_length": "Unknown",
                "pricing": {}
            }
        
        # Add special model
        special_model = "coursconnecte/meta-llama-meta-bcdb7"
        print(f"{len(known_models) + 1}. {special_model} (Special model)")
        
        return model_data
    
    except Exception as e:
        print(f"Error listing Together AI models: {e}")
        # Return a list of known working models
        print("\nUsing known working models:")
        known_models = [
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "meta-llama/Llama-3-8b-chat-hf",
            "meta-llama/Llama-3-70b-chat-hf"
        ]
        
        # Create a simple fallback structure
        model_data = {
            "all_models": known_models + ["coursconnecte/meta-llama-meta-bcdb7"],
            "free_models": known_models,
            "paid_models": [],
            "model_details": {}
        }
        
        for i, model in enumerate(known_models, 1):
            print(f"{i}. {model} (Free - Fallback)")
            model_data["model_details"][model] = {
                "id": model,
                "display_name": model,
                "type": "Unknown",
                "is_free": True,
                "context_length": "Unknown",
                "pricing": {}
            }
        
        # Add special model
        special_model = "coursconnecte/meta-llama-meta-bcdb7"
        print(f"{len(known_models) + 1}. {special_model} (Special model)")
        
        return model_data

def display_famous_models_menu(mode=None):
    """
    Display a menu of famous and preferred models.
    
    Args:
        mode (str, optional): The current mode (general_chat, audio_generation, or image_generation)
        
    Returns:
        list: A list of all famous models with category information
    """
    print("\n=== FAMOUS & PREFERRED MODELS ===")
    
    all_famous_models = []
    model_index = 1
    
    # Filter categories based on mode
    categories_to_display = list(FAMOUS_MODELS.keys())
    if mode == "general_chat":
        categories_to_display = ["Chat Models"]
        print("Note: Showing only Chat Models for General Chat/Instructions mode.")
    elif mode == "audio_generation":
        categories_to_display = ["Audio Models"]
        print("Note: Showing only Audio Models for Audio Generation mode.")
    elif mode == "image_generation":
        categories_to_display = ["Image Models"]
        print("Note: Showing only Image Models for Image Generation mode.")
    
    for category in categories_to_display:
        models = FAMOUS_MODELS[category]
        print(f"\n{category}:")
        for model in models:
            print(f"{model_index}. {model['name']} - {model['description']}")
            # Add category information to each model
            model_with_category = model.copy()
            model_with_category["category"] = category
            all_famous_models.append(model_with_category)
            model_index += 1
    
    # Add all models with category information (even if not displayed)
    if mode is not None:
        for category, models in FAMOUS_MODELS.items():
            if category not in categories_to_display:
                for model in models:
                    model_with_category = model.copy()
                    model_with_category["category"] = category
                    all_famous_models.append(model_with_category)
    
    return all_famous_models
