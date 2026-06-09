import asyncio
import sys
sys.path.insert(0, '.')

from app.db.database import init_db, engine


async def main():
    print('正在创建数据库表...')
    await init_db()
    print('所有表创建完成！')
    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(main())
