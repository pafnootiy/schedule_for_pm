import json
from random import choice

from faker import Faker

import config


def create_fake_student(fake: Faker) -> dict:
    return {
        "name": fake.name(),
        "level": choice(["novice", "novice+", "junior", "middle"]),
        "tg_username": f"@{fake.word()}_{fake.word()}",
        "discord_username": f"{fake.word()}#{fake.random_int(1_000, 10_000)}",
        "is_far_east": choice([True, False]),
    }


def create_fake_pm(fake: Faker) -> dict:
    return {
        "name": fake.name(),
        "time_slot": str([(x, x + 1) for x in range(18, 21)]),
        "tg_username": f"@{fake.word()}_{fake.word()}",
        "discord_username": f"{fake.word()}#{fake.random_int(1_000, 10_000)}",
    }


def generate_student_json(count: int, fake: Faker) -> None:
    students = [create_fake_student(fake) for _ in range(count)]
    with open(f"{config.STUDENTS_TITLE}.json", "w") as file:
        json.dump(students, file, indent=4)


def generate_pm_json(count: int, fake: Faker) -> None:
    pm = [create_fake_pm(fake) for _ in range(count)]
    with open(f"{config.PM_TITLE}.json", "w") as file:
        json.dump(pm, file, indent=4)


def parse_json(filename: str) -> list[dict]:
    with open(filename, "r") as file:
        return json.load(file)


def main():
    fake = Faker()
    generate_student_json(200, fake)
    generate_pm_json(10, fake)


if __name__ == "__main__":
    main()
