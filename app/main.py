"""
Liskov substitution
"""
from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET


class DisplayTypeBook(ABC):
    @abstractmethod
    def display_type_book(self, content):
        pass


class PrintBookContent(ABC):
    @abstractmethod
    def print_book_content(self, content):
        pass


class SerializeBook(ABC):
    @abstractmethod
    def serialize_book(self, content):
        pass


class DisplayConsoleBook(DisplayTypeBook):
    def display_type_book(self, content):
        print(content)


class DisplayReverseBook(DisplayTypeBook):
    def display_type_book(self, content):
        print(content[::-1])


class PrintContentConsoleBook(PrintBookContent):
    def __init__(self, title):
        self.title = title

    def print_book_content(self, content):
        print(f"Printing the book: {self.title}...")
        print(content)


class PrintContentReverseBook(PrintBookContent):
    def __init__(self, title):
        self.title = title

    def print_book_content(self, content):
        print(f"Printing the book in reverse: {self.title}...")
        print(content[::-1])


class SerializeJsonBook(SerializeBook):
    def __init__(self, title):
        self.title = title

    def serialize_book(self, content):
        return json.dumps({"title": self.title, "content": content})


class SerializeXMLBook(SerializeBook):
    def __init__(self, title):
        self.title = title

    def serialize_book(self, content):
        root = ET.Element("book")
        title_elem = ET.SubElement(root, "title")
        title_elem.text = self.title
        content_elem = ET.SubElement(root, "content")
        content_elem.text = content
        return ET.tostring(root, encoding="unicode")


class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    def display(self, display_strategy: DisplayTypeBook):
        display_strategy.display_type_book(self.content)

    def print_book(self, print_strategy: PrintBookContent):
        print_strategy.print_book_content(self.content)

    def serialize(self, serialize_strategy: SerializeBook) -> str:
        return serialize_strategy.serialize_book(self.content)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            if method_type == "console":
                book.display(DisplayConsoleBook())
            elif method_type == "reverse":
                book.display(DisplayReverseBook())
        elif cmd == "print":
            if method_type == "console":
                book.print_book(PrintContentConsoleBook(book.title))
            elif method_type == "reverse":
                book.print_book(PrintContentReverseBook(book.title))
        elif cmd == "serialize":
            if method_type == "json":
                return book.serialize(SerializeJsonBook(book.title))
            elif method_type == "xml":
                return book.serialize(SerializeXMLBook(book.title))


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
