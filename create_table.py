from core.configs import settings
from core.database import engine
from core.base import Base
import models.__all_models


async def create_tables() -> None:
    
    print('Criando as tabelas no banco de dados...')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print('tabelas criadas com sucesso.')


if __name__ == '__main__':
    import asyncio
    print("iniciado")
    asyncio.run(create_tables())   
