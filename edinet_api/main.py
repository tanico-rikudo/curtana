from fastapi import FastAPI
from routers import headline, sample

app = FastAPI()
app.include_router(headline.router)
app.include_router(sample.router)

