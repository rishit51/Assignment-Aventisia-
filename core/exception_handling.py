from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx


async def github_api_error_handler(request: Request, exc: httpx.HTTPStatusError):
    print(exc)
    return JSONResponse(
        status_code=exc.response.status_code,
        content={"detail": exc.response.json().get(
            "message", "GitHub API error")}
    )


async def github_network_error_handler(request: Request, exc: httpx.RequestError):
    return JSONResponse(
        status_code=503,
        content={"detail": f"Could not reach GitHub API: {type(exc).__name__}"}
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(httpx.HTTPStatusError, github_api_error_handler)
    app.add_exception_handler(httpx.RequestError, github_network_error_handler)
