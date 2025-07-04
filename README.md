# Gemini Bot CRUD API

A Flask-based REST API that provides CRUD (Create, Read, Update, Delete) operations for managing Gemini bot interactions with the Google Gemini API. Built with Flask-RESTX for automatic Swagger UI documentation.

## Features

- **CRUD Operations**: Full Create, Read, Update, Delete functionality for prompts
- **Google Gemini Integration**: Seamless integration with Gemini (via google-generativeai)
- **Response Management**: Store and retrieve Gemini responses
- **RESTful API**: Clean, intuitive REST endpoints
- **Automatic Documentation**: Swagger UI automatically generated from Flask-RESTX
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Cross-origin resource sharing enabled

## Prerequisites

- Python 3.7 or higher
- Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/app/apikey))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SalmanMuhammad/Flask_CRUD_LLM
   cd flask-crud-llm
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file and add your Gemini API key
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```

## Usage

### Starting the Server

```bash
python app.py
```

The server will start on `http://localhost:5500`

### API Documentation

**Swagger UI**: Visit `http://localhost:5500/docs` for interactive API documentation

### API Endpoints

All endpoints are prefixed with `/api/`:

#### 1. Initialize Gemini
```http
POST /api/initialize
Content-Type: application/json

{
    "model": "gemini-1.5-flash"
}
```

#### 2. Create a Prompt
```http
POST /api/prompts
Content-Type: application/json

{
    "prompt": "What is the capital of France?"
}
```

#### 3. Get All Prompts
```http
GET /api/prompts
```

#### 4. Get Specific Prompt
```http
GET /api/prompts/{prompt_index}
```

#### 5. Update a Prompt
```http
PUT /api/prompts/{prompt_index}
Content-Type: application/json

{
    "new_prompt": "What is the capital of Germany?"
}
```

#### 6. Delete a Prompt
```http
DELETE /api/prompts/{prompt_index}
```

#### 7. Get Gemini Response
```http
POST /api/prompts/{prompt_index}/response
```


## Example Usage

### Using curl

1. **Initialize Gemini**:
   ```bash
   curl -X POST http://localhost:5500/api/initialize \
     -H "Content-Type: application/json" \
     -d '{"model": "gemini-1.5-flash"}'
   ```

2. **Create a prompt**:
   ```bash
   curl -X POST http://localhost:5500/api/prompts \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Explain quantum computing in simple terms"}'
   ```

3. **Get response for the prompt**:
   ```bash
   curl -X POST http://localhost:5500/api/prompts/0/response
   ```

4. **Update the prompt**:
   ```bash
   curl -X PUT http://localhost:5500/api/prompts/0 \
     -H "Content-Type: application/json" \
     -d '{"new_prompt": "Explain artificial intelligence in simple terms"}'
   ```

5. **Get all prompts**:
   ```bash
   curl http://localhost:5500/api/prompts
   ```

### Using Python requests

```python
import requests

# Base URL
base_url = "http://localhost:5500/api"

# Initialize Gemini
response = requests.post(f"{base_url}/initialize", 
                        json={"model": "gemini-1.5-flash"})
print(response.json())

# Create a prompt
response = requests.post(f"{base_url}/prompts", 
                        json={"prompt": "What is machine learning?"})
print(response.json())

# Get response for the prompt
response = requests.post(f"{base_url}/prompts/0/response")
print(response.json())

# Update the prompt
response = requests.put(f"{base_url}/prompts/0", 
                       json={"new_prompt": "What is deep learning?"})
print(response.json())
```

## Project Structure

```
flask-crud-llm/
├── app.py              # Main Flask-RESTX application
├── chatbot_api.py      # GeminiBotAPI class implementation
├── requirements.txt    # Python dependencies
├── test_api.py         # Test script for API endpoints
├── README.md           # This file
└── requirement.doc     # Original requirements
```

## GeminiBotAPI Class

The `GeminiBotAPI` class provides the core functionality:

### Methods

- `initialize_gemini()`: Initialize Gemini API with credentials and settings
- `create_prompt(prompt)`: Store a user prompt for later use
- `get_response(prompt_index)`: Get Gemini response for a stored prompt
- `update_prompt(prompt_index, new_prompt)`: Update an existing prompt
- `delete_prompt(prompt_index)`: Delete a prompt
- `get_all_prompts()`: Retrieve all stored prompts

### Data Storage

The application uses in-memory storage for simplicity. In a production environment, you might want to use a database like PostgreSQL or MongoDB.

## Flask-RESTX Features

- **Automatic Swagger UI**: Visit `/docs` for interactive API documentation
- **Request/Response Models**: Defined schemas for all API operations
- **Namespace Organization**: Clean API structure with `/api/` prefix
- **Parameter Validation**: Automatic validation of request parameters
- **Response Documentation**: Clear documentation of all response formats

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors

All error responses include a descriptive message and status.

## Configuration

You can customize the Gemini settings by modifying the initialization parameters:

- `model`: Gemini model to use (default: "gemini-1.5-flash")

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

To test the API without a Gemini API key, the application will start but LLM functionality will be disabled. You can still test the CRUD operations for prompts.

## API Documentation

The Swagger UI provides:
- Interactive API testing
- Request/response schemas
- Parameter descriptions
- Example requests
- Response codes

Visit `http://localhost:5500/docs` after starting the server.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on the repository. 
