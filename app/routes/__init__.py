from .home import router as home_router
from .predict import router as predict_router
from .health import router as health_router

routes = [home_router, predict_router, health_router]

