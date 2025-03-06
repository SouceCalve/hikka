from hikkatl.types import Message
from .. import loader, utils
import random

@loader.tds
class NekoSpeakModule(loader.Module):
    """Модуль для стилизации речи под неко"""
    strings = {"name": "NekoSpeak", "converted": "{text}"}
    strings_ru = {"converted": "{text}"}

    def __init__(self):
        self.active = False
        self.pm_enabled = False
        self.public_enabled = False
        self.realcatlike = False

    def neko_speak(self, text):
        # Замена "н" на "ня" в некоторых словах
        words = text.split()
        new_words = []
        for word in words:
            if word.lower().startswith("н") and len(word) > 1:
                word = "ня" + word[2:]
            new_words.append(word)
            if word.lower().startswith("р") and len(word) > 1:
                word = "ррр" + word[1:]
            new_words.append(word)
        text = " ".join(new_words)

        # Замена стандартных фраз
        replacements = {
            "нет ": "нят",
            " нет ": "нят",
            " нет": "нят",
            "ничего": "нячего",
            " но": " ня",
            " но ": " ня ",
            "но ": "ня ",
            "что?": "ня?",
            "ура!": "ня!",
            "о нет": "о-ня!",
            "мур": "муррр",
            "пре": "пррре",
            "ра": "ррра",
            "привет": "мяувет",
            "хорошо":"мяу-ряско",
            "плохо":"мяу-чалька",
            "пиздец":"Мря!",
            "блять":"Мяр!",
            "замечательных":"замуррчательных",
            "няко":"неко",
            "нядо":"надо"
        }
        for key, value in replacements.items():
            text = text.replace(key, value)

        # Добавление "мяу" и концовок
        if random.random() < 0.3:  # 30% шанс добавить "мяу"
            text += " мяу~"
        elif random.random() < 0.2:  # 20% шанс добавить "-ня"
            text += "-ня"

        return text

    @loader.command(ru_doc="Стилизовать текст под неко")
    async def neko(self, message: Message):
        """Стилизовать текст под неко"""
        text = utils.get_args_raw(message)
        if not text:
            return await utils.answer(message, "Ня? Введи текст!")

        converted_text = self.neko_speak(text)
        await utils.answer(message, self.strings("converted").format(text=converted_text))

    @loader.command(ru_doc="Включить автоматическое преобразование речи в неко-стиль")
    async def nekospeak(self, message: Message):
        """Включить автоматическое преобразование речи в неко-стиль"""
        self.active = True
        await utils.answer(message, "Ня~ Теперь все твои сообщения будут преобразовываться!")

    @loader.command(ru_doc="Отключить автоматическое преобразование речи в неко-стиль")
    async def nekospeakstop(self, message: Message):
        """Отключить автоматическое преобразование речи в неко-стиль"""
        self.active = False
        await utils.answer(message, "Ня... Теперь сообщения не будут изменяться.")

    @loader.command(ru_doc="Переключить преобразование сообщений в ЛС")
    async def nekospeakpm(self, message: Message):
        """Переключить преобразование сообщений в ЛС"""
        self.pm_enabled = not self.pm_enabled
        status = "включено" if self.pm_enabled else "выключено"
        await utils.answer(message, f"Ня! Преобразование в ЛС теперь {status}.")

    @loader.command(ru_doc="Переключить преобразование сообщений в публичных чатах")
    async def nekospeakpublic(self, message: Message):
        """Переключить преобразование сообщений в публичных чатах"""
        self.public_enabled = not self.public_enabled
        status = "включено" if self.public_enabled else "выключено"
        await utils.answer(message, f"Ня! Преобразование в публичных чатах теперь {status}.")

    async def watcher(self, message: Message):
        if not self.active:
            return
        if message.out:
            if message.is_private and not self.pm_enabled:
                return
            if not message.is_private and not self.public_enabled:
                return
            new_text = self.neko_speak(message.text)
            await message.edit(new_text)
