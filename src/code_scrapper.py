import pathlib

CONTENT_OUTPUT_PATH = pathlib.Path() / 'data' / 'corpora' / 'raw' / 'code' / 'code.txt'
CONTENT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

SCAN_FOLDERS = [
    # pathlib.Path('/Users/catalyst/Desktop/Extension'),
    # pathlib.Path('/Users/catalyst/Desktop/Учёба'),
    pathlib.Path('/Volumes/MVME/Catalyst/Код'),
]
ALLOWED_FILES = {
    '.py',
    '.java',
    '.cpp', '.cs', 
    '.rs',
    '.html', '.js', '.css', '.tsx', '.jsx',
    '.yaml', '.toml',
    '.sh', '.zsh'
}
IGNORE_FOLDERS = {
    'venv', '__pycache__', 'static',
    'build', 'dist', 'bin', 
    'Library', 'Imported',
    'node_modules', '.next', 'public',
    'target',
    '.git',
    'dumps', 'data', 'img', 'images', 'pages', '.obsidian',
    'etc', 'tests', 
    'Mi-Create', 'PointsMiner', 'PointsMinerV2',
}
IGNORE_FILES = {
    '*.min.css', '*.min.js', 
    '*save.py', '*save.toml', '._*',
    'Лог с цветами'
}

# Get code from all files
validates_files = set() 
content = ''

for folder in SCAN_FOLDERS:
    for file in folder.glob('*/**'):
        if not file.is_file():
            continue

        if file.suffix not in ALLOWED_FILES:
            continue

        if any(file.match(pattern) for pattern in IGNORE_FILES):
            continue

        if any(ignore_folder in file.parts[:-1] for ignore_folder in IGNORE_FOLDERS):
            continue

        validates_files.add(file.relative_to(folder))
        content += open(file, 'r', encoding='utf-8', errors='ignore').read()

validates_files = sorted(validates_files)

# Group all code in one file
with open(CONTENT_OUTPUT_PATH, 'w') as file:
    file.write(content)

print(*('\n - ' + str(file) for file in validates_files))
print(f'Gathered {len(validates_files)} files')
