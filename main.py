
"""
Multi-agent system for AI-powered code generation.

This is the main entry point for the application, which orchestrates the
multi-agent system for generating code using AI models.

Developed by Blackbeard (https://blackbeard.one | https://tentitanics.com | https://github.com/blackbeardONE)
© 2023-2024 Blackbeard. All rights reserved.
"""

from langchain_openai import ChatOpenAI, OpenAI
from langchain_together import Together
from langchain_community.callbacks.manager import get_openai_callback
import os
import sys

# Import modules
from models_config import FAMOUS_MODELS
from api_utils import verify_openai_key, verify_together_key
from audio_gen import run_audio_generation_mode, generate_audio
from image_gen import run_image_generation_mode, generate_image
from agent_system_direct import run_multi_agent_system, talk_to_ai
from model_selection import display_famous_models_menu, list_together_models

def select_mode():
    """
    Select the mode of operation.
    
    Returns:
        str: The selected mode
    """
    print("\n=== SELECT MODE ===")
    print("1. Test LLM Provider")
    print("2. Talk to AI")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        return "test_llm"
    elif choice == "2":
        return "talk_to_ai"
    elif choice == "3":
        print("Exiting program.")
        sys.exit(0)
    else:
        print("Invalid choice. Defaulting to Test LLM Provider.")
        return "test_llm"

def select_test_llm_option():
    """
    Select the test option for LLM Provider.
    
    Returns:
        str: The selected test option
    """
    print("\n=== TEST LLM PROVIDER ===")
    print("1. General Chat/Instructions (3-Step Process)")
    print("2. Audio Generation")
    print("3. Image Generation")
    print("4. Return to previous menu")
    print("5. Return to main menu")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == "1":
        return "general_chat"
    elif choice == "2":
        return "audio_generation"
    elif choice == "3":
        return "image_generation"
    elif choice == "4":
        # Return to previous menu (main menu in this case)
        return select_mode()
    elif choice == "5":
        # Return to main menu
        main()
        sys.exit(0)
    else:
        print("Invalid choice. Defaulting to General Chat/Instructions.")
        return "general_chat"

def select_talk_to_ai_option():
    """
    Select the option for Talk to AI.
    
    Returns:
        str: The selected option
    """
    print("\n=== TALK TO AI ===")
    print("1. General Chat/Instructions")
    print("2. Audio Generation")
    print("3. Image Generation")
    print("4. Return to previous menu")
    print("5. Return to main menu")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == "1":
        return "general_chat"
    elif choice == "2":
        return "audio_generation"
    elif choice == "3":
        return "image_generation"
    elif choice == "4":
        # Return to previous menu (main menu in this case)
        return select_mode()
    elif choice == "5":
        # Return to main menu
        main()
        sys.exit(0)
    else:
        print("Invalid choice. Defaulting to General Chat/Instructions.")
        return "general_chat"

def initialize_llm(mode="general_chat"):
    """
    Initialize the language model based on user choice.
    
    Args:
        mode (str): The current mode (general_chat, audio_generation, or image_generation)
        
    Returns:
        tuple: The initialized language model, the API key, and the selected model name (for image/audio generation)
    """
    # Ask user to choose between OpenAI and Together AI
    print("Choose an LLM provider:")
    print("1. OpenAI")
    print("2. Together AI (native API)")
    print("3. Together AI (via OpenAI-compatible API)")
    print("4. Famous & Preferred Models")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        # OpenAI option
        while True:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if not openai_api_key:
                openai_api_key = input("Please enter your OpenAI API key: ")
                if not openai_api_key:
                    raise ValueError("An OpenAI API key is required to run this script")
            
            print("Verifying OpenAI API key...")
            if verify_openai_key(openai_api_key):
                print("OpenAI API key is valid!")
                return ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key), openai_api_key, None
            else:
                print("Invalid OpenAI API key. Please try again.")
                os.environ.pop("OPENAI_API_KEY", None)  # Clear the environment variable if it exists
    
    elif choice == "2":
        # Together AI option (native API)
        while True:
            together_api_key = os.environ.get("TOGETHER_API_KEY")
            if not together_api_key:
                together_api_key = input("Please enter your Together AI API key: ")
                if not together_api_key:
                    raise ValueError("A Together AI API key is required to run this script")
            
            print("Verifying Together AI API key...")
            if verify_together_key(together_api_key):
                print("Together AI API key is valid!")
                
                # Get available models from Together AI with pricing info
                model_data = list_together_models(together_api_key)
                all_models = model_data["all_models"]
                
                # Filter options
                print("\nFilter options:")
                print("1. Show all models")
                print("2. Show only free models")
                print("3. Show only paid models")
                print("4. Return to previous menu")
                print("5. Return to main menu")
                
                filter_choice = input("Enter your choice (1-5, default is 1): ") or "1"
                
                if filter_choice == "2":
                    filtered_models = model_data["free_models"]
                    print("\nShowing only FREE models:")
                elif filter_choice == "3":
                    filtered_models = model_data["paid_models"]
                    print("\nShowing only PAID models:")
                elif filter_choice == "4":
                    # Return to previous menu
                    print("Returning to previous menu...")
                    if mode == "general_chat":
                        return select_test_llm_option(), None, None
                    elif mode == "audio_generation":
                        return select_test_llm_option(), None, None
                    elif mode == "image_generation":
                        return select_test_llm_option(), None, None
                    else:
                        return select_mode(), None, None
                elif filter_choice == "5":
                    # Return to main menu
                    print("Returning to main menu...")
                    main()
                    sys.exit(0)
                else:
                    filtered_models = all_models
                    print("\nShowing ALL models:")
                
                # Display filtered models
                for i, model_id in enumerate(filtered_models, 1):
                    if model_id in model_data["model_details"]:
                        details = model_data["model_details"][model_id]
                        price_status = "Free" if details["is_free"] else "Paid"
                        print(f"{i}. {model_id} ({price_status})")
                    else:
                        print(f"{i}. {model_id}")
                
                # Let user choose a model
                model_choice = input(f"Choose a model (1-{len(filtered_models)}, default is 1): ") or "1"
                
                try:
                    model_index = int(model_choice) - 1
                    if 0 <= model_index < len(filtered_models):
                        model_name = filtered_models[model_index]
                    else:
                        print(f"Invalid choice. Using default model: {filtered_models[0]}")
                        model_name = filtered_models[0]
                except ValueError:
                    print(f"Invalid input. Using default model: {filtered_models[0]}")
                    model_name = filtered_models[0]
                
                print(f"Selected model: {model_name}")
                
                # Display model details if available
                if model_name in model_data["model_details"]:
                    details = model_data["model_details"][model_name]
                    print(f"Model type: {details['type']}")
                    print(f"Context length: {details['context_length']}")
                    print(f"Pricing: {'Free' if details['is_free'] else 'Paid'}")
                
                try:
                    return Together(
                        model=model_name,
                        temperature=0,
                        max_tokens=1000,  # Set a higher max_tokens value to avoid truncation
                        together_api_key=together_api_key
                    ), together_api_key, None
                except Exception as e:
                    print(f"\n⚠️ ERROR: Failed to initialize Together AI model: {e}")
                    print("Would you like to try another provider? (y/n)")
                    retry = input().lower()
                    if retry == 'y':
                        return initialize_llm()
                    else:
                        print("Exiting program.")
                        sys.exit(1)
            else:
                print("Invalid Together AI API key. Please try again.")
                os.environ.pop("TOGETHER_API_KEY", None)  # Clear the environment variable if it exists
    
    elif choice == "3":
        # Together AI via OpenAI-compatible API
        while True:
            together_api_key = os.environ.get("TOGETHER_API_KEY")
            if not together_api_key:
                together_api_key = input("Please enter your Together AI API key: ")
                if not together_api_key:
                    raise ValueError("A Together AI API key is required to run this script")
            
            print("Verifying Together AI API key...")
            if verify_together_key(together_api_key):
                print("Together AI API key is valid!")
                
                # Get available models from Together AI with pricing info
                model_data = list_together_models(together_api_key)
                all_models = model_data["all_models"]
                
                # Filter options
                print("\nFilter options:")
                print("1. Show all models")
                print("2. Show only free models")
                print("3. Show only paid models")
                print("4. Return to previous menu")
                print("5. Return to main menu")
                
                filter_choice = input("Enter your choice (1-5, default is 1): ") or "1"
                
                if filter_choice == "2":
                    filtered_models = model_data["free_models"]
                    print("\nShowing only FREE models:")
                elif filter_choice == "3":
                    filtered_models = model_data["paid_models"]
                    print("\nShowing only PAID models:")
                elif filter_choice == "4":
                    # Return to previous menu
                    print("Returning to previous menu...")
                    if mode == "general_chat":
                        return select_test_llm_option(), None
                    elif mode == "audio_generation":
                        return select_test_llm_option(), None
                    elif mode == "image_generation":
                        return select_test_llm_option(), None
                    else:
                        return select_mode(), None
                elif filter_choice == "5":
                    # Return to main menu
                    print("Returning to main menu...")
                    main()
                    sys.exit(0)
                else:
                    filtered_models = all_models
                    print("\nShowing ALL models:")
                
                # Display filtered models
                for i, model_id in enumerate(filtered_models, 1):
                    if model_id in model_data["model_details"]:
                        details = model_data["model_details"][model_id]
                        price_status = "Free" if details["is_free"] else "Paid"
                        print(f"{i}. {model_id} ({price_status})")
                    else:
                        print(f"{i}. {model_id}")
                
                # Let user choose a model
                model_choice = input(f"Choose a model (1-{len(filtered_models)}, default is 1): ") or "1"
                
                try:
                    model_index = int(model_choice) - 1
                    if 0 <= model_index < len(filtered_models):
                        model_name = filtered_models[model_index]
                    else:
                        print(f"Invalid choice. Using default model: {filtered_models[0]}")
                        model_name = filtered_models[0]
                except ValueError:
                    print(f"Invalid input. Using default model: {filtered_models[0]}")
                    model_name = filtered_models[0]
                
                print(f"Selected model: {model_name}")
                
                # Display model details if available
                if model_name in model_data["model_details"]:
                    details = model_data["model_details"][model_name]
                    print(f"Model type: {details['type']}")
                    print(f"Context length: {details['context_length']}")
                    print(f"Pricing: {'Free' if details['is_free'] else 'Paid'}")
                
                # Recommend API interface based on model type
                recommended_api = "1"  # Default to Chat Completions API
                if model_name in model_data["model_details"]:
                    model_type = model_data["model_details"][model_name]["type"].lower()
                    if "chat" in model_type:
                        recommended_api = "1"  # Chat Completions API
                    else:
                        recommended_api = "2"  # Completions API
                
                # Ask user which API interface to use
                print("\nChoose API interface:")
                print(f"1. Chat Completions API {'(Recommended for this model)' if recommended_api == '1' else ''}")
                print(f"2. Completions API {'(Recommended for this model)' if recommended_api == '2' else ''}")
                
                api_choice = input(f"Enter your choice (1 or 2, default is {recommended_api}): ") or recommended_api
                
                try:
                    if api_choice == "2":
                        # Use OpenAI Completions API
                        from langchain_openai import OpenAI
                        print("Using OpenAI Completions API with Together AI backend")
                        print("API Base: https://api.together.xyz/v1")
                        
                        return OpenAI(
                            temperature=0,
                            model_name=model_name,
                            openai_api_key=together_api_key,
                            openai_api_base="https://api.together.xyz/v1",
                            max_tokens=1000
                        ), together_api_key, model_name if mode in ["image_generation", "audio_generation"] else None
                    else:
                        # Use OpenAI Chat Completions API (default)
                        print("Using OpenAI Chat Completions API with Together AI backend")
                        print("API Base: https://api.together.xyz/v1")
                        
                        return ChatOpenAI(
                            temperature=0,
                            model_name=model_name,
                            openai_api_key=together_api_key,
                            openai_api_base="https://api.together.xyz/v1",
                            max_tokens=1000
                        ), together_api_key, model_name if mode in ["image_generation", "audio_generation"] else None
                except Exception as e:
                    print(f"\n⚠️ ERROR: Failed to initialize Together AI model: {e}")
                    print("Would you like to try another provider? (y/n)")
                    retry = input().lower()
                    if retry == 'y':
                        return initialize_llm()
                    else:
                        print("Exiting program.")
                        sys.exit(1)
            else:
                print("Invalid Together AI API key. Please try again.")
                os.environ.pop("TOGETHER_API_KEY", None)  # Clear the environment variable if it exists
    
    elif choice == "4":
        # Famous & Preferred Models
        while True:
            together_api_key = os.environ.get("TOGETHER_API_KEY")
            if not together_api_key:
                together_api_key = input("Please enter your Together AI API key: ")
                if not together_api_key:
                    raise ValueError("A Together AI API key is required to run this script")
            
            print("Verifying Together AI API key...")
            if verify_together_key(together_api_key):
                print("Together AI API key is valid!")
                
                # Display famous models menu with mode parameter
                all_famous_models = display_famous_models_menu(mode)
                
                # Filter models based on mode
                if mode == "general_chat":
                    filtered_famous_models = [model for model in all_famous_models 
                                             if "Chat Models" in model.get("category", "")]
                    if filtered_famous_models:  # Only use filtered list if it's not empty
                        all_famous_models = filtered_famous_models
                elif mode == "audio_generation":
                    filtered_famous_models = [model for model in all_famous_models 
                                             if "Audio Models" in model.get("category", "")]
                    if filtered_famous_models:  # Only use filtered list if it's not empty
                        all_famous_models = filtered_famous_models
                elif mode == "image_generation":
                    filtered_famous_models = [model for model in all_famous_models 
                                             if "Image Models" in model.get("category", "")]
                    if filtered_famous_models:  # Only use filtered list if it's not empty
                        all_famous_models = filtered_famous_models
                
                # Let user choose a model
                print(f"{len(all_famous_models) + 1}. Return to previous menu")
                print(f"{len(all_famous_models) + 2}. Return to main menu")
                model_choice = input(f"Choose a model (1-{len(all_famous_models) + 2}, default is 1): ") or "1"
                
                try:
                    model_index = int(model_choice) - 1
                    # Check if user wants to return to previous menu
                    if model_index == len(all_famous_models):
                        print("Returning to previous menu...")
                        return initialize_llm(mode)
                    # Check if user wants to return to main menu
                    elif model_index == len(all_famous_models) + 1:
                        print("Returning to main menu...")
                        # Re-run the main function
                        main()
                        sys.exit(0)
                    # Otherwise, select a model
                    elif 0 <= model_index < len(all_famous_models):
                        model_info = all_famous_models[model_index]
                        model_name = model_info["name"]
                    else:
                        print(f"Invalid choice. Using default model: {all_famous_models[0]['name']}")
                        model_info = all_famous_models[0]
                        model_name = model_info["name"]
                except ValueError:
                    print(f"Invalid input. Using default model: {all_famous_models[0]['name']}")
                    model_info = all_famous_models[0]
                    model_name = model_info["name"]
                
                print(f"Selected model: {model_name}")
                print(f"Description: {model_info['description']}")
                
                # Store the selected model info for later use
                selected_model_info = model_info
                
                # Determine if this is a special model
                is_special_model = model_name == "coursconnecte/meta-llama-meta-bcdb7"
                
                # Recommend API interface based on model name
                recommended_api = "1"  # Default to Chat Completions API
                if "code" in model_name.lower() or is_special_model:
                    recommended_api = "2"  # Completions API
                
                # Ask user which API interface to use
                print("\nChoose API interface:")
                print(f"1. Chat Completions API {'(Recommended for this model)' if recommended_api == '1' else ''}")
                print(f"2. Completions API {'(Recommended for this model)' if recommended_api == '2' else ''}")
                
                api_choice = input(f"Enter your choice (1 or 2, default is {recommended_api}): ") or recommended_api
                
                try:
                    if api_choice == "2":
                        # Use OpenAI Completions API
                        from langchain_openai import OpenAI
                        print("Using OpenAI Completions API with Together AI backend")
                        print("API Base: https://api.together.xyz/v1")
                        
                        return OpenAI(
                            temperature=0,
                            model_name=model_name,
                            openai_api_key=together_api_key,
                            openai_api_base="https://api.together.xyz/v1",
                            max_tokens=1000
                        ), together_api_key, model_name if mode in ["image_generation", "audio_generation"] else None
                    else:
                        # Use OpenAI Chat Completions API (default)
                        print("Using OpenAI Chat Completions API with Together AI backend")
                        print("API Base: https://api.together.xyz/v1")
                        
                        return ChatOpenAI(
                            temperature=0,
                            model_name=model_name,
                            openai_api_key=together_api_key,
                            openai_api_base="https://api.together.xyz/v1",
                            max_tokens=1000
                        ), together_api_key, model_name if mode in ["image_generation", "audio_generation"] else None
                except Exception as e:
                    print(f"\n⚠️ ERROR: Failed to initialize Together AI model: {e}")
                    print("Would you like to try another provider? (y/n)")
                    retry = input().lower()
                    if retry == 'y':
                        return initialize_llm()
                    else:
                        print("Exiting program.")
                        sys.exit(1)
            else:
                print("Invalid Together AI API key. Please try again.")
                os.environ.pop("TOGETHER_API_KEY", None)  # Clear the environment variable if it exists
    
    else:
        print("Invalid choice. Defaulting to OpenAI.")
        return initialize_llm()

def run_test_llm_general_chat(llm, *args):
    """
    Run the test LLM general chat with preconstructed instructions.
    
    Args:
        llm: The language model to use
    """
    # Define a specific task that will be consistent across all agents
    user_prompt = "Write a Python function called 'is_prime' that checks if a number is prime"
    
    # Check if we're using OpenAI for token tracking
    if isinstance(llm, ChatOpenAI) or isinstance(llm, OpenAI):
        try:
            with get_openai_callback() as cb:
                run_multi_agent_system(llm, user_prompt)
                print("\n📊 Token Usage Summary:")
                print(cb)
        except Exception as e:
            print(f"\n⚠️ ERROR during execution: {e}")
            sys.exit(1)
    else:
        # For Together AI or other providers, just run without token tracking
        run_multi_agent_system(llm, user_prompt)

def run_test_llm_audio_generation(api_key, model_name=None):
    """
    Run the test LLM audio generation with preconstructed text.
    
    Args:
        api_key: The API key to use
    """
    # Preconstructed text for audio generation
    text = "Hi this is Ten Titanics. Welcome aboard!"
    
    # Get available audio models
    audio_models = FAMOUS_MODELS["Audio Models"]
    
    # Display available audio models
    print("\nAvailable Audio Models:")
    for i, model in enumerate(audio_models, 1):
        print(f"{i}. {model['name']} - {model['description']}")
    
    # Let user choose a model
    model_choice = input(f"Choose a model (1-{len(audio_models)}, default is 2 for sonic-2): ") or "2"
    
    try:
        model_index = int(model_choice) - 1
        if 0 <= model_index < len(audio_models):
            model_info = audio_models[model_index]
            model_name = model_info["name"]
        else:
            print(f"Invalid choice. Using default model: {audio_models[1]['name']}")
            model_info = audio_models[1]
            model_name = model_info["name"]
    except ValueError:
        print(f"Invalid input. Using default model: {audio_models[1]['name']}")
        model_info = audio_models[1]
        model_name = model_info["name"]
    
    print(f"Selected model: {model_name}")
    print(f"Description: {model_info['description']}")
    
    # Display available voices
    print("\nAvailable Voices:")
    for i, voice in enumerate(AVAILABLE_VOICES, 1):
        print(f"{i}. {voice}")
    
    # Let user choose a voice
    voice_choice = input(f"Choose a voice (1-{len(AVAILABLE_VOICES)}, default is 1): ") or "1"
    
    try:
        voice_index = int(voice_choice) - 1
        if 0 <= voice_index < len(AVAILABLE_VOICES):
            voice = AVAILABLE_VOICES[voice_index]
        else:
            print(f"Invalid choice. Using default voice: {AVAILABLE_VOICES[0]}")
            voice = AVAILABLE_VOICES[0]
    except ValueError:
        print(f"Invalid input. Using default voice: {AVAILABLE_VOICES[0]}")
        voice = AVAILABLE_VOICES[0]
    
    print(f"Selected voice: {voice}")
    
    # Generate the audio
    output_file = "test_audio.mp3"
    success = generate_audio(api_key, text, model_name, voice, output_file)
    
    if success:
        audio_path = os.path.join("Audio", output_file)
        print(f"\n✅ Audio generation complete! File saved to: {audio_path}")
        print(f"You can play this file with your default audio player.")
    else:
        print("\n⚠️ Audio generation failed.")
        
    # Add options to return to previous menu, main menu, or exit
    print("\nWhat would you like to do next?")
    print("1. Generate another audio file")
    print("2. Return to previous menu")
    print("3. Return to main menu")
    print("4. Exit")
    
    next_choice = input("Enter your choice (1-4): ")
    
    if next_choice == "1":
        # Run audio generation again
        return run_test_llm_audio_generation(api_key, model_name)
    elif next_choice == "2":
        # Return to previous menu - this will be handled by the calling function
        return "previous_menu"
    elif next_choice == "3":
        # Return to main menu - this will be handled by the calling function
        return "main_menu"
    elif next_choice == "4":
        # Exit
        print("Exiting program.")
        import sys
        sys.exit(0)
    else:
        # Default to returning to previous menu
        print("Invalid choice. Returning to previous menu.")
        return "previous_menu"

def run_test_llm_image_generation(api_key, model_name=None):
    """
    Run the test LLM image generation with preconstructed prompt.
    
    Args:
        api_key: The API key to use
        model_name: The model name to use (if already selected)
    """
    # Preconstructed prompt for image generation
    prompt = "Anime photo of Donald Trump"
    
    # Get available image models
    image_models = FAMOUS_MODELS["Image Models"]
    
    # If model_name is not provided, ask the user to select one
    if not model_name:
        # Display available image models
        print("\nAvailable Image Models:")
        for i, model in enumerate(image_models, 1):
            print(f"{i}. {model['name']} - {model['description']}")
        
        # Let user choose a model
        model_choice = input(f"Choose a model (1-{len(image_models)}, default is 3 for FLUX.1-schnell): ") or "3"
        
        try:
            model_index = int(model_choice) - 1
            if 0 <= model_index < len(image_models):
                model_info = image_models[model_index]
                model_name = model_info["name"]
            else:
                # Find the FLUX.1-schnell model
                schnell_index = next((i for i, m in enumerate(image_models) if "FLUX.1-schnell" in m["name"]), 2)
                print(f"Invalid choice. Using default model: {image_models[schnell_index]['name']}")
                model_info = image_models[schnell_index]
                model_name = model_info["name"]
        except ValueError:
            # Find the FLUX.1-schnell model
            schnell_index = next((i for i, m in enumerate(image_models) if "FLUX.1-schnell" in m["name"]), 2)
            print(f"Invalid input. Using default model: {image_models[schnell_index]['name']}")
            model_info = image_models[schnell_index]
            model_name = model_info["name"]
        
        print(f"Selected model: {model_name}")
    
    # Set default parameters
    width = 1024
    height = 1024
    
    # Set steps based on model
    if "FLUX.1-schnell" in model_name:
        print("Note: FLUX.1-schnell only supports 1-12 steps")
        steps = 10  # Default for FLUX.1-schnell
    else:
        steps = 20  # Default for other models
    
    # Generate the image
    output_file = "trump_anime"
    success = generate_image(
        api_key=api_key,
        prompt=prompt,
        model=model_name,
        height=height,
        width=width,
        steps=steps,
        save_path=output_file
    )
    
    if success:
        print(f"\n✅ Image generation complete!")
        print(f"Images are saved in the 'Images' folder. You can view them in your file explorer.")
    else:
        print("\n⚠️ Image generation failed.")
        
    # Add options to return to previous menu, main menu, or exit
    print("\nWhat would you like to do next?")
    print("1. Generate another image")
    print("2. Return to previous menu")
    print("3. Return to main menu")
    print("4. Exit")
    
    next_choice = input("Enter your choice (1-4): ")
    
    if next_choice == "1":
        # Run image generation again
        return run_test_llm_image_generation(api_key, model_name)
    elif next_choice == "2":
        # Return to previous menu - this will be handled by the calling function
        return "previous_menu"
    elif next_choice == "3":
        # Return to main menu - this will be handled by the calling function
        return "main_menu"
    elif next_choice == "4":
        # Exit
        print("Exiting program.")
        import sys
        sys.exit(0)
    else:
        # Default to returning to previous menu
        print("Invalid choice. Returning to previous menu.")
        return "previous_menu"

def main():
    """
    Main function to run the multi-agent system.
    """
    try:
        # Select mode
        mode = select_mode()
        
        if mode == "test_llm":
            # Test LLM Provider mode
            test_option = select_test_llm_option()
            
            if test_option == "general_chat":
                # Initialize the LLM based on user choice
                llm, _, _ = initialize_llm("general_chat")
                # Run the test LLM general chat
                run_test_llm_general_chat(llm)
            elif test_option == "audio_generation":
                # Initialize the LLM based on user choice
                _, api_key, model_name = initialize_llm("audio_generation")
                # Run the test LLM audio generation and handle the return value
                result = run_test_llm_audio_generation(api_key, model_name)
                if result == "main_menu":
                    # Re-run the main function
                    main()
                    sys.exit(0)
                # If result is "previous_menu" or None, the function will return and the flow will continue
            elif test_option == "image_generation":
                # Initialize the LLM based on user choice
                _, api_key, model_name = initialize_llm("image_generation")
                # Run the test LLM image generation and handle the return value
                result = run_test_llm_image_generation(api_key, model_name)
                if result == "main_menu":
                    # Re-run the main function
                    main()
                    sys.exit(0)
                # If result is "previous_menu" or None, the function will return and the flow will continue
        
        elif mode == "talk_to_ai":
            # Talk to AI mode
            talk_option = select_talk_to_ai_option()
            
            if talk_option == "general_chat":
                # Initialize the LLM based on user choice
                llm, _, _ = initialize_llm("general_chat")
                # Run the talk to AI general chat
                talk_to_ai(llm)
            elif talk_option == "audio_generation":
                # Initialize the LLM based on user choice
                _, api_key, model_name = initialize_llm("audio_generation")
                # Run the audio generation mode and handle the return value
                result = run_audio_generation_mode(api_key, model_name)
                if result == "main_menu":
                    # Re-run the main function
                    main()
                    sys.exit(0)
                # If result is "previous_menu" or None, the function will return and the flow will continue
            elif talk_option == "image_generation":
                # Initialize the LLM based on user choice
                _, api_key, model_name = initialize_llm("image_generation")
                # Run the image generation mode and handle the return value
                result = run_image_generation_mode(api_key, model_name)
                if result == "main_menu":
                    # Re-run the main function
                    main()
                    sys.exit(0)
                # If result is "previous_menu" or None, the function will return and the flow will continue
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n⚠️ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
