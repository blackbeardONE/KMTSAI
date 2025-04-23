"""
Image generation module.

This module provides functions for generating images from text prompts using
Together AI's image generation API.

Developed by Blackbeard (https://blackbeard.one | https://tentitanics.com | https://github.com/blackbeardONE)
© 2023-2024 Blackbeard. All rights reserved.
"""

import requests
import os
import base64
from models_config import FAMOUS_MODELS
import sys

def generate_image(api_key, prompt, model="black-forest-labs/FLUX.1-schnell", 
                  negative_prompt=None, height=1024, width=1024, steps=20, 
                  guidance=3.5, output_format="jpeg", response_format="base64", 
                  seed=None, n=1, save_path="output_image", reference_image=None):
    """
    Generate an image from a text prompt using Together AI's image generation API.
    
    Args:
        api_key (str): The Together AI API key
        prompt (str): The text prompt describing the desired image
        model (str): The model to use for image generation
        negative_prompt (str, optional): The prompt or prompts not to guide the image generation
        height (int): Height of the image to generate in pixels
        width (int): Width of the image to generate in pixels
        steps (int): Number of generation steps
        guidance (float): Adjusts the alignment of the generated image with the input prompt
        output_format (str): The format of the image response (jpeg or png)
        response_format (str): Format of the image response (base64 or url)
        seed (int, optional): Seed used for generation
        n (int): Number of image results to generate
        save_path (str): Base path to save the generated images
        reference_image (str, optional): Path to a reference image (required for FLUX.1-depth model)
        
    Returns:
        bool: True if image generation was successful, False otherwise
    """
    # Ensure Images directory exists
    images_dir = "Images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Created directory: {images_dir}")
    print(f"\nGenerating image using {model}...")
    print(f"Prompt: '{prompt}'")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": model,
        "prompt": prompt,
        "height": height,
        "width": width,
        "steps": steps,
        "guidance": guidance,
        "output_format": output_format,
        "response_format": response_format,
        "n": n
    }
    
    # Add optional parameters if provided
    if negative_prompt:
        data["negative_prompt"] = negative_prompt
    if seed is not None:
        data["seed"] = seed
        
    # Add reference image for FLUX.1-depth model
    if "FLUX.1-depth" in model and reference_image:
        # Check if reference_image is a URL or a local file path
        if reference_image.startswith(('http://', 'https://')):
            data["image_url"] = {"url": reference_image}
        else:
            # For local files, we need to encode them as base64
            try:
                with open(reference_image, "rb") as img_file:
                    import base64
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                    data["image_url"] = {"url": f"data:image/jpeg;base64,{img_base64}"}
            except Exception as e:
                print(f"⚠️ Error reading reference image: {e}")
                return False
    
    try:
        response = requests.post(
            "https://api.together.xyz/v1/images/generations",
            headers=headers,
            json=data,
            timeout=60  # Image generation might take longer
        )
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Process and save the generated images
            for i, image_data in enumerate(response_data.get("data", [])):
                if response_format == "base64" and "b64_json" in image_data:
                    # Save base64 image to file
                    import base64 as b64  # Import locally to avoid namespace issues
                    img_data = b64.b64decode(image_data["b64_json"])
                    file_extension = output_format.lower()
                    file_name = f"{save_path}_{i+1}.{file_extension}" if n > 1 else f"{save_path}.{file_extension}"
                    file_path = os.path.join("Images", file_name)
                    
                    with open(file_path, "wb") as f:
                        f.write(img_data)
                    print(f"✅ Image {i+1} saved to {file_path}")
                elif response_format == "url" and "url" in image_data:
                    # Just display the URL
                    print(f"✅ Image {i+1} URL: {image_data['url']}")
            
            return True
        else:
            print(f"⚠️ Error generating image: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
                
                # Provide more helpful error messages
                if response.status_code == 400:
                    if "FLUX.1-depth" in model and "reference image is missing" in str(error_data):
                        print("\nThe FLUX.1-depth model requires a valid reference image.")
                        print("Please try again with a valid image URL or file path.")
                    elif "invalid_request_error" in str(error_data):
                        print("\nThere was an issue with your request parameters.")
                        print("Please check your prompt, dimensions, and other settings.")
                elif response.status_code == 500:
                    print("\nThe server encountered an internal error.")
                    print("This might be a temporary issue with the Together AI service.")
                    print("You can try again later or use a different model.")
                    
                    if "FLUX.1-depth" in model:
                        print("\nFor FLUX.1-depth model, try using a different reference image.")
                        print("The image should be a clear, well-lit photo with good resolution.")
            except:
                print(f"Response content: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"⚠️ Exception while generating image: {e}")
        return False

def run_image_generation_mode(api_key, model_name=None):
    """
    Run the image generation mode, allowing the user to generate images from text prompts.
    
    Args:
        api_key (str): The Together AI API key
        model_name (str, optional): Pre-selected model name from previous step
    """
    print("\n=== IMAGE GENERATION MODE ===")
    
    image_models = FAMOUS_MODELS["Image Models"]
    model_info = None
    
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
        print(f"Description: {model_info['description']}")
    else:
        # Find model info for the pre-selected model
        for model in image_models:
            if model["name"] == model_name:
                model_info = model
                break
        
        if not model_info:
            # If model_info is not found, use the first model as fallback
            model_info = image_models[0]
            model_name = model_info["name"]
            print(f"Using model: {model_name}")
            print(f"Description: {model_info['description']}")
    
    # Get prompt for image generation
    prompt = input("\nEnter prompt for image generation: ")
    if not prompt:
        prompt = "A beautiful landscape with mountains, a lake, and a sunset"
        print(f"Using default prompt: '{prompt}'")
    
    # Get negative prompt (optional)
    negative_prompt = input("Enter negative prompt (optional): ")
    
    # Get image dimensions
    try:
        width = int(input("Enter image width in pixels (default is 1024): ") or "1024")
        height = int(input("Enter image height in pixels (default is 1024): ") or "1024")
    except ValueError:
        print("Invalid dimensions. Using default 1024x1024.")
        width = 1024
        height = 1024
    
    # Get number of steps (limit to 1-12 for FLUX.1-schnell)
    try:
        if "FLUX.1-schnell" in model_name:
            print("Note: FLUX.1-schnell only supports 1-12 steps")
            steps_input = input("Enter number of generation steps (1-12, default is 10): ") or "10"
            steps = int(steps_input)
            steps = max(1, min(12, steps))  # Limit between 1 and 12
        else:
            steps_input = input("Enter number of generation steps (default is 20): ") or "20"
            steps = int(steps_input)
    except ValueError:
        if "FLUX.1-schnell" in model_name:
            print("Invalid steps. Using default 10.")
            steps = 10
        else:
            print("Invalid steps. Using default 20.")
            steps = 20
    
    # Get guidance value
    try:
        guidance = float(input("Enter guidance value (default is 3.5): ") or "3.5")
    except ValueError:
        print("Invalid guidance value. Using default 3.5.")
        guidance = 3.5
    
    # Get output format
    output_format = input("Enter output format (jpeg/png, default is jpeg): ").lower() or "jpeg"
    if output_format not in ["jpeg", "png"]:
        print("Invalid format. Using default jpeg.")
        output_format = "jpeg"
    
    # Get number of images
    try:
        n = int(input("Enter number of images to generate (1-4, default is 1): ") or "1")
        n = max(1, min(4, n))  # Limit between 1 and 4
    except ValueError:
        print("Invalid number. Generating 1 image.")
        n = 1
    
    # Get output filename
    output_file = input("Enter output filename (without extension, default is 'generated_image'): ") or "generated_image"
    
    # Handle reference image for FLUX.1-depth model
    reference_image = None
    if "FLUX.1-depth" in model_name:
        print("Note: FLUX.1-depth requires a reference image")
        print("The reference image should be a publicly accessible URL or a local file path.")
        print("For local files, make sure the path is correct and the file exists.")
        print("Example URL: https://example.com/image.jpg")
        print("Example local path: C:\\Users\\Username\\Pictures\\image.jpg")
        reference_image_path = input("Enter path to reference image or URL: ")
        if reference_image_path:
            reference_image = reference_image_path
            # If it's a local path, verify the file exists
            if not reference_image_path.startswith(('http://', 'https://')):
                if not os.path.exists(reference_image_path):
                    print(f"Warning: The file {reference_image_path} does not exist or cannot be accessed.")
                    retry = input("Do you want to try a different path? (y/n): ").lower()
                    if retry == 'y':
                        reference_image_path = input("Enter path to reference image or URL: ")
                        reference_image = reference_image_path
                    else:
                        print("Proceeding with the provided path, but generation may fail.")
        else:
            print("No reference image provided. The generation will fail for FLUX.1-depth model.")
            print("Would you like to use a different model instead? (y/n)")
            change_model = input().lower()
            if change_model == 'y':
                print("\nAvailable Image Models:")
                for i, model in enumerate(image_models, 1):
                    if "FLUX.1-depth" not in model["name"]:
                        print(f"{i}. {model['name']} - {model['description']}")
                
                model_choice = input(f"Choose a model (default is FLUX.1-schnell): ") or "2"
                try:
                    model_index = int(model_choice) - 1
                    if 0 <= model_index < len(image_models):
                        if "FLUX.1-depth" not in image_models[model_index]["name"]:
                            model_info = image_models[model_index]
                            model_name = model_info["name"]
                        else:
                            # Find the FLUX.1-schnell model
                            schnell_index = next((i for i, m in enumerate(image_models) if "FLUX.1-schnell" in m["name"]), 1)
                            model_info = image_models[schnell_index]
                            model_name = model_info["name"]
                    else:
                        # Find the FLUX.1-schnell model
                        schnell_index = next((i for i, m in enumerate(image_models) if "FLUX.1-schnell" in m["name"]), 1)
                        model_info = image_models[schnell_index]
                        model_name = model_info["name"]
                except ValueError:
                    # Find the FLUX.1-schnell model
                    schnell_index = next((i for i, m in enumerate(image_models) if "FLUX.1-schnell" in m["name"]), 1)
                    model_info = image_models[schnell_index]
                    model_name = model_info["name"]
                
                print(f"Selected model: {model_name}")
                print(f"Description: {model_info['description']}")
    
    # Generate the image
    success = generate_image(
        api_key=api_key,
        prompt=prompt,
        model=model_name,
        negative_prompt=negative_prompt if negative_prompt else None,
        height=height,
        width=width,
        steps=steps,
        guidance=guidance,
        output_format=output_format,
        n=n,
        save_path=output_file,
        reference_image=reference_image
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
        # Run image generation mode again
        return run_image_generation_mode(api_key)
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
