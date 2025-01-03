import asyncio
import os
import shutil
from pathlib import Path
import logging
import argparse

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def read_folder(source_folder: Path, output_folder: Path):
    """
    Асинхронно читає всі файли у вихідній папці та копіює їх у цільову папку на основі розширення.
    """
    tasks = []
    try:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = Path(root) / file
                tasks.append(copy_file(file_path, output_folder))
        await asyncio.gather(*tasks)
        logger.info("Сортування завершено.")
    except Exception as e:
        logger.error(f"Помилка під час читання папки: {e}")

async def copy_file(file_path: Path, output_folder: Path):
    """
    Асинхронно копіює файл у відповідну підпапку в цільовій папці на основі розширення.
    """
    try:
        file_extension = file_path.suffix[1:] or "unknown"
        target_folder = output_folder / file_extension
        target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy, file_path, target_file)
        logger.info(f"Файл {file_path} скопійовано до {target_folder}")
    except Exception as e:
        logger.error(f"Помилка під час копіювання файлу {file_path}: {e}")

def main():
    # Парсер аргументів командного рядка
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширеннями.")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки.")
    parser.add_argument("output", type=str, help="Шлях до цільової папки.")
    args = parser.parse_args()

    source_folder = Path(args.source)
    output_folder = Path(args.output)

    # Перевірка існування папок
    if not source_folder.exists() or not source_folder.is_dir():
        logger.error("Вказана вихідна папка не існує або не є папкою.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    # Запуск асинхронної функції
    asyncio.run(read_folder(source_folder, output_folder))

if __name__ == "__main__":
    main()
