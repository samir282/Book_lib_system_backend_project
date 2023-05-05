from fastapi import FastAPI

from server.database import base, engine
from router.router import router as appRoutes

base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(appRoutes, prefix='/api')




