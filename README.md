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
run_stack.ps1

### Run the application
docker run -d -p 8000:8000 fastapi-regression:latest

```

