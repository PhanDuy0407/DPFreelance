from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from router import routers
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in routers:
    app.include_router(router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error = "Network Error"
    for err in exc.errors():
        msg = err.get("msg", "")
        if msg == 'Field required':
            field = err.get("loc", (""))[-1]
            error = f"Missing field: {field}"
            break
        error = err.get("msg", "").split("Value error, ")[-1]
        break

    return JSONResponse(
        status_code=422,
        content={"detail": error}
    )


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload="True")
