from fastapi import FastAPI
from pyaigress.api import api_router, lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)