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

# POST CURSO
@router.post('/', status_code=status.HTTP_201_CREATED, response_model= CursoSchema)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(curso.titulo, curso.aulas, curso.horas)

    db.add(novo_curso)
    await db.commit()
    return curso

# GET CURSOS
@router.get('/',response_model=List[CursoSchema])
async def get_curso(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos      

@router.get('/{id_curso}', status_code=status.HTTP_200_OK, response_model=CursoSchema)
async def get_curso(id_curso: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()

        if curso:
            return curso
        
        raise HTTPException(detail='Curso não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
    

@router.put('/{id_curso}', status_code=status.HTTP_202_ACCEPTED, response_model=CursoSchema)
async def put_curso(id_curso: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:

        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso_up = result.scalar_one_or_none()

        if curso:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas

            await session.commit()

            return curso_up
        
        raise HTTPException(detail='Curso não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    
@router.delete('/{id_curso}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id_curso: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id_curso)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()


        if curso:
            await session.delete(curso)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(detail='Curso não Encontrado', status_code=status.HTTP_404_NOT_FOUND)
                       