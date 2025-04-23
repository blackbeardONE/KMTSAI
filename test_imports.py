"""
Test script for imports.
"""

def main():
    """
    Main function to test imports.
    """
    try:
        from langchain_openai import ChatOpenAI, OpenAI
        print("✅ langchain_openai imports successful")
    except ImportError as e:
        print(f"❌ langchain_openai import error: {e}")
    
    try:
        from langchain_together import Together
        print("✅ langchain_together imports successful")
    except ImportError as e:
        print(f"❌ langchain_together import error: {e}")
    
    try:
        from langchain_community.callbacks.manager import get_openai_callback
        print("✅ langchain_community imports successful")
    except ImportError as e:
        print(f"❌ langchain_community import error: {e}")
    
    try:
        from models_config import FAMOUS_MODELS
        print("✅ models_config imports successful")
    except ImportError as e:
        print(f"❌ models_config import error: {e}")
    
    try:
        from model_selection import display_famous_models_menu, list_together_models
        print("✅ model_selection imports successful")
    except ImportError as e:
        print(f"❌ model_selection import error: {e}")

if __name__ == "__main__":
    main()
