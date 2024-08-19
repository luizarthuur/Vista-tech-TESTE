#AQUI importamos todos os endpoints existentes para montar a nossa API completa

from fastapi import APIRouter

from api.v1.endpoints import curso

api_router = APIRouter()
api_router.include_router(curso.router, prefix='/cursos', tags=['Cursos'])

# O nosso endpoint de cursos será:
# /api/v1/cursos