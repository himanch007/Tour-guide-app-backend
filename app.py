from fastapi import Depends, FastAPI
import uvicorn
from middleware.exception_middleware import catch_exceptions_middleware
from middleware.http_error import Conflict, Unauthorized, Unprocessable, http_error_handler
from core.dependencies.authentication import authentication_dependency
from core.routes import api_router as authenticated_router
from unauth_routes import api_router as unauthenticated_router
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(docs_url=os.environ.get('DOCS_URL'))


@app.get("/")
async def index():
    return {"name": "Backend"}


if __name__ == "__main__":
    uvicorn.run(app)


# error handlers
app.add_exception_handler(Unauthorized, http_error_handler)
app.add_exception_handler(Conflict, http_error_handler)
app.add_exception_handler(Unprocessable, http_error_handler)


# middleware
# app.middleware('http')(catch_exceptions_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    authenticated_router,
    dependencies=[Depends(authentication_dependency)]
)
app.include_router(unauthenticated_router)
