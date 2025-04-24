# FastAPI + HTMX + Linear Regression Docker Application

This project is a simple **FastAPI** web application that leverages a **linear regression model** trained on some data. The application uses **HTMX** for enhanced user interactions and is fully containerized using **Podman** (or Docker).

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [License](#license)

## Project Overview

This repository demonstrates the following:
1. **Linear Regression Model**: A simple regression model built with `scikit-learn`.
2. **FastAPI Application**: A web application serving the model using FastAPI, with **HTMX** for dynamic content loading.
3. **Dockerization**: Full containerization using **Podman** (or Docker), including model training and serving.

## Prerequisites

To work with this project, you need the following tools:

- **Python 3.11+** (for development)
- **Podman** or **Docker** (for containerization)
- **HTMX** (for frontend interactivity)
- **scikit-learn** (for training the linear regression model)

### Python Packages
Make sure to install the required Python packages before running the project:


### Build stack
build_stack.ps1

### Build AND run stack
build_and_run_stack.ps1

### You may want to make a POST request using the following PowerShell command 
Invoke-RestMethod -Method POST -Uri http://127.0.0.1:8000/predict -Body (@{features = @(1.0, 1.0)} | ConvertTo-Json -Depth 2) -ContentType "application/json"

```

