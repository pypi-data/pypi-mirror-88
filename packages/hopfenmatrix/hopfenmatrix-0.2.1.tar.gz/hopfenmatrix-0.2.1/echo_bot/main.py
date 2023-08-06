import asyncio

from hopfenmatrix.matrix import MatrixBot


def echo():
    async def callback(bot: MatrixBot, room, event):
        await bot.send_reply(message=event.body, room_id=room.room_id, event=event)
    return callback


async def main():
    bot = MatrixBot()
    bot.set_auto_join()
    bot.register_command(echo(), accepted_aliases="", make_default=True)
    await bot.start_bot()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
