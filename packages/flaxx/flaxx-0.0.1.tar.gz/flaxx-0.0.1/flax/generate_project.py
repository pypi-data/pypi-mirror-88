import os

files = ["app.py", "models.py", "schemas.py", "enums.py", "database.py"]
folders = ["android", "ios"]


def generate_project_structure():
    for file in files:
        with open(f"app/{file}", 'w'):
            pass

    for folder in folders:
        os.makedirs(f"app/{folder}")


if __name__ == "__main__":
    generate_project_structure()
