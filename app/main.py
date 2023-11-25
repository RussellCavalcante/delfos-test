from fastapi import FastAPI
from app.routes.assets_routes import router as assets_routes
from app.routes.measurements_routes import router as measurements_routes
from app.routes.user_routes import router as user_routes

app = FastAPI()
@app.get('/health-check')
def health_check():
    return True

app.include_router(assets_routes)
app.include_router(measurements_routes)
app.include_router(user_routes)