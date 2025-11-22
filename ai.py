"""Простой модуль ИИ для NPC.

Здесь реализован:
- SimpleNPC: простой правило-ориентированный "ИИ" для диалогов
- Заготовка для интеграции с OpenAI (раскомментируйте и настройте при желании)
"""
import random

class SimpleNPC:
    def __init__(self, name="NPC", role="персонаж"):
        self.name = name
        self.role = role
        self.mood = random.choice(['нейтральна', 'дружелюбна', 'подозрительна'])

    def respond(self, player_text, context=None):
        """Возвращает строку-ответ на сообщение игрока.

        Логика простая:
        - Если игрок задает вопрос (заканчивается на ?), вернуть короткий ответ.
        - Если игрок говорит 'помоги', дать подсказку.
        - Иначе — сформировать ответ на основе рандомных шаблонов.
        """
        text = (player_text or '').strip().lower()
        if not text:
            return "..."  # молчание

        if text.endswith('?'):
            return self._answer_question(text, context)
        if 'помог' in text or 'подсказ' in text:
            return "Могу подсказать: попробуй осмотреться и поговорить с другими."

        templates = [
            "Я не уверена, что это хорошая идея.",
            "Хмм... звучит интересно.",
            "Расскажи ещё.",
            "Мне кажется, это опасно."
        ]
        return random.choice(templates)

    def _answer_question(self, text, context):
        # Очень простая "логика" ответов на вопросы
        if 'как' in text:
            return "Как? Ну... действуй осторожно и слушай своё сердце."
        if 'где' in text:
            room = context.get('room') if context else None
            if room:
                return f"Ты сейчас в {room}. Может, стоит посмотреть вокруг." 
            return "Тут вокруг темновато, но можно поискать указатели."
        return "Это сложный вопрос. Я подумаю."


# --- Заготовка для интеграции с OpenAI ---
# Чтобы использовать, раскомментируйте и установите библиотеку openai, затем
# установите переменную окружения OPENAI_API_KEY с вашим ключом.
#
# import os
# import openai
#
# def openai_respond(player_text, system_prompt="Ты — NPC в текстовой RPG."):
#     openai.api_key = os.getenv('OPENAI_API_KEY')
#     if not openai.api_key:
#         return "(OpenAI API ключ не найден)"\#
#     try:
#         resp = openai.ChatCompletion.create(
#             model='gpt-4o-mini',  # или другая доступная модель
#             messages=[
#                 {'role': 'system', 'content': system_prompt},
#                 {'role': 'user', 'content': player_text}
#             ],
#             max_tokens=150,
#             temperature=0.7
#         )
#         return resp['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return f"(Ошибка OpenAI: {e})"
