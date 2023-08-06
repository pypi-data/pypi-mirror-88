import asyncio

import hopfenmatrix.run
import hopfenmatrix.config
import hopfenmatrix.callbacks
import hopfenmatrix.matrix


async def test_send(api):
    #await api.send_message("test", "!RyLzgPLXqKckiBeGKc:matrix.hopfenspace.org")
    await asyncio.sleep(0.1)


def command_y():
    async def send_response(api: hopfenmatrix.matrix.MatrixBot, room, event):
        await api.send_reply("Received ping - PONG", room, event)
    return send_response


def command_x():
    async def send_response_2(api: hopfenmatrix.matrix.MatrixBot, room, event):
        x = await api.is_room_private(room)
    return send_response_2


def command_img(img_file):
    async def send_response_img(api: hopfenmatrix.matrix.MatrixBot, room, event):
        await api.send_image(img_file, room)
    return send_response_img


def command_vid(vid_file):
    async def send_response_vid(api: hopfenmatrix.matrix.MatrixBot, room, event):
        await api.send_video(vid_file, room)
    return send_response_vid


def command_file(file_path):
    async def send_response_file(api: hopfenmatrix.matrix.MatrixBot, room, event):
        await api.send_file(file_path, room)
    return send_response_file


def command_audio(audio_path):
    async def send_audio_file(api: hopfenmatrix.matrix.MatrixBot, room, event):
        await api.send_audio(audio_path, room)
    return send_audio_file


def command_emote():
    async def send_audio_file(api: hopfenmatrix.matrix.MatrixBot, room, event):
        await api.send_emote("Em", room, formatted_message='<font color=\"#ff0000\">Em</font>')
    return send_audio_file


def command_location():
    async def send_audio_file(api: hopfenmatrix.matrix.MatrixBot, room, event):
        await api.send_location("Bunker", "geo:48.53776,11.50583", room)
    return send_audio_file


async def main():
    matrix = hopfenmatrix.matrix.MatrixBot(enable_initial_info=True)
    matrix.set_auto_join(allowed_users=["@izomikron:matrix.hopfenspace.org"],
                         allowed_rooms=["!RyLzgPLXqKckiBeGKc:matrix.hopfenspace.org",
                                        "!nDJBWQuDujZgzsyNFv:matrix.hopfenspace.org"])

    matrix.register_command(command_img("/home/omikron/Nextcloud/GonGaming/Logos/omikron_1_1.jpg"),
                            accepted_aliases="img")
    matrix.register_command(command_vid("/home/omikron/Nextcloud/GonGaming/Logos/Intro.mp4"),
                            accepted_aliases="vid")
    matrix.register_command(command_file("/home/omikron/Nextcloud/3D-Models/3D_printer_test_mini.STL"),
                            accepted_aliases="file")
    matrix.register_command(command_audio("/home/omikron/Nextcloud/Music/Feuerschwanz/Methämmer/Schubsetanz.ogg"),
                            accepted_aliases="audio",
                            alias_is_regex=True,
                            command_syntax="<subcommand>",
                            description="Send an audio file.")
    matrix.register_command(command_emote(), accepted_aliases=["emote"])
    matrix.register_command(command_location(), accepted_aliases="loc")

    await matrix.start_bot()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
