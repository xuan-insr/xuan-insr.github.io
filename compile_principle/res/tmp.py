import os

files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".pdf")]
for f in files:
    print(f'- [{f}](./res/{f})')