class Vacancy:
    def __init__(self, title: str, salary: int, link: str, description: str):
        self.title = title
        self.salary = salary
        self.link = link
        self.description = description


    def __str__(self):
        return f"{self.title}, {self.salary}, {self.link}, {self.description}"


    def __lt__(self, other):
        return self.salary < other.salary


    def __eq__(self, other):
        return self.title == other.title and \
            self.salary == other.salary and \
            self.link == other.link and \
            self.description == other.description



