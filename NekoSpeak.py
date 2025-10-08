from hikkatl.types import Message
from .. import loader, utils
import random

@loader.tds
class NekoSpeakModule(loader.Module):
    """Модуль для стилизации речи под неко"""

    strings = {
        "name": "NekoSpeak",
        "converted": "{text}",
        "banned": "Ня~ Чат {} добавлен в черный список.",
        "unbanned": "Ня~ Чат {} удален из черного списка.",
        "already_banned": "Ня... Этот чат уже в черном списке!",
        "not_banned": "Ня... Этот чат не был забанен!",
        "no_access": "Ня? У меня нет доступа к этому чату.",
        "banned_list": "Список забаненных чатов:\n{}"
    }

    def __init__(self):
        self.active = False
        self.pm_enabled = False
        self.public_enabled = False
        # Загружаем из БД или создаём новый список
        self.banned_chats = set()
        self.bad_minded = False

    async def client_ready(self):
        saved = self.db.get("NekoSpeak", "banned_chats", [])
        self.banned_chats = set(saved)

    def save_banned_chats(self):
        # Сохраняем список забаненных чатов в БД
        self.db.set("NekoSpeak", "banned_chats", list(self.banned_chats))


    def is_encrypt(self, text):
        flag = False
        encrypting_count=0
        for x in range(1,3):
            if("=" in text[-x]):
                encrypting_count+=1
            if(encrypting_count>=1):
                flag = True
        return flag

    def neko_speak(self, text):

        if(not self.is_encrypt(text)):
            words = text.split()
            new_words = []
            for word in words:
                if word.lower().startswith("н") and len(word) > 2 and (random.random() < 0.05 or self.bad_minded):
                    word = "ня" + word[2:]
                if random.random() < 0.05 or self.bad_minded:
                    word = word.replace("р", "р-" * random.randint(2,4)+"р")
                    word = word.replace("r", "r" * random.randint(2,4)+"r")
                new_words.append(word)
            text = " ".join(new_words)

            replacements = {
                "ничего": "нячего", "что?": "ня?", "ура!": "ня!", "о нет": "о-ня!",
                "привет": "мяувет", "Привет": "Мяувет", "хорошо":"мяу-ряско",
                "плохо":"мяу-чалька", "пиздец":"мря!", "Пиздец":"Мря!",
                "блять":"мяр!", "Блять":"Мяр!", "замечательные":"замуррчательные",
                "замечательный":"замуррчательный", "замечательных":"замуррчательных",
                "Замечательные":"Замуррчательные", "Замечательный":"Замуррчательный",
                "Замечательных":"Замуррчательных", "прекрасное":"замурчательное",
                "Прекрасное":"Замурчательное", "прекрасный":"замурчательный",
                "Прекрасный":"Замурчательный", "прекрасная":"замурчательная",
                "Прекрасная":"Замурчательная", "заебись":"замурчательно",
                "Заебись":"Замурчательно", "охуенно":"замурчательно",
                "Охуенно":"Замурчательно", "няхуя":"МРЯВ?! Ньё-ньё!!",
                "Няхуя":"МРЯВ?! Ньё-ньё!!", "няко":"неко", "Няко":"неко",
                "нядо":"надо", "Нядо":"Надо", "В рот ебал":"МРЯФФ!!",
                "в рот ебал":"МРЯФФ!!", "ебал":"мряк-мрря!", "Ебал":"МРЯФФ!!",
                "хуёво":"ньёрфф...", "Хуёво":"Ньёрфф...", "пидрилит":"мряк-мрря!",
                "Пидрилит":"Мряк-мрря!",
            }

            specialchar = [",",".","<",">","/","''",'""',":",";","{","}","[","]","|","!","@","#","$","%","^","&","?","*","(",")","-","_","+","=","`","~","№"]

            for key, value in replacements.items():
                if(random.random()<0.05 or self.bad_minded):
                    text = text.replace(key, value)

            if random.random() < 0.05 or self.bad_minded:
                    text += " мяу~"
            elif random.random() < 0.05 or self.bad_minded:
                if(text[-1:] in specialchar):
                    text=text[:-1]+"-ня"+text[-1:]
                else:
                    text += "-ня"

        return text

    @loader.command(ru_doc="Стилизовать текст под неко")
    async def neko(self, message: Message):
        text = utils.get_args_raw(message)
        if not text:
            return await utils.answer(message, "Ня? Введи текст!")
        converted_text = self.neko_speak(text)
        await utils.answer(message, self.strings("converted").format(text=converted_text))

    @loader.command(ru_doc="Включить автоматическое преобразование речи в неко-стиль")
    async def nekospeak(self, message: Message):
        self.active = True
        await utils.answer(message, "Ня~ Теперь все твои сообщения будут преобразовываться!")

    @loader.command(ru_doc="Отключить автоматическое преобразование речи в неко-стиль")
    async def nekospeakstop(self, message: Message):
        self.active = False
        await utils.answer(message, "Ня... Теперь сообщения не будут изменяться.")

    @loader.command(ru_doc="Переключить преобразование сообщений в ЛС")
    async def nekospeakpm(self, message: Message):
        self.pm_enabled = not self.pm_enabled
        status = "включено" if self.pm_enabled else "выключено"
        await utils.answer(message, f"Ня! Преобразование в ЛС теперь {status}.")

    @loader.command(ru_doc="Переключить преобразование сообщений в публичных чатах")
    async def nekospeakpublic(self, message: Message):
        self.public_enabled = not self.public_enabled
        status = "включено" if self.public_enabled else "выключено"
        await utils.answer(message, f"Ня! Преобразование в публичных чатах теперь {status}.")

    @loader.command(ru_doc="Отключает рандом, преобразовывает всё без шансов спастись")
    async def nekospeakdumb(self, message: Message):
        self.bad_minded = not self.bad_minded
        status = "отключён" if self.bad_minded else "включён"
        await utils.answer(message, f"Ня! Рандом {status}.")

    @loader.command(ru_doc="Заблокировать чат для работы модуля")
    async def nekospeakex(self, message: Message):
        args = utils.get_args_raw(message)
        try:
            chat_id = int(args) if args.isdigit() else None
            if not chat_id:
                reply = await message.get_reply_message()
                if reply:
                    chat_id = reply.sender_id or reply.chat_id
                else:
                    chat_id = message.chat_id
        except Exception:
            chat_id = message.chat_id

        if chat_id in self.banned_chats:
            await utils.answer(message, self.strings("already_banned"))
            return

        self.banned_chats.add(chat_id)
        self.save_banned_chats()
        await utils.answer(message, self.strings("banned").format(str(chat_id)))

    @loader.command(ru_doc="Разблокировать чат")
    async def nekospeakin(self, message: Message):
        args = utils.get_args_raw(message)
        try:
            chat_id = int(args) if args.isdigit() else None
            if not chat_id:
                reply = await message.get_reply_message()
                if reply:
                    chat_id = reply.sender_id or reply.chat_id
                else:
                    chat_id = message.chat_id
        except Exception:
            chat_id = message.chat_id

        if chat_id not in self.banned_chats:
            await utils.answer(message, self.strings("not_banned"))
            return

        self.banned_chats.remove(chat_id)
        self.save_banned_chats()
        await utils.answer(message, self.strings("unbanned").format(str(chat_id)))

    @loader.command(ru_doc="Показать список заблокированных чатов (только в ЛС)")
    async def nekospeaklist(self, message: Message):
        if not message.is_private:
            await utils.answer(message, self.strings("no_access"))
            return

        if not self.banned_chats:
            await utils.answer(message, "Ня... Список забаненных чатов пуст.")
            return

        banned_list = "\n".join([f"- {chat}" for chat in self.banned_chats])
        await utils.answer(message, self.strings("banned_list").format(banned_list))

    async def watcher(self, message: Message):
        if not self.active:
            return
        if message.out:
            chat_id = message.chat_id
            if chat_id in self.banned_chats:
                return
            if message.is_private and not self.pm_enabled:
                return
            if not message.is_private and not self.public_enabled:
                return
            new_text = self.neko_speak(message.text)
            if new_text != message.text:
                await message.edit(new_text)
