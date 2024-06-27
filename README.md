# All-in-One FastAPI Backend for Telegram Mini-Apps
___

This project provides a robust and efficient backend solution designed specifically for handling Telegram mini-apps. It leverages the power of FastAPI, providing high performance, easy-to-use endpoints, and seamless integration with various services like Redis, RabbitMQ, and PostgreSQL.

## Features

- **High Performance**: Utilizes FastAPI for fast, asynchronous request handling.
- **Database Integration**: Supports PostgreSQL with both standard and Psycopg2 connectors.
- **Messaging Support**: Integrates with RabbitMQ for message brokering.
- **Caching**: Utilizes Redis for caching purposes.
- **Scalable Architecture**: Configurable connection pooling and overflow management.
- **Easy Deployment**: Environment variables for configuration to streamline deployment.
- **Observability**: Integrates with Prometheus, Loki, Grafana, and Tempo for monitoring, logging, and tracing.

## Getting Started

### Prerequisites

- Python 3.11
- PostgreSQL
- Redis
- RabbitMQ
- Docker & Docker Compose

### Installation

1. **Install the dependencies**:
    ```bash
    poetry install
    ```

2. **Set up the environment variables**:

    Create a `.env` file in the root directory of the project and populate it with your configuration values. Use the `.env.example` file as a reference:

    ```env
    DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/mini_app_db
    DATABASE_URL_PSYCOPG2=postgresql+psycopg2://postgres:password@localhost/mini_app_db
    
    DB_USERNAME=postgres
    DB_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5432
    DB_DATABASE=mini_app_db
    
    TRACEBACK_OUTPUT_ENABLED=True
    
    REDIS_HOST=localhost
    REDIS_PORT=6379
   
    RABBITMQ_HOST=localhost
    RABBITMQ_PORT=5672
    RABBITMQ_USER=guest
    RABBITMQ_PASSWORD=guest
    
    ASYNC_ENGINE_POOL_SIZE=20
    ASYNC_ENGINE_MAX_OVERFLOW=50
    
    BOT_LINK=<BOT_LINK>
    
    BOT_TOKEN=<BOT_TOKEN>
    
    OTLP_GRPC_ENDPOINT=http://localhost:4317
    ```
   
3.  **Create postgres database, e.g. `mini_app_db`**.

**Integrate with your Telegram Mini-App**: 

Your Telegram Mini-App should send initialization data using `POST`, `PUT` requests in the following format:

```json
{
  "initData": "query_id=<query_id>&user=%7B%22id%22%3A456158277%2C%22first_name%22%3A%22John%20Doe%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22john_doe%22%2C%22language_code%22%3A%22en%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=<CHAT_INSTANCE>&chat_type=private&auth_date=<AUTH_DATE>&hash=<HASH>"
}
```

### Docker Compose Setup

The project includes a `docker-compose.yml` file that sets up the entire stack for you, including the database, caching, messaging, and monitoring services.

### Running the Application with Docker Compose

To start the entire application stack using

 Docker Compose, follow these steps:

1. **Build and start the containers**:
    ```bash
    docker-compose up --build -d
    ```

2. **Access the services**:
    - **API**: `http://localhost:8000`
    - **Grafana**: `http://localhost:3000`
    - **Prometheus**: `http://localhost:9090`
    - **Loki**: `http://localhost:3100`
    - **Tempo**: `http://localhost:4317`
    - **RabbitMQ Management**: `http://localhost:15672`