"""
Audio generation module.

This module provides functions for generating audio from text using
Together AI's text-to-speech API.

Developed by Blackbeard (https://blackbeard.one | https://tentitanics.com | https://github.com/blackbeardONE)
© 2023-2024 Blackbeard. All rights reserved.
"""

import requests
from models_config import FAMOUS_MODELS, AVAILABLE_VOICES
import sys

import os

def generate_audio(api_key, text, model="cartesia/sonic-2", voice="laidback woman", output_file="output.mp3"):
    """
    Generate audio from text using Together AI's text-to-speech API.
    
    Args:
        api_key (str): The Together AI API key
        text (str): The text to convert to speech
        model (str): The model to use for text-to-speech
        voice (str): The voice to use for text-to-speech
        output_file (str): The output file path
        
    Returns:
        bool: True if audio generation was successful, False otherwise
    """
    # Ensure Audio directory exists
    audio_dir = "Audio"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
        print(f"Created directory: {audio_dir}")
    
    # Prepare the full path for the output file
    output_path = os.path.join(audio_dir, output_file)
    print(f"\nGenerating audio using {model}...")
    print(f"Text: '{text}'")
    print(f"Voice: {voice}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": "mp3"
    }
    
    try:
        response = requests.post(
            "https://api.together.ai/v1/audio/speech",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            # Save the audio content to a file
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio generated successfully and saved to {output_path}")
            return True
        else:
            print(f"⚠️ Error generating audio: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Response content: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"⚠️ Exception while generating audio: {e}")
        return False

def run_audio_generation_mode(api_key, model_name=None):
    """
    Run the audio generation mode, allowing the user to generate audio from text.
    
    Args:
        api_key (str): The Together AI API key
        model_name (str, optional): Pre-selected model name from previous step
    """
    print("\n=== AUDIO GENERATION MODE ===")
    
    audio_models = FAMOUS_MODELS["Audio Models"]
    model_info = None
    
    # If model_name is not provided, ask the user to select one
    if not model_name:
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
    else:
        # Find model info for the pre-selected model
        for model in audio_models:
            if model["name"] == model_name:
                model_info = model
                break
        
        if not model_info:
            # If model_info is not found, use the default model as fallback
            model_info = audio_models[1]  # sonic-2 is at index 1
            model_name = model_info["name"]
            print(f"Using model: {model_name}")
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
    
    # Get text to convert to speech
    text = input("\nEnter text to convert to speech: ")
    if not text:
        text = "Hello, this is a test of the Together AI text to speech system. It sounds quite natural, doesn't it?"
        print(f"Using default text: '{text}'")
    
    # Get output filename and ensure it has .mp3 extension
    output_file = input("Enter output filename (default is output.mp3): ") or "output.mp3"
    
    # Ensure the filename ends with .mp3
    if not output_file.lower().endswith('.mp3'):
        output_file += '.mp3'
        print(f"Adding .mp3 extension. Output file will be: {output_file}")
    
    # Generate the audio
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
        # Run audio generation mode again
        return run_audio_generation_mode(api_key, model_name)
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
