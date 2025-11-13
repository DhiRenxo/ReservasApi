import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL_ASYNC")

async def test_connection():
    print(f"Intentando conectar a la base de datos:\n{DATABASE_URL}\n")

    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1 AS conectado"))
            print("✅ Conexión exitosa:", result.scalar())
    except Exception as e:
        print("❌ Error al conectar con la base de datos:")
        print(e)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
