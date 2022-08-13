from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/check")
async def root():
    return {"message": "Healthy"}


@app.get("/test")
async def root():
    return {"message": "Test Complete"}
