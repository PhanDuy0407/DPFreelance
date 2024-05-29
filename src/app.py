from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import routers

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

if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload="True")
