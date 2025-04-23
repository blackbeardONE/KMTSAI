"""
Agent system module.

This module provides functions for the multi-agent system implementation,
including planner, coder, and critic agents.
"""

import sys
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def planner_agent(llm, task):
    """
    Planner agent that breaks down coding tasks into implementation steps.
    
    Args:
        llm: The language model to use
        task (str): The task to plan
        
    Returns:
        str: The implementation plan
    """
    try:
        # Check if we're using the OpenAI completions API or ChatOpenAI
        if hasattr(llm, 'invoke'):
            # Using ChatOpenAI or Together
            messages = [
                SystemMessage(content="""You are a senior software architect. Your job is to break down coding tasks into implementation steps.
                Be specific and detailed in your breakdown. Focus only on the task provided and do not deviate from it."""),
                HumanMessage(content=f"Task: {task}")
            ]
            response = llm.invoke(messages)
            # Handle different return types
            return response.content if hasattr(response, 'content') else response
        else:
            # Using OpenAI completions API
            prompt = f"""You are a senior software architect. Your job is to break down coding tasks into implementation steps.
            Be specific and detailed in your breakdown. Focus only on the task provided and do not deviate from it.
            
            Task: {task}
            
            Implementation steps:"""
            
            response = llm(prompt)
            return response
    except Exception as e:
        print(f"\n⚠️ ERROR in planner_agent: {e}")
        sys.exit(1)

def coder_agent(llm, instruction):
    """
    Coder agent that writes code based on instructions.
    
    Args:
        llm: The language model to use
        instruction (str): The instruction to follow
        
    Returns:
        str: The generated code
    """
    try:
        # Check if we're using the OpenAI completions API or ChatOpenAI
        if hasattr(llm, 'invoke'):
            # Using ChatOpenAI or Together
            messages = [
                SystemMessage(content="""You are an expert Python developer. Write clean and readable Python code based on the instructions.
                Implement exactly what is requested, with appropriate comments and error handling. Do not deviate from the task."""),
                HumanMessage(content=f"Based on these instructions, write Python code to solve the problem:\n{instruction}")
            ]
            response = llm.invoke(messages)
            # Handle different return types
            return response.content if hasattr(response, 'content') else response
        else:
            # Using OpenAI completions API
            prompt = f"""You are an expert Python developer. Write clean and readable Python code based on the instructions.
            Implement exactly what is requested, with appropriate comments and error handling. Do not deviate from the task.
            
            Based on these instructions, write Python code to solve the problem:
            {instruction}
            
            ```python
            """
            
            response = llm(prompt)
            # Extract code from response if needed
            if "```python" in response and "```" in response.split("```python", 1)[1]:
                code_block = response.split("```python", 1)[1].split("```", 1)[0]
                return code_block.strip()
            return response
    except Exception as e:
        print(f"\n⚠️ ERROR in coder_agent: {e}")
        sys.exit(1)

def critic_agent(llm, code):
    """
    Critic agent that reviews code for correctness and suggests improvements.
    
    Args:
        llm: The language model to use
        code (str): The code to review
        
    Returns:
        str: The review
    """
    try:
        # Check if we're using the OpenAI completions API or ChatOpenAI
        if hasattr(llm, 'invoke'):
            # Using ChatOpenAI or Together
            messages = [
                SystemMessage(content="""You are a code reviewer. Review the following Python function for correctness and suggest improvements.
                Focus specifically on the code provided and ensure it correctly implements the intended functionality of checking if a number is prime.
                Check for edge cases (like negative numbers, 0, 1, 2), efficiency, and readability.
                The function should be named 'is_prime' and should return True if the number is prime, False otherwise."""),
                HumanMessage(content=f"Review this Python function that is supposed to check if a number is prime. The function should be named 'is_prime':\n{code}")
            ]
            response = llm.invoke(messages)
            # Handle different return types
            return response.content if hasattr(response, 'content') else response
        else:
            # Using OpenAI completions API
            prompt = f"""You are a code reviewer. Review the following Python function for correctness and suggest improvements.
            Focus specifically on the code provided and ensure it correctly implements the intended functionality of checking if a number is prime.
            Check for edge cases (like negative numbers, 0, 1, 2), efficiency, and readability.
            The function should be named 'is_prime' and should return True if the number is prime, False otherwise.
            
            Review this Python function that is supposed to check if a number is prime. The function should be named 'is_prime':
            
            {code}
            
            Review:"""
            
            response = llm(prompt)
            return response
    except Exception as e:
        print(f"\n⚠️ ERROR in critic_agent: {e}")
        sys.exit(1)

def run_multi_agent_system(llm, user_request):
    """
    Run the multi-agent system to process a user request.
    
    Args:
        llm: The language model to use
        user_request (str): The user's request
    """
    try:
        print("📌 User Request:", user_request)
        
        print("\n🔧 Step 1: Planning the task...")
        plan = planner_agent(llm, user_request)
        print(plan)

        print("\n💻 Step 2: Generating code...")
        code = coder_agent(llm, plan)
        print(code)

        print("\n🧐 Step 3: Reviewing code...")
        review = critic_agent(llm, code)
        print(review)
    except Exception as e:
        print(f"\n⚠️ ERROR in run_multi_agent_system: {e}")
        sys.exit(1)

def talk_to_ai(llm):
    """
    Interactive chat with the AI model.
    
    Args:
        llm: The language model to use
    """
    try:
        print("\n=== TALK TO AI MODE ===")
        print("You can have a conversation with the AI. Type 'exit' to end the conversation.")
        
        # Get system instruction from user
        system_instruction = input("\nEnter system instruction (or press Enter for default): ")
        if not system_instruction:
            system_instruction = "You are a helpful AI assistant. Provide clear, concise, and accurate responses to the user's questions."
        
        # Set up the conversation with system message
        system_message = SystemMessage(content=system_instruction)
        
        # Start the conversation loop
        while True:
            # Get user input
            user_input = input("\nYou: ")
            
            # Check if user wants to exit
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nExiting conversation mode.")
                break
            
            # Create a new conversation for each exchange to avoid the "messages can have at most one message" error
            conversation = [
                system_message,
                HumanMessage(content=user_input)
            ]
            
            try:
                # Get AI response
                if hasattr(llm, 'invoke'):
                    # Using ChatOpenAI or Together
                    response = llm.invoke(conversation)
                    ai_response = response.content if hasattr(response, 'content') else response
                else:
                    # Using OpenAI completions API
                    prompt = f"{system_instruction}\n\nUser: {user_input}\n\nAI:"
                    ai_response = llm(prompt)
                
                # Print AI response
                print(f"\nAI: {ai_response}")
                
            except Exception as e:
                print(f"\n⚠️ ERROR: {e}")
                print("Let's continue the conversation.")
                
    except Exception as e:
        print(f"\n⚠️ ERROR in talk_to_ai: {e}")
        sys.exit(1)
