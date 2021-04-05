import os
import re
from typing import List, Dict, Any, Optional

from commitizen import defaults
from commitizen.cz.base import BaseCommitizen


class JacobCz(BaseCommitizen):
    bump_pattern = defaults.bump_pattern
    bump_map = defaults.bump_map
    commit_parser = defaults.commit_parser
    changelog_pattern = defaults.bump_pattern
    change_type_map = {
        "feat": "Добавлено",
        "fix": "Исправлено",
        "refactor": "Рефактор"
    }

    def questions(self) -> list:
        """Questions regarding the commit message."""
        questions: List[Dict[str, Any]] = [
            {
                "type": "list",
                "name": "prefix",
                "message": "Выберите тип изменений",
                "choices": [
                    {
                        "value": "fix",
                        "name": "fix: Исправление бага. Соответствует PATCH в нотации SemVer",
                    },
                    {
                        "value": "feat",
                        "name": "feat: Новый функционал. Соответствует MINOR в нотации SemVer",
                    },
                    {
                        "value": "docs",
                        "name": "docs: Изменение документации",
                    },
                    {
                        "value": "style",
                        "name": (
                            "style: Изменения, не меняющие смысл кода (форматирование, пробелы, запятые, пр.)"
                        ),
                    },
                    {
                        "value": "refactor",
                        "name": (
                            "refactor: Изменения кода, ни не добавляющие нового функционала, ни не чинящие баги"
                        ),
                    },
                    {
                        "value": "perf",
                        "name": "perf: Улучшения производительности",
                    },
                    {
                        "value": "test",
                        "name": (
                            "test: Добавление или исправления тестов"
                        ),
                    },
                    {
                        "value": "build",
                        "name": (
                            "build: Изменения, касающиеся системы сборки или зависимостей (примеры: deps, docker)"
                        ),
                    },
                    {
                        "value": "ci",
                        "name": (
                            "ci: Изменения конфига Github Actions"
                        ),
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "Что меняет этот коммит: ([enter] чтобы пропустить)\n"
                ),
            },
            {
                "type": "input",
                "name": "subject",
                "message": (
                    "Краткое описание изменений в активном залоге: (нижний регистр, без точки в конце)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "Дополнительная информация об изменениях: ([enter] чтобы пропустить)\n"
                ),
            },
            {
                "type": "confirm",
                "message": "Это НЕСОВМЕСТИМОЕ ИЗМЕНЕНИЕ? Соответствует MAJOR в нотации SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Футер. Информация о Несовместимом изменении и "
                    "упоминание ишью, которое закрывает этот коммит: ([enter] чтобы пропустить)\n"
                ),
            },
        ]
        return questions

    def message(self, answers: dict) -> str:
        """Generate the message with the given answers."""
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE: {footer}"
        if footer:
            footer = f"\n\n{footer}"

        message = f"{prefix}{scope}: {subject}{body}{footer}"

        return message

    def example(self) -> str:
        return (
            "fix: correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "closes issue #12"
        )

    def schema(self) -> str:
        return (
            "<тип>(<область изменений>): <краткое описание>\n"
            "<ПУСТАЯ СТРОКА>\n"
            "<подробное описание>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: )<футер>"
        )

    def schema_pattern(self) -> str:
        pattern = (
            r"(build|ci|docs|feat|fix|perf|refactor|style|test|chore|revert|bump)!?"
            r"(\(\S+\))?:(\s.*)"
        )
        return pattern

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content

    def process_commit(self, commit: str) -> str:
        pat = re.compile(self.schema_pattern())
        m = re.match(pat, commit)
        if m is None:
            return ""
        return m.group(3).strip()

    @staticmethod
    def changelog_hook(_: str, partial_changelog: Optional[str]) -> str:
        return partial_changelog


discover_this = JacobCz
