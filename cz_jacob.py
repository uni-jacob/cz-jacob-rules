from commitizen.cz.base import BaseCommitizen


class JacobCz(BaseCommitizen):
    def questions(self) -> list:
        """Questions regarding the commit message."""
        questions = [
            {
                "type": "list",
                "name": "type",
                "message": "Выберите тип вносимых изменений",
                "choices": [
                    {
                        "key": "fix",
                        "value": "Исправление бага. PATCH в нотации SemVer",
                    },
                    {
                        "key": "docs",
                        "value": "Изменение документации",
                    },
                    {
                        "key": "style",
                        "value": "Изменения, не меняющие смысл кода (форматирование, пробелы, запятые, пр.)",
                    },
                    {
                        "key": "refactor",
                        "value": "Изменения кода, ни добавляющие нового функционала, ни чинящие баги",
                    },
                    {
                        "key": "perf",
                        "value": "Улучшения производительности",
                    },
                    {
                        "key": "test",
                        "value": "Исправление или добавление тестов",
                    },
                    {
                        "key": "build",
                        "value": "Изменения, касающиеся системы сборки или зависимостей (примеры: deps, docker)",
                    },
                    {
                        "key": "ci",
                        "value": "Изменения конфига Github Actions",
                    },
                ],
            },
            {"type": "input", "name": "title", "message": "Commit title"},
        ]
        return questions

    def message(self, answers: dict) -> str:
        """Generate the message with the given answers."""
        return "{0}: {1}".format(answers.get("type"), answers.get("title"))


discover_this = JacobCz
