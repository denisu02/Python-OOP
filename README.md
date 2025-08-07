# OOP Python Flask App

This is a simple Flask web application that provides mathematical operations (power, factorial, Fibonacci) and logs each request to a SQLite database. The app also exposes Prometheus metrics for monitoring.

## Features

- **Power Calculation**: Compute `a^b` for user-provided values.
- **Fibonacci**: Compute the nth Fibonacci number.
- **Factorial**: Compute the factorial of n.
- **Request Logging**: All operations are logged to a database.
- **Prometheus Metrics**: Basic request metrics are exposed.
- **View Logs**: See a list of all previous operations.

## Project Structure

```
.
├── app.py
├── config.py
├── logging_utils.py
├── math_utils.py
├── models.py
├── requirements.txt
├── static/
│   └── style.css
├── instance/
│   └── database.db
├── .env
├── .gitignore
```

## Setup

1. **Clone the repository** and navigate to the project folder.

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Configure environment variables** in `.env`:
    ```
    DATABASE_URI=sqlite:///instance/database.db
    ```

4. **Run the application**:
    ```sh
    python app.py
    ```

5. **Access the app** at [http://localhost:5000](http://localhost:5000).

## Endpoints

- `/` — Main page with forms for all operations.
- `/pow` — Power calculation (`a` and `b` as query parameters).
- `/fib/<n>` — Fibonacci calculation.
- `/factorial/<n>` — Factorial calculation.
- `/logs` — View operation logs.