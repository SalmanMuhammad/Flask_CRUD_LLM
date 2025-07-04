import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiBotAPI:
    """
    A class to handle Gemini bot interactions with Google Gemini API.
    Provides CRUD operations for managing prompts and responses.
    """

    def __init__(self):
        """Initialize the Gemini Bot API with Gemini credentials."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Configure Gemini client
        genai.configure(api_key=self.api_key)
        self.model_name = "gemini-1.5-flash"
        self.model = genai.GenerativeModel(self.model_name)
        self.chat = self.model.start_chat(history=[])

        # In-memory storage for prompts and responses
        self.prompts: List[Dict] = []
        self.responses: List[Dict] = []

    def initialize_gemini(self, model: str = "gemini-1.5-flash") -> Dict:
        """
        Initialize the Gemini API with the required credentials and settings.

        Args:
            model (str): The Gemini model to use

        Returns:
            Dict: Status message indicating successful initialization
        """
        try:
            self.model_name = model
            self.model = genai.GenerativeModel(self.model_name)
            self.chat = self.model.start_chat(history=[])
            # Test the API connection
            test_response = self.model.generate_content("Hello from Gemini!")
            return {
                "status": "success",
                "message": f"Gemini initialized successfully with model: {self.model_name}",
                "test_response": test_response.text,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to initialize Gemini: {str(e)}",
            }

    def create_prompt(self, prompt: str) -> Dict:
        """
        Take a user-provided prompt as input and store it for later interactions.

        Args:
            prompt (str): The user's prompt text

        Returns:
            Dict: Information about the stored prompt including its index
        """
        if not prompt or not prompt.strip():
            return {"status": "error", "message": "Prompt cannot be empty"}
        prompt_data = {
            "id": len(self.prompts),
            "content": prompt.strip(),
            "created_at": self._get_timestamp(),
        }
        self.prompts.append(prompt_data)
        return {
            "status": "success",
            "message": "Prompt created successfully",
            "prompt_index": prompt_data["id"],
            "prompt": prompt_data,
        }

    def get_response(self, prompt_index: int) -> Dict:
        """
        Take the index of a previously stored prompt and return the Gemini bot's response.

        Args:
            prompt_index (int): Index of the stored prompt

        Returns:
            Dict: The Gemini response or error message
        """
        if prompt_index < 0 or prompt_index >= len(self.prompts):
            return {
                "status": "error",
                "message": f"Invalid prompt index: {prompt_index}. Available indices: 0-{len(self.prompts)-1}",
            }
        prompt_data = self.prompts[prompt_index]
        try:
            # Generate response using Gemini API
            response = self.model.generate_content(prompt_data["content"])
            response_text = response.text
            # Store the response
            response_data = {
                "id": len(self.responses),
                "prompt_index": prompt_index,
                "prompt": prompt_data["content"],
                "response": response_text,
                "created_at": self._get_timestamp(),
            }
            self.responses.append(response_data)
            return {
                "status": "success",
                "message": "Response generated successfully",
                "prompt_index": prompt_index,
                "prompt": prompt_data["content"],
                "response": response_text,
                "response_id": response_data["id"],
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to generate response: {str(e)}",
            }

    def update_prompt(self, prompt_index: int, new_prompt: str) -> Dict:
        """
        Update an existing prompt at the given index with a new prompt provided by the user.

        Args:
            prompt_index (int): Index of the prompt to update
            new_prompt (str): New prompt content

        Returns:
            Dict: Status message indicating success or failure
        """
        if prompt_index < 0 or prompt_index >= len(self.prompts):
            return {
                "status": "error",
                "message": f"Invalid prompt index: {prompt_index}. Available indices: 0-{len(self.prompts)-1}",
            }
        if not new_prompt or not new_prompt.strip():
            return {"status": "error", "message": "New prompt cannot be empty"}
        old_prompt = self.prompts[prompt_index]["content"]
        self.prompts[prompt_index]["content"] = new_prompt.strip()
        self.prompts[prompt_index]["updated_at"] = self._get_timestamp()
        return {
            "status": "success",
            "message": "Prompt updated successfully",
            "prompt_index": prompt_index,
            "old_prompt": old_prompt,
            "new_prompt": new_prompt.strip(),
        }

    def delete_prompt(self, prompt_index: int) -> Dict:
        """
        Delete a prompt at the given index.

        Args:
            prompt_index (int): Index of the prompt to delete

        Returns:
            Dict: Status message indicating success or failure
        """
        if prompt_index < 0 or prompt_index >= len(self.prompts):
            return {
                "status": "error",
                "message": f"Invalid prompt index: {prompt_index}. Available indices: 0-{len(self.prompts)-1}",
            }
        deleted_prompt = self.prompts.pop(prompt_index)
        for i in range(prompt_index, len(self.prompts)):
            self.prompts[i]["id"] = i
        return {
            "status": "success",
            "message": "Prompt deleted successfully",
            "deleted_prompt": deleted_prompt,
        }

    def get_all_prompts(self) -> Dict:
        """
        Get all stored prompts.

        Returns:
            Dict: List of all prompts
        """
        return {
            "status": "success",
            "prompts": self.prompts,
            "count": len(self.prompts),
        }

    def get_all_responses(self) -> Dict:
        """
        Get all stored responses.

        Returns:
            Dict: List of all responses
        """
        return {
            "status": "success",
            "responses": self.responses,
            "count": len(self.responses),
        }

    def _get_timestamp(self) -> str:
        """Helper method to get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()
