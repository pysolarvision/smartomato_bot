import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from config import Config

from routers import router as main_router
from routers.commands.helpers import create_folder, image_resizer

config = Config()
dp = Dispatcher()
dp.include_router(main_router)


@dp.message(F.document)
async def download_documents(msg: types.Message, state: FSMContext):
    await msg.reply(text='Изображение получил, скачиваю. Преобразовываю.')

    user_id: int = msg.from_user.id

    create_folder(str(config.path_load), user_id)
    create_folder(str(config.path_upload_v1), user_id)
    create_folder(str(config.path_upload_v2), user_id)

    file_id: str = msg.document.file_id
    file = await msg.bot.get_file(file_id)
    file_path: str = file.file_path

    user_data = await state.get_data()
    cut_top_value = int(user_data.get('cut_top', 0))
    cut_bottom_value = int(user_data.get('cut_bottom', 0))

    await msg.bot.download_file(file_path=file_path,
                                destination=f'{str(config.path_load)}/{user_id}/{msg.document.file_name}')

    loop = asyncio.get_event_loop()
    try:
        processed_image_v1 = await loop.run_in_executor(None,
                                                        image_resizer,
                                                        f'{str(config.path_load)}/{user_id}/{msg.document.file_name}',
                                                        cut_top_value,
                                                        cut_bottom_value,
                                                        1284,
                                                        2778)
        processed_image_v2 = await loop.run_in_executor(None,
                                                        image_resizer,
                                                        f'{str(config.path_load)}/{user_id}/{msg.document.file_name}',
                                                        cut_top_value,
                                                        cut_bottom_value,
                                                        1242,
                                                        2208)
    except ValueError as e:
        await msg.reply(text=f"Ошибка при манипулировании изображением: {e}")
    else:
        processed_image_v1.save(f'{str(config.path_upload_v1)}/{user_id}/65_{msg.document.file_name}')
        processed_image_v2.save(f'{str(config.path_upload_v2)}/{user_id}/55_{msg.document.file_name}')

        await msg.reply_document(
            document=types.FSInputFile(
                path=f'{str(config.path_upload_v1)}/{user_id}/65_{msg.document.file_name}'),
            caption="Изображение 1284х2778 6.5")

        await msg.reply_document(
            document=types.FSInputFile(
                path=f'{str(config.path_upload_v2)}/{user_id}/55_{msg.document.file_name}'),
            caption="Изображение 1242х2208 5.5")


async def main():
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
