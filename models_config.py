"""
Models configuration module.

This module contains the definitions and configurations for various AI models
used in the application, including language models, code models, image models,
and audio models.
"""

# Curated list of models organized by working status
FAMOUS_MODELS = {
    "Chat Models": [
        {"name": "meta-llama/Llama-3-70b-chat-hf", "description": "Meta's Llama 3 70B - Powerful open-source model with strong reasoning", "is_free": True, "status": "working"},
        {"name": "mistralai/Mixtral-8x7B-Instruct-v0.1", "description": "Mistral's Mixtral - Mixture of experts architecture with strong performance", "is_free": True, "status": "working"},
        {"name": "deepseek-ai/DeepSeek-V3", "description": "DeepSeek V3 - Advanced model with strong reasoning capabilities", "is_free": True, "status": "working"},
        {"name": "deepseek-ai/DeepSeek-R1", "description": "DeepSeek R1 - Knowledge-focused model with enhanced reasoning", "is_free": True, "status": "working"},
        {"name": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", "description": "Llama 4 Maverick - Specialized 17B model with 128 experts", "is_free": True, "status": "working"},
        {"name": "meta-llama/Llama-3.3-70B-Instruct-Turbo", "description": "Meta's Llama 3.3 70B - Latest version with improved instruction following (Buggy)", "is_free": True, "status": "needs_rework"},
        {"name": "meta-llama/Llama-4-Scout-17B-16E-Instruct", "description": "Llama 4 Scout - Specialized 17B model with 16 experts (Buggy)", "is_free": True, "status": "needs_rework"}
    ],
    "Image Models": [
        {"name": "black-forest-labs/FLUX.1.1-pro", "description": "FLUX.1.1 Pro - High quality image generation", "is_free": True, "status": "working"},
        {"name": "black-forest-labs/FLUX.1-schnell", "description": "FLUX.1 Schnell - Fast image generation model (Note: only allows 1-12 steps for parameters)", "is_free": True, "status": "needs_refactor"},
        {"name": "black-forest-labs/FLUX.1-depth", "description": "FLUX.1 Depth - Image generation with depth perception", "is_free": True, "status": "needs_rework"}
    ],
    "Audio Models": [
        {"name": "cartesia/sonic", "description": "Sonic - High-quality text-to-speech model", "is_free": True, "status": "working"},
        {"name": "cartesia/sonic-2", "description": "Sonic 2 - Improved text-to-speech with enhanced naturalness", "is_free": True, "status": "working"}
    ]
}

# Available voices for audio generation
AVAILABLE_VOICES = [
    "laidback woman",
    "polite man",
    "storyteller lady",
    "friendly sidekick"
]
