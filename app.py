from flask import Flask
from flask_restx import Api, Resource, Namespace, fields
from flask_cors import CORS
from chatbot_api import GeminiBotAPI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Flask-RESTX API
api = Api(
    app,
    version="1.0",
    title="Gemini Bot CRUD API",
    description="A Flask-based REST API that provides CRUD operations for managing Gemini bot interactions",
    doc="/docs",
    default="api",
    default_label="Gemini Bot API Endpoints",
)

# Create namespaces
api_ns = Namespace("api", description="Gemini Bot API operations")
api.add_namespace(api_ns)

# Define API models for request/response schemas
prompt_model = api.model(
    "Prompt",
    {
        "prompt": fields.String(required=True, description="The prompt text"),
    },
)

new_prompt_model = api.model(
    "NewPrompt",
    {
        "new_prompt": fields.String(required=True, description="The new prompt text"),
    },
)

initialize_model = api.model(
    "Initialize",
    {
        "model": fields.String(
            default="gemini-1.5-flash", description="Gemini model to use"
        ),
    },
)

prompt_response_model = api.model(
    "PromptResponse",
    {
        "status": fields.String(description="Response status"),
        "message": fields.String(description="Response message"),
        "prompt_index": fields.Integer(description="Index of the created prompt"),
        "prompt": fields.Raw(description="Prompt data"),
    },
)

response_model = api.model(
    "Response",
    {
        "status": fields.String(description="Response status"),
        "message": fields.String(description="Response message"),
        "prompt_index": fields.Integer(description="Index of the prompt"),
        "prompt": fields.String(description="Original prompt"),
        "response": fields.String(description="Gemini response"),
        "response_id": fields.Integer(description="Response ID"),
    },
)

prompts_list_model = api.model(
    "PromptsList",
    {
        "status": fields.String(description="Response status"),
        "prompts": fields.List(fields.Raw, description="List of prompts"),
        "count": fields.Integer(description="Number of prompts"),
    },
)

error_model = api.model(
    "Error",
    {
        "status": fields.String(description="Error status"),
        "message": fields.String(description="Error message"),
    },
)

# Initialize the Gemini Bot API as None - will be initialized via API call
chatbot_api = None


@api_ns.route("/initialize")
class InitializeAPI(Resource):
    @api_ns.expect(initialize_model)
    @api_ns.response(200, "Success", response_model)
    @api_ns.response(400, "Bad Request", error_model)
    @api_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Initialize Gemini with custom settings"""
        global chatbot_api
        try:
            data = api.payload or {}
            model = data.get("model", "gemini-1.5-flash")

            # Initialize the Gemini Bot API
            chatbot_api = GeminiBotAPI()
            result = chatbot_api.initialize_gemini(model)

            if result["status"] == "success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to initialize Gemini: {str(e)}",
            }, 500


@api_ns.route("/prompts")
class PromptsAPI(Resource):
    @api_ns.expect(prompt_model)
    @api_ns.response(201, "Created", prompt_response_model)
    @api_ns.response(400, "Bad Request", error_model)
    @api_ns.response(500, "Internal Server Error", error_model)
    def post(self):
        """Create a new prompt"""
        if not chatbot_api:
            return {
                "status": "error",
                "message": "Gemini Bot API not available. Please initialize first using /api/initialize endpoint.",
            }, 500

        try:
            data = api.payload
            if not data or "prompt" not in data:
                return {"status": "error", "message": "Prompt field is required"}, 400

            result = chatbot_api.create_prompt(data["prompt"])
            if result["status"] == "success":
                return result, 201
            else:
                return result, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create prompt: {str(e)}",
            }, 500

    @api_ns.response(200, "Success", prompts_list_model)
    @api_ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """Get all stored prompts"""
        if not chatbot_api:
            return {
                "status": "error",
                "message": "Gemini Bot API not available. Please initialize first using /api/initialize endpoint.",
            }, 500

        try:
            result = chatbot_api.get_all_prompts()
            return result, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get prompts: {str(e)}",
            }, 500


@api_ns.route("/prompts/<int:prompt_index>")
@api_ns.param("prompt_index", "The prompt index")
class PromptAPI(Resource):
    @api_ns.response(200, "Success", prompt_response_model)
    @api_ns.response(404, "Not Found", error_model)
    @api_ns.response(500, "Internal Server Error", error_model)
    def get(self, prompt_index):
        """Get a specific prompt by index"""
        if not chatbot_api:
            return {
                "status": "error",
                "message": "Gemini Bot API not available. Please initialize first using /api/initialize endpoint.",
            }, 500

        try:
            result = chatbot_api.get_all_prompts()
            if result["status"] == "success":
                if prompt_index < len(result["prompts"]):
                    return {
                        "status": "success",
                        "prompt": result["prompts"][prompt_index],
                    }, 200
                else:
                    return {
                        "status": "error",
                        "message": f"Prompt index {prompt_index} not found",
                    }, 404
            else:
                return result, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get prompt: {str(e)}",
            }, 500

    @api_ns.expect(new_prompt_model)
    @api_ns.response(200, "Success", prompt_response_model)
    @api_ns.response(400, "Bad Request", error_model)
    @api_ns.response(500, "Internal Server Error", error_model)
    def put(self, prompt_index):
        """Update a prompt at the given index"""
        if not chatbot_api:
            return {
                "status": "error",
                "message": "Gemini Bot API not available. Please initialize first using /api/initialize endpoint.",
            }, 500

        try:
            data = api.payload
            if not data or "new_prompt" not in data:
                return {
                    "status": "error",
                    "message": "new_prompt field is required",
                }, 400

            result = chatbot_api.update_prompt(prompt_index, data["new_prompt"])
            if result["status"] == "success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update prompt: {str(e)}",
            }, 500

    @api_ns.response(200, "Success", prompt_response_model)
    @api_ns.response(500, "Internal Server Error", error_model)
    def delete(self, prompt_index):
        """Delete a prompt at the given index"""
        if not chatbot_api:
            return {
                "status": "error",
                "message": "Gemini Bot API not available. Please initialize first using /api/initialize endpoint.",
            }, 500

        try:
            result = chatbot_api.delete_prompt(prompt_index)
            if result["status"] == "success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete prompt: {str(e)}",
            }, 500


@api_ns.route("/prompts/<int:prompt_index>/response")
@api_ns.param("prompt_index", "The prompt index")
class ResponseAPI(Resource):
    @api_ns.response(200, "Success", response_model)
    @api_ns.response(400, "Bad Request", error_model)
    @api_ns.response(500, "Internal Server Error", error_model)
    def post(self, prompt_index):
        """Get Gemini response for a prompt at the given index"""
        if not chatbot_api:
            return {
                "status": "error",
                "message": "Gemini Bot API not available. Please initialize first using /api/initialize endpoint.",
            }, 500

        try:
            result = chatbot_api.get_response(prompt_index)
            if result["status"] == "success":
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to get response: {str(e)}",
            }, 500


if __name__ == "__main__":
    # Check if Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable is not set!")
        print(
            "Please set your Gemini API key in the .env file or as an environment variable."
        )
        print(
            "You can still test the API structure, but LLM functionality will not work."
        )
    elif not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set!")
        print(
            "Please set your OpenAI API key in the .env file or as an environment variable."
        )
        print(
            "You can still test the API structure, but LLM functionality will not work."
        )

    app.run(debug=True, host="0.0.0.0", port=5500)
