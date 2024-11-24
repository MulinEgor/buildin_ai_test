from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.analyzer.dependencies import get_analyzer_service
from core.analyzer.service import AnalyzerService
from core.auth.utils.jwt import set_jwt_exception_handler
from core.auth.views import router as auth_router
from core.analyzer.views import router as analyzer_router
from core.database import set_prisma_config
from core.logger import setup_logging


setup_logging()

app = FastAPI(
    title='AI API',
    root_path='/api',
    docs_url='/',
    description='API для получения актуальных данных по акциям с анализом от Гига Чат'
)


load_dotenv()
set_prisma_config(app)
set_jwt_exception_handler(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


routers = [auth_router, analyzer_router]
for router in routers:
    app.include_router(router)
    
    
