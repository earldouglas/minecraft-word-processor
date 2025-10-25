from amulet_nbt import load
from amulet_nbt import utf8_escape_decoder
from dataclasses import dataclass
from pathlib import Path
from plyvel import DB
from plyvel import repair_db
from sys import argv
from sys import exit
from typing import Optional

if len(argv) != 2:
    print(f"Usage: {argv[0]} <db path>")
    exit(-1)


@dataclass
class Book:
    title: str
    author: str
    pages: [str]


def parse_item(item) -> list[Book]:
    books = []

    try:

        name = item["Name"].py_str

        if name == "minecraft:writable_book" or name == "minecraft:written_book":
            book = Book(
                title=item["tag"]["title"].py_str.strip(),
                author=item["tag"]["author"].py_str.strip(),
                pages=[],
            )

            for page in item["tag"]["pages"]:
                text = page["text"].py_str
                book.pages.append(text)

            books.append(book)

    except Exception as e:
        None

    return books


def exfiltrate_from_inventory(nbt) -> list[Book]:
    books = []

    try:
        for item in nbt["Inventory"]:
            books.extend(parse_item(item))
    except Exception as e:
        None

    return books


def exfiltrate_from_book(nbt) -> list[Book]:
    books = []

    try:
        item = nbt["book"]
        books.extend(parse_item(item))
    except Exception as e:
        None

    return books


def exfiltrate_from_nbt(nbt) -> list[Book]:
    books = []

    books.extend(exfiltrate_from_inventory(nbt))
    books.extend(exfiltrate_from_book(nbt))

    return books


def exfiltrate_from_buffer(buffer) -> list[Book]:
    books = []

    try:
        nbt = load(
            filepath_or_buffer=buffer,
            little_endian=True,
            string_decoder=utf8_escape_decoder,
        ).compound

        books.extend(exfiltrate_from_nbt(nbt))

    except Exception as e:
        None

    return books


def exfiltrate(db_path) -> list[Book]:
    books = []

    repair_db(db_path)
    db = DB(db_path, create_if_missing=False)

    for key, value in db:
        books.extend(exfiltrate_from_buffer(value))

    return books


def save_book(book, file_path) -> None:

    with open(file_path, "w") as f:

        print("---", file=f)
        print(f"title: {book.title}", file=f)
        print(f"author: {book.author}", file=f)
        print("...", file=f)

        print("", file=f)

        first = True
        for page in book.pages:

            if first:
                first = False
            else:
                print("---", file=f)
                print("", file=f)

            print(page, file=f)
            print("", file=f)


def main() -> None:

    Path("target").mkdir(parents=True, exist_ok=True)

    db_path = argv[1]
    books = exfiltrate(db_path)

    print(f"Found {len(books)} books:")

    for idx, book in enumerate(books):
        file_path = f"target/{idx}-{book.title.replace(" ", "-")}.md"
        print(f"* {book.title}, by {book.author} -> {file_path}")
        save_book(book, file_path)


main()
