import pathlib

from internal.setup import setup

ARGS = setup('corpus_scrapper')
ARGS['content_output_path'].parent.mkdir(parents=True, exist_ok=True)

# Get code from all files
validated_files = set() 
content = ''

for folder in ARGS['scan_folders']:
    for file in folder.glob('*/**'):
        if not file.is_file():
            continue

        if file.suffix not in ARGS['allowed_files']:
            continue

        if any(file.match(pattern) for pattern in ARGS['ignore_files']):
            continue

        if any(ignore_folder in file.parts[:-1] for ignore_folder in ARGS['ignore_folders']):
            continue

        validated_files.add(file.relative_to(folder))
        content += open(file, 'r', encoding='utf-8', errors='ignore').read()

validated_files = sorted(validated_files)

# Group all code in one file
with open(ARGS['content_output_path'], 'w') as file:
    file.write(content)

print(*('\n - ' + str(file) for file in validated_files))
print(f'Gathered {len(validated_files)} files')
