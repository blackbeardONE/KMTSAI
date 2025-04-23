"""
Test script for main.py with non-interactive mode.
"""

import os
import sys
from model_selection import display_famous_models_menu

def main():
    """
    Main function to test the model_selection module.
    """
    # Display famous models menu
    all_famous_models = display_famous_models_menu()
    
    # Print the models with their categories
    print("\nModels with categories:")
    for i, model in enumerate(all_famous_models, 1):
        print(f"{i}. {model['name']} - Category: {model.get('category', 'Unknown')}")
    
    # Test filtering by category
    chat_models = [model for model in all_famous_models if "Chat Models" in model.get("category", "")]
    print(f"\nNumber of Chat Models: {len(chat_models)}")
    
    # Print the filtered models
    print("\nFiltered Chat Models:")
    for i, model in enumerate(chat_models, 1):
        print(f"{i}. {model['name']} - Category: {model.get('category', 'Unknown')}")

if __name__ == "__main__":
    main()
