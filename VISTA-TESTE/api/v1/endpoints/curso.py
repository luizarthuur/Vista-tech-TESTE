from typing import List
from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from core.deps import get_session

router = APIRouter()


#POST Curso
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def postCurso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):

    novo_curso = CursoModel(titulo=curso.titulo, aulas= curso.aulas, horas=curso.horas)

    db.add(novo_curso)

    await db.commit()

    return novo_curso


#GET Cursos
@router.get('/', response_model=List[CursoSchema])
async def getcursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos

#GET Curso
@router.get('/{curso_id}', response_model= CursoSchema, status_code= status.HTTP_200_OK)
async def getcurso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso: CursoModel = result.scalars().one_or_none()

        if curso:
            return curso
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
#PUT Curso
@router.put('/{curso_id}', response_model= CursoSchema, status_code= status.HTTP_202_ACCEPTED)
async def putcurso(curso_id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):

    async with db as session:

        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_update = result.scalars().one_or_none()

        if curso_update:
            curso_update.titulo = curso.titulo
            curso_update.aulas = curso.aulas
            curso_update.horas = curso.horas

            await session.commit()

            return curso_update
        
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
#Podemos validar melhor na parte do put em relação ao usuário informar ou não as informações para serem atualizadas.

#DEL Curso
@router.delete('/{curso_id}', status_code= status.HTTP_204_NO_CONTENT)
async def deletecurso(curso_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:

        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_delete = result.scalars().one_or_none()

        if curso_delete:
            await session.delete(curso_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
        
