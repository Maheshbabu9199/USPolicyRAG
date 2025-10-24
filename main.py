from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.router.api_router import api_router

app = FastAPI(version='0.1', title='USPolicy RAG')


@app.get("/health", response_class=JSONResponse)
async def health_check():   
    """
    Health check endpoint to verify the service is running.
    """
    return JSONResponse(content={"status": "ok"}, status_code=200)

app.include_router(router=api_router, prefix='/api')
