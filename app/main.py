"""
Single Responsibility Principle
"""
import json
import xml.etree.ElementTree as ET


class DisplayTypeBook:
    def display_console(self, content):
        print(content)

    def display_reverse(self, content):
        print(content[::-1])


class PrintBookContent:
    def print_book_console(self, title, content):
        print(f"Printing the book: {title}...")
        print(content)

    def print_book_reverse(self, title, content):
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class SerializeBook:
    def serialize_json(self, title, content):
        return json.dumps({"title": title, "content": content})

    def serialize_xml(self, title, content):
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
        self.display_type_book = DisplayTypeBook()
        self.print_book_content = PrintBookContent()
        self.serialize_book = SerializeBook()

    def display(self, method_type: str):
        if method_type == "console":
            self.display_type_book.display_console(self.content)

        elif method_type == "reverse":
            self.display_type_book.display_reverse(self.content)

    def print_book(self, method_type: str):
        if method_type == "console":
            self.print_book_content.print_book_console(
                self.title, self.content
            )

        elif method_type == "reverse":
            self.print_book_content.print_book_reverse(
                self.title, self.content
            )

    def serialize(self, method_type: str):
        if method_type == "json":
            return self.serialize_book.serialize_json(
                self.title, self.content
            )

        elif method_type == "xml":
            return self.serialize_book.serialize_xml(self.title, self.content)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            book.display(method_type)
        elif cmd == "print":
            book.print_book(method_type)
        elif cmd == "serialize":
            return book.serialize(method_type)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
