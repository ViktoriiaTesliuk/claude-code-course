class Book:
    def __init__(self, title: str, author: str, year: int, genre: str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self) -> str:
        return f'"{self.title}" by {self.author} ({self.year}) [{self.genre}]'
