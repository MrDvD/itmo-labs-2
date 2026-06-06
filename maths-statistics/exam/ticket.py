import argparse
import os
import random
import sys
from typing import List, Set


def load_questions(file_path: str) -> List[str]:
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл '{file_path}' не найден.")
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def load_history(history_path: str) -> Set[str]:
    if not os.path.exists(history_path):
        return set()
    with open(history_path, "r", encoding="utf-8") as file:
        return {line.strip() for line in file if line.strip()}


def save_history(history_path: str, history: Set[str]) -> None:
    with open(history_path, "w", encoding="utf-8") as file:
        for q in history:
            file.write(f"{q}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Утилита для случайного выбора вопросов из файла с поддержкой истории."
    )
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        required=True,
        help="Путь к текстовому файлу с вопросами",
    )
    parser.add_argument(
        "-p",
        "--preserve-history",
        action="store_true",
        help="Включить режим сохранения истории (не повторять старые вопросы)",
    )
    parser.add_argument(
        "-r",
        "--remove-history",
        action="store_true",
        help="Сбросить (удалить) файл истории перед запуском",
    )
    parser.add_argument(
        "--history-file",
        type=str,
        default="history.txt",
        help="Путь к файлу истории (по умолчанию: history.txt)",
    )
    args = parser.parse_args()

    if args.remove_history:
        if os.path.exists(args.history_file):
            try:
                os.remove(args.history_file)
                print(f"Файл истории '{args.history_file}' успешно удален.")
            except OSError as e:
                print(f"Ошибка при удалении файла истории: {e}")
        else:
            print(f"Файл истории '{args.history_file}' не существует.")

    questions: List[str] = load_questions(args.source)

    if args.preserve_history:
        history: Set[str] = load_history(args.history_file)
        available_questions: List[str] = [
            q for q in questions if q not in history
        ]
    else:
        history = set()
        available_questions = questions

    os.system("cls" if os.name == "nt" else "clear")
    print("--- 🎲 Тянем случайный билет... ---")

    if not available_questions:
        print("Все вопросы из файла уже были вытянуты!")
        print("Используйте параметр -r, чтобы сбросить историю.")
        print("---------------------------------")
        sys.exit(0)

    k: int = min(2, len(available_questions))
    selected: List[str] = random.sample(available_questions, k)

    print("Ваши вопросы:")
    for q in selected:
        print(f"👉 {q}")
        if args.preserve_history:
            history.add(q)

    if args.preserve_history:
        save_history(args.history_file, history)
        remaining: int = len(questions) - len(history)
        print("---------------------------------")
        print(f"Осталось невытянутых вопросов: {remaining} из {len(questions)}")

    print("---------------------------------")


if __name__ == "__main__":
    main()