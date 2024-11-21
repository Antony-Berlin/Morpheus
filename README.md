# Morpheus

## Setup Instructions

Follow these steps to set up the application locally:

1. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Get the API key from OpenRouter:**
    - Visit the [OpenRouter website](https://openrouter.ai/meta-llama/llama-3.2-3b-instruct:free) and generate an API key for LLaMA 3.2 3B Instruct.

4. **Create a `.env` file inside the app folder and add the API key:**
    - Add the following line to the `.env` file:
      ```
      OPEN_ROUTER_API_KEY=your_api_key_here
      ```

5. **Start the Gunicorn server:**
    ```bash
    gunicorn --reload wsgi:app
    ```