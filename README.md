# My Services

A collection of reusable Python service modules and clients for common backend and automation tasks.

The project is built as a personal backend toolkit and a practical space for developing reusable components around HTTP clients, browser automation, Redis, Telegram and FastAPI.

## 🎯 Purpose

The goal of the project is to collect common infrastructure components in one place instead of repeatedly implementing the same low-level functionality in individual projects.

The repository is also used to experiment with different approaches to designing reusable Python services and clients.

## 🧩 Planned Components

| Component             | Purpose                                                  |
| --------------------- | -------------------------------------------------------- |
| **Logging client**    | Common application logging                               |
| **Transport client**  | Async HTTP requests, cookies, retries and proxy support  |
| **Selenium client**   | Browser automation and HTML retrieval                    |
| **Playwright client** | Modern browser automation                                |
| **Redis client**      | Redis-based storage and supporting operations            |
| **DB client**         | Reusable database-related components                     |
| **Telegram client**   | Telegram Bot API integration                             |
| **FastAPI demo**      | Example of using the components in a backend application |

The repository is developed incrementally, so some components are currently in development.

## 🛠 Tech Stack

* Python 3.12+
* Poetry
* `asyncio`
* `aiohttp`
* `aiohttp-socks`
* `tenacity`
* Selenium
* Playwright
* Redis
* FastAPI
* aiogram
* pytest
* aioresponses

## 📁 Project Structure

```text
my-services/
├── services/
│   ├── ...
│   └── ...
├── .gitignore
├── pyproject.toml
└── README.md
```

The `services` package contains reusable components. Each service is intended to have a focused responsibility and can be used independently where appropriate.

## 🚀 Development

Install dependencies with Poetry:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest
```

The project uses `pytest-asyncio` and `aioresponses` for testing asynchronous code and HTTP interactions.

## 📌 Project Status

This is a work-in-progress personal toolkit rather than a published production-ready package.

The components are being developed incrementally and are intended to become reusable building blocks for future Python backend and automation projects.

The repository is deliberately kept separate from individual applications so that common infrastructure can evolve independently.
