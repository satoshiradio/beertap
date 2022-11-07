import asyncio

from Controller.maincontroller import MainController


async def main():
    app = MainController()
    await app.exec()
    pass


if __name__ == '__main__':
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
