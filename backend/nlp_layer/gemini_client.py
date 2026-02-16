"""
Gemini API Client

This module handles communication with Google's Gemini AI.
Translator between our code and the AI.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()


class GeminiClient:
    """
    A client for interacting with Google Gemini API.

    This class handles:
    - API authentication
    - Sending prompts to Gemini
    - Receiving responses

    Example usage:
        client = GeminiClient()
        response = client.generate("What is 2+2?")
        print(response)  # "4"

    """

    def __init__(self, api_key: str = None):
        # Get API key from argument or environment variable
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        # Check if we have a key
        if not self.api_key:
            raise ValueError(
                "No API key provided! Either pass it to __init__ "
                "or set the GEMINI_API_KEY environment variable."
            )

        # config the gemini library with our key
        genai.configure(api_key=self.api_key)

        # create a model instance
        # "gemini-2.0-flash" is the current text model
        self.model = genai.GenerativeModel("gemini-2.5-flash")

        print("Gemini client initialized successfully!")

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and get a response.

        Args:
            prompt: The text prompt to send to the AI

        Returns:
            The AI's response as a string

        """

        try:
            # send prompt to Gemini
            response = self.model.generate_content(prompt)

            # return the text response
            return response.text

        except Exception as e:
            # If something goes wrong (error)
            print(f"Error calling Gemini API: {e}")
            raise


if __name__ == "__main__":
    # This code only runs when you execute this file directly
    # python backend/nlp_layer/gemini_client.py

    print("Testing Gemini Client...")
    print("-" * 40)

    # Create a client
    client = GeminiClient()

    # Test with a simple prompt
    test_prompt = "What is 2 + 2? Answer with just the number."
    print(f"Prompt: {test_prompt}")

    response = client.generate(test_prompt)
    print(f"Response: {response}")

    print("-" * 40)
    print("Test complete!")
