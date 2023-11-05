import os
import re

# Путь к вашему проекту (нужно указать конкретный путь к директории проекта)
project_path = '/home/oleksandr/github_pavilion/prework/Warsztat'

# Путь к файлу, в который будет сохранена вся документация
documentation_file = 'project_documentation.md'

# Regex для поиска строк документации
docstring_regex = re.compile(r'""".+?"""', re.DOTALL)


# Функция для извлечения и записи документации в файл
def extract_documentation(file_path, output_file):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        matches = docstring_regex.findall(content)
        if matches:
            output_file.write(f'\n# {os.path.basename(file_path)}\n\n')
            for match in matches:
                # Удаление лишних пробелов и кавычек
                cleaned_match = match.strip('"').strip()
                output_file.write(f'{cleaned_match}\n\n')


# Открытие файла для записи документации
with open(documentation_file, 'w', encoding='utf-8') as output_file:
    # Обход всех файлов в директории проекта
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                extract_documentation(os.path.join(root, file), output_file)

print(f'Документация проекта записана в файл {documentation_file}')
