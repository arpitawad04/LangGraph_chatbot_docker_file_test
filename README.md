# LangGraph Chatbot with Docker

A simple and interactive chatbot app built with LangGraph, Streamlit, and OpenAI. This project is containerized with Docker so it can be run consistently across machines.

## Features

- Chat interface built with Streamlit
- LangGraph-based workflow for message processing
- Docker support for easy deployment
- Environment-based configuration for API keys
- Simple project structure suitable for learning and demos

## Project Structure

```text
.
├── Dockerfile
├── Langraphstreamlit.py
├── requirements.txt
├── streamlit.py
├── .env
└── README.md
```

## Prerequisites

Before running this project, make sure you have:

- Python 3.12+
- Docker Desktop installed and running
- An OpenAI API key

## Setup

1. Clone the repository:

```bash
git clone https://github.com/arpitawad04/LangGraph_chatbot_docker_file_test.git
cd LangGraph_chatbot_docker_file_test
```

2. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

3. Install dependencies locally (optional):

```bash
pip install -r requirements.txt
```

4. Run the app locally:

```bash
streamlit run streamlit.py
```

## Docker Usage

Build the Docker image:

```bash
docker build -t my-langgraph-chatbot .
```

Run the container:

```bash
docker run -p 8501:8501 --env-file .env my-langgraph-chatbot
```

Then open your browser at:

```text
http://localhost:8501
```

## Environment Variables

The app uses the following environment variable:

- `OPENAI_API_KEY` : Your OpenAI API key used by the chatbot

## Notes

- Do not commit your real API keys to GitHub.
- Keep your `.env` file local and add it to `.gitignore`.
- If you face authentication issues, check that your API key is valid and has the required permissions.

## Troubleshooting

### Docker build fails

Make sure Docker Desktop is running and your system can access the Docker daemon.

### API key error

If you see an authentication error, verify that:

- the key is valid
- the key is stored correctly in `.env`
- the key is not enclosed in quotes if you are using `python-dotenv`

## License

This project is for educational and demonstration purposes.
