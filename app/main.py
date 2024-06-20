"""
Interface segregation
"""
from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET


class DisplayBook(ABC):
    @abstractmethod
    def display(self, content):
        pass


class PrintBook(ABC):
    @abstractmethod
    def print(self, title, content):
        pass


class SerializeBook(ABC):
    @abstractmethod
    def serialize(self, title, content):
        pass


class DisplayConsole(DisplayBook):
    def display(self, content):
        print(content)


class DisplayReverse(DisplayBook):
    def display(self, content):
        print(content[::-1])


class PrintConsole(PrintBook):
    def print(self, title, content):
        print(f"Printing the book: {title}...")
        print(content)


class PrintReverse(PrintBook):
    def print(self, title, content):
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class SerializeToJson(SerializeBook):
    def serialize(self, title, content):
        return json.dumps({"title": title, "content": content})


class SerializeToXml(SerializeBook):
    def serialize(self, title, content):
        root = ET.Element("book")
        title_elem = ET.SubElement(root, "title")
        title_elem.text = title
        content_elem = ET.SubElement(root, "content")
        content_elem.text = content
        return ET.tostring(root, encoding="unicode")


class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def display(self, display_strategy: DisplayBook):
        display_strategy.display(self.content)

    def print_book(self, print_strategy: PrintBook):
        print_strategy.print(self.title, self.content)

    def serialize(self, serialize_strategy: SerializeBook) -> str:
        return serialize_strategy.serialize(self.title, self.content)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            if method_type == "console":
                book.display(DisplayConsole())
            elif method_type == "reverse":
                book.display(DisplayReverse())
        elif cmd == "print":
            if method_type == "console":
                book.print_book(PrintConsole())
            elif method_type == "reverse":
                book.print_book(PrintReverse())
        elif cmd == "serialize":
            if method_type == "json":
                return book.serialize(SerializeToJson())
            elif method_type == "xml":
                return book.serialize(SerializeToXml())


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
