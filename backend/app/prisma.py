from app.models.schemas import LogCreate
from prisma import Prisma

prisma = Prisma(auto_register=True)


async def startup():
    await prisma.connect()

    await LogCreate.prisma().create(
        {
            "message": "Inicia aplicação e base de dados",
            "logLevel": "INFO",
        }
    )


async def shutdown():
    await prisma.disconnect()
