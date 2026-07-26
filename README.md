# Multi-Tool Agent(Weather & Currency Conversion Agent)

An AI agent built with **LangChain** and **FastAPI** that answers natural language queries about weather forecasts and currency conversion. The agent uses tool-calling to decide when and how to fetch live weather data or currency exchange rates, chaining multiple tool calls together when a query requires it (e.g. "What's the weather in Lahore and convert 100 USD to PKR?").

---

## Features

- **Conversational agent** powered by an LLM (via OpenRouter) with native tool-calling support
- **Weather tool** — fetches multi-day forecasts (temperature, humidity, wind speed, rain chance, conditions) for any city
- **Currency conversion tools** — a two-step tool chain: fetches a live exchange rate, then converts a given amount using that rate
- **Sequential/dependent tool orchestration** — the agent correctly chains tool calls where one tool's output feeds into the next (e.g. get conversion rate → then convert amount)
- **Production-style structure** — centralized config, custom exceptions, structured logging
- **REST API** built with FastAPI, with auto-generated Swagger docs
- **Unit tested** with `pytest`, using mocked API responses (no live API calls during testing)
- **Dockerized** for consistent local and cloud deployment

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangChain (`create_agent`) |
| LLM provider | OpenRouter (`langchain-openrouter`) |
| API framework | FastAPI + Uvicorn |
| Weather data | OpenWeatherMap API |
| Currency data | ExchangeRate-API |
| Testing | Pytest + `unittest.mock` |
| Containerization | Docker |
| Deployment target | AWS |

---

## Architecture

The agent follows a standard tool-calling loop:

1. User sends a natural language query to `POST /chat`
2. The agent (LLM) decides which tool(s) it needs and generates a tool call
3. The corresponding tool executes (e.g. calls the OpenWeatherMap or ExchangeRate-API)
4. The tool's result is fed back to the LLM
5. The LLM either calls another tool (if the query needs more data, e.g. currency conversion requires a rate lookup *before* a conversion) or returns a final natural language answer
6. Steps 2-5 repeat until no more tool calls are needed

### Available Tools

| Tool | Purpose | Input | Output |
|---|---|---|---|
| `search_weather` | Get weather forecast for a city | `city_name`, `days` | Cleaned forecast data (temp, condition, humidity, wind, rain chance per time slot) |
| `rate_conversion` | Get live exchange rate between two currencies | `base_currency`, `target_currency` | Conversion rate |
| `currency_converter` | Convert an amount using a given rate | `base_currency` (amount), `conversion_rate` | Converted amount |

---

## Project Structure

```
weather_currency_agent/
├── app/
│   ├── main.py                     # FastAPI app entry point
│   ├── configs/
│   │   └── keys_config.py          # Centralized env var / settings loading
│   ├── logger/
│   │   └── custom_logger.py        # Reusable logger setup (console + file handlers)
│   ├── exception/
│   │   └── custome_exceptions.py   # Custom exception classes (WeatherAPIError, CurrencyAPIError, etc.)
│   ├── tools/
│   │   ├── search_weather.py       # Weather tool + data cleaning
│   │   └── currency_tool.py        # Rate lookup + conversion tools
│   ├── agents/
│   │   ├── models.py               # LLM model initialization (ChatOpenRouter)
│   │   └── agent_setup.py          # create_agent() setup with tools + system prompt
│   └── api/
│       ├── schemas.py              # Pydantic request/response models
│       └── routes/
│           └── chat_route.py       # POST /chat endpoint
├── tests/
│   └── test_tools.py               # Unit tests with mocked API responses
├── .env                             # Environment variables (not committed)
├── .env.example                     # Template for required environment variables
├── .dockerignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- API keys for:
  - [OpenRouter](https://openrouter.ai/) (LLM access)
  - [OpenWeatherMap](https://openweathermap.org/) (weather data)
  - [ExchangeRate-API](https://www.exchangerate-api.com/) (currency rates)

### 1. Clone the repository

```bash
git clone https://github.com/Muhammad-Wasil-Ali/weather-currency-agent.git
cd weather-currency-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your actual keys:

```bash
cp .env.example .env
```

```env
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=your_chosen_model_slug
WEATHER_API_KEY=your_openweathermap_key
EXCHANGERATE_API_KEY=your_exchangerate_api_key
```

> **Note:** Do not wrap values in quotes in the `.env` file — this can cause authentication errors when running inside Docker.

### 5. Run locally

```bash
uvicorn app.main:app --reload
```

Visit:
- `http://localhost:8000/` — health check
- `http://localhost:8000/docs` — interactive Swagger API docs

---

## API Usage

### `POST /chat`

**Request:**
```json
{
  "message": "What's the weather in Attock for 2 days and convert 10 USD to PKR?"
}
```

**Response:**
```json
{
  "reply": "Attock will see temperatures between 25°C and 34°C over the next 2 days, with rain likely in the mornings. Also, 10 USD converts to approximately 2,776.82 PKR.",
  "tool_calls_made": ["search_weather", "rate_conversion", "currency_converter"]
}
```

---

## Running Tests

Tests use mocked API responses, so no real API calls or internet connection is required.

```bash
pytest tests/ -v
```

---

## Running with Docker

### Build the image

```bash
docker build -t weather-currency-agent .
```

### Run the container

```bash
docker run -p 8000:8000 --env-file .env weather-currency-agent
```

Visit `http://localhost:8000/docs` to confirm it's running.

---

## Deployment

This project is designed to be deployed as a containerized service on AWS (ECS/EC2). Deployment steps and infrastructure setup are documented separately as this part of the project evolves.

---

## Key Design Decisions

- **Two-step currency conversion** (`rate_conversion` + `currency_converter` as separate tools) instead of one combined tool — this lets the LLM correctly reason through dependent, sequential tool calls rather than hardcoding the chain in Python, which is closer to how real-world agentic systems are built.
- **Custom exceptions instead of returning error strings** — keeps error handling explicit and lets the FastAPI layer map specific failures to appropriate HTTP status codes (400 for bad input, 502 for upstream API failures, 500 for unexpected errors).
- **Centralized config and logging** — avoids scattered `os.getenv()` calls and inconsistent logging across modules, making the codebase easier to maintain and deploy.

---

## Author

**Muhammad Wasil**
- GitHub: [github.com/Muhammad-Wasil-Ali](https://github.com/Muhammad-Wasil-Ali)
- LinkedIn: [linkedin.com/in/muhammad-wasil-ali](https://linkedin.com/in/muhammad-wasil-ali)

---

## License

This project is open source and available under the [MIT License](LICENSE).
