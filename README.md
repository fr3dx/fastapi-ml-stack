# FastAPI + HTMX + Multi-output Linear Regression

This project is a **FastAPI**-based web application powered by a **multi-output linear regression model**, trained using `scikit-learn`. It includes a simple **HTMX** frontend for user interaction and is fully containerized using **Podman** or **Docker**.

## Tech Stack

- **Python 3.12**
- **FastAPI** (API framework)
- **HTMX** (frontend interactivity)
- **scikit-learn** (machine learning)
- **Pydantic** (data validation)
- **CORSMiddleware** (CORS handling)
- **Podman/Docker** (containerization)

## Features

- **Regression Model**: Predicts 3 outputs (`y₁`, `y₂`, `y₃`) from 2 inputs (`x₁`, `x₂`):

```
y₁ = 3 * x₁ + 2 * x₂
y₂ = x₁ - x₂
y₃ = -x₁ + 4 * x₂
```

- **API Endpoints**:
- `POST /predict`: Accepts form data and returns `y₁`, `y₂`, `y₃`
- `GET /`: Serves HTMX frontend
- `GET /health`: Healthcheck

- **Frontend**: HTMX-powered form with real-time results
- **Containerized**: Complete stack in containers for reproducibility

## Backend Overview

- **Model**: `regression_model.pkl` (pre-trained multi-output regression)
- **Pydantic Models**:
- `Features`: Validates input data
- `Predictions`: Structures output
- **Configuration**: `.env` support via `pydantic.BaseSettings`

## Prerequisites

- Docker Desktop (recommended for Windows) → [Download](https://www.docker.com/products/docker-desktop/)
- Podman Desktop → [Download](https://podman.io/getting-started/installation)
- PowerShell (built-in on Windows)

## Run Locally on Windows

Launch from PowerShell:
```
build_and_run_stack.ps1
```

Then open:
```
http://localhost:8000
```

### PowerShell Scripts

| Task                               | Script                           |
|------------------------------------|----------------------------------|
| Build containers                   | `build_stack.ps1`                |
| Build + run full stack             | `build_and_run_stack.ps1`        |
| Clean up containers/images         | `remove_all_container_images.ps1`|


## Project structure
```
fastapi-ml-stack/
│
├── app/
│   │
│   ├── config/                     # Config files
│   │   └── settings.py             # Pydantic
│   │
│   ├── models/                     # ML models, train and predict
│   │   ├── __init__.py
│   │   ├── train_model.py          
│   │   ├── load_model.py           
│   │   └── regression_model.pkl    # model created after training
│   │
│   ├── routes/                     # Routes
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── predict.py
│   │   └── health.py
│   │
│   ├── static/                     # Static files (CSS)
│   │   └── style.css
│   │
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── index.html
│   │   ├── result.html
│   │   └── error.html
│   │
│   ├── __init__.py
│   ├── main.py                     # FastAPI app init
│   └── .env
│
├── build_and_run_stack.ps1
├── build_stack.ps1
├── Dockerfile
├── healthcheck.py
├── requirements.txt 
└── remove_all_container_images.ps1 # Docker healthcheck script

```
## API Usage

### Predict (cURL)

```
curl -X POST -d "x1=1&x2=2" http://127.0.0.1:8000/predict
```
```
<div class="result">
    <h3>Prediction Results</h3>
    <div class="prediction">
      <p><strong>y₁:</strong> 7.0</p>
      <p><strong>y₂:</strong> -1.0</p>
      <p><strong>y₃:</strong> 7.0</p>
    </div>
    <div class="inputs">
      <p><strong>x₁:</strong> 1.0</p>
      <p><strong>x₂:</strong> 2.0</p>
    </div>
  </div>
```
```
curl -X GET http://127.0.0.1:8000/health
```
```
{"status":"ok"}
```


## The frontend
![Frontend](/images/fe.png)

## License

This project is licensed under the [MIT License](https://mit-license.org/).

---

<p align="center">
  Built with ❤️ and rational thought.<br>
  <em>Amore et ratione.</em>
</p>


