from aiogram import Router, types, F
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart, Command

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(msg: types.Message) -> None:
    text = (
        "<b>Бот</b> позволяет форматировать изображения для площадок <b>AppStoreConnect</b> и "
        "<b>GooglePlayConsole</b>.\n\n"
        "Если на скриншоте есть <b>status bar</b> или нижняя панель управления, то не забудь обрезать их, "
        "чтобы площадки приняли изображение.\n"
        "Обрезать изображения можно с помощью команды <b>/cut</b> \n"
        "Чтобы посмотреть весь список команд, используй <b>/help</b>")

    await msg.answer(text=text)


@router.message(Command("help"))
async def handle_help(msg: types.Message) -> None:
    text = ("<b>/help</b> - описание функций\n"
            "<b>/cut</b> - указать значение среза изображения сверху и снизу в пикселях\n"
            "<b>/bar</b> - высота статус бара на iOS\n"
            "<b>/hub</b> - история изображений за несколько дней\n\n"
    
            "Если загружаемое изображение уже обрезано - пользоваться командой <b>/cut</b> необязательно."
            "Информация о параметрах среза сохраняется. Повторно задавать не нужно.\n\n"
            "Изображения должны быть отправлены как <b>документ</b>. Для этого при отправке изображений отключи "
            "сжатие фото.")

    await msg.answer(text=text,
                     action=ChatAction.TYPING)


@router.message(Command("bar"))
async def handel_photo(msg: types.Message) -> None:
    text: str = ("На iPhone X и более поздних моделях: Высота статусной строки составляет около <b>44</b> \n"
                 "На более ранних моделях: Обычно высота статусной строки составляет около <b>25</b> пикселей.")

    await msg.reply(text=text,
                    action=ChatAction.TYPING)


@router.message(F.photo)
async def handel_photo(msg: types.Message) -> None:
    text: str = "Ты забыл отключить сжатие изображений."

    await msg.reply(text=text,
                    action=ChatAction.TYPING)
