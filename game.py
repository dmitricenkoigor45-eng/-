#!/usr/bin/env python3
"""Простой текстовый движок для одиночной RP-игры.

Запуск: python game.py
"""
from ai import SimpleNPC
import sys

class Player:
    def __init__(self, name="Игрок"):
        self.name = name
        self.hp = 20
        self.inventory = []

class Room:
    def __init__(self, title, desc, exits=None, npcs=None):
        self.title = title
        self.desc = desc
        self.exits = exits or {}
        self.npcs = npcs or []

    def describe(self):
        print(f"\n== {self.title} ==\n{self.desc}\n")
        if self.npcs:
            print("Здесь присутствуют:")
            for n in self.npcs:
                print(f" - {n.name}")
        if self.exits:
            print("Выходы:", ', '.join(self.exits.keys()))

def prompt(prompt_text="> "):
    try:
        return input(prompt_text).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nВыход...")
        sys.exit(0)

def main():
    print("Добро пожаловать в RP-игру! Назовите вашего героя:")
    pname = prompt()
    if not pname:
        pname = "Игрок"
    player = Player(pname)

    # Создаем NPC с простым ИИ
    npc = SimpleNPC(name="Альта", role="путешественница")

    # Простая карта из 2 комнат
    room1 = Room("Таверна у Горящего Камня",
                 "Теплая таверна с деревянными столами и слышимой сверху музыкой.",
                 exits={"выйти": "переулок"},
                 npcs=[npc])
    room2 = Room("Пустой переулок",
                 "Узкий переулок, освещённый фонарями. Место выглядит подозрительно.",
                 exits={"войти": "таверна"})

    rooms = {"таверна": room1, "переулок": room2}
    current = "таверна"

    print(f"\nПривет, {player.name}! Начнем приключение.")

    while True:
        rooms[current].describe()
        cmd = prompt("Ввод: ").lower()

        if cmd in ("выход", "quit", "q", "exit"):
            print("Пока!") 
            break
        elif cmd in ("осмотреться", "look", "l"):
            rooms[current].describe()
        elif cmd.startswith("поговорить"):
            # Поговорить с NPC
            if rooms[current].npcs:
                # Если имя указано: "поговорить Альта"
                parts = cmd.split(maxsplit=1)
                target = None
                if len(parts) > 1:
                    name = parts[1].strip()
                    for n in rooms[current].npcs:
                        if n.name.lower() == name.lower():
                            target = n
                            break
                else:
                    target = rooms[current].npcs[0]

                if target:
                    print(f"Вы начинаете разговор с {target.name}...")
                    player_input = prompt("Сказать: ")
                    reply = target.respond(player_input, context={'room': current})
                    print(f"{target.name}: {reply}")
                else:
                    print("Тот персонаж не здесь.")
            else:
                print("Здесь никого нет, с кем можно поговорить.")
        elif cmd in rooms[current].exits:
            current = rooms[current].exits[cmd]
            print(f"Вы идете: {cmd} -> {current}")
        else:
            print("Неизвестная команда. Попробуйте: 'осмотреться', 'поговорить', 'выход'")

if __name__ == '__main__':
    main()
