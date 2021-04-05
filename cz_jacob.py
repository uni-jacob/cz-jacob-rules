from commitizen.cz.base import BaseCommitizen


class JacobCz(BaseCommitizen):
    def questions(self) -> list:
        """Questions regarding the commit message."""
        questions = [
            {
                "type": "list",
                "name": "type",
                "message": "Выберите тип вносимых изменений",
                "choices": {
                    "fix": "Исправление бага. PATCH в нотации SemVer",
                    "docs": "Изменение документации",
                    "style": "Изменения, не меняющие смысл кода (форматирование, пробелы, запятые, пр.)",
                    "refactor": "Изменения кода, ни добавляющие нового функционала, ни чинящие баги",
                    "perf": "Улучшения производительности",
                    "test": "Исправление или добавление тестов",
                    "build": "Изменения, касающиеся системы сборки или зависимостей (примеры: deps, docker)",
                    "ci": "Изменения конфига Github Actions",
                },
            },
            {"type": "input", "name": "title", "message": "Commit title"},
        ]
        return questions

    def message(self, answers: dict) -> str:
        """Generate the message with the given answers."""
        return "{0}: {1}".format(answers.get("type"), answers.get("title"))


discover_this = JacobCz
