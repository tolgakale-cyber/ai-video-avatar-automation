import asyncio
import os

import edge_tts


VOICE = "tr-TR-AhmetNeural"


async def _generate_speech(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(output_path)


def generate_speech(text, output_path):
    asyncio.run(
        _generate_speech(text, output_path)
    )