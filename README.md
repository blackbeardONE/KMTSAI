# 🤖 (KMTS) Kikipatsu, Maki, Tori and Stronger AI – Multi-Agent System (LangChain + OpenAI + Together AI)

This project demonstrates a modular **multi-agent AI system** built using [LangChain](https://www.langchain.com/), OpenAI's GPT models, and Together AI. It showcases how agents can collaborate toward a shared goal by simulating the behavior of a Planner, a Coder, and a Critic — just like a real-world development team.

---

## 🛠 Tech Stack

- Python 3.9+
- [LangChain](https://docs.langchain.com)
- [OpenAI GPT-3.5 Turbo](https://platform.openai.com)
- [Together AI](https://together.ai) for image and audio generation
- Callback tracking via `get_openai_callback`

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install langchain langchain_openai langchain_together requests tabulate
```

### 2. Set Your API Keys

```bash
export OPENAI_API_KEY="your-openai-key-here"
export TOGETHER_API_KEY="your-together-key-here"
```

### 3. Run the Program

```bash
python main.py
```

---

## 🌟 Features

- **Multi-Agent System**: Collaborative AI agents working together
- **Multi-Mode Operation**: Supports Test LLM Provider and Talk to AI modes
- **Multi-Provider Support**: Choose between OpenAI, Together AI (native API), Together AI (OpenAI-compatible API), and Famous & Preferred Models
- **Model Selection & Filtering**: Filter models by free/paid status and categories (Chat, Audio, Image)
- **Audio Generation**: Generate audio with selectable voices using Sonic models
- **Image Generation**: Generate images with configurable models and parameters (steps, width, height)
- **Token Usage Tracking**: Monitor token usage for OpenAI models via callback tracking
- **Robust User Interaction**: Interactive menus with options to retry, return to previous or main menus, and exit gracefully
- **Error Handling**: Handles API key verification and initialization errors with user prompts

---

## 📝 Documentation

The system supports three main modes:
1. **General Chat/Instructions**: Interact with AI models for text generation
2. **Audio Generation**: Create audio files from text input with voice selection
3. **Image Generation**: Generate images from text prompts with model and parameter selection

### Image Generation Models
- FLUX.1.1 Pro - High quality image generation
- FLUX.1 Schnell - Fast image generation model
- FLUX.1 Depth - Image generation with depth perception (requires reference image)

### Audio Generation Models
- Sonic - High-quality text-to-speech model
- Sonic 2 - Improved text-to-speech with enhanced naturalness

---

## 🆕 Latest Changes

- Added multi-mode operation with Test LLM Provider and Talk to AI modes
- Integrated multiple LLM providers including Together AI native and OpenAI-compatible APIs
- Enhanced model selection with filtering options for free and paid models
- Added voice selection for audio generation
- Improved image generation with configurable parameters and model choices
- Implemented token usage tracking for OpenAI API calls
- Improved user interaction flow with menu navigation and error handling

---

## 👨‍💻 Developer

Developed by [Blackbeard](https://blackbeard.one) | [Ten Titanics](https://tentitanics.com) | [GitHub](https://github.com/blackbeardONE)

© 2023-2024 Blackbeard. All rights reserved.
