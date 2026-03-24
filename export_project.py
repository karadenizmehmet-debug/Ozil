import os

OUTPUT_FILE = "project_dump.txt"
ROOT_DIR = "."

# hariç klasörler
EXCLUDE_FOLDERS = {
    ".git", "__pycache__", "venv", "env",
    "build", "dist", ".idea", ".vscode"
}

# dahil uzantılar
INCLUDE_EXTENSIONS = {
    ".py", ".html", ".js", ".json", ".css", ".txt"
}

# özellikle dahil edilmesin (güvenlik)
EXCLUDE_FILES = {
    ".env"
}

def should_skip(path):
    return any(folder in path for folder in EXCLUDE_FOLDERS)

def should_include(file):
    if file in EXCLUDE_FILES:
        return False
    return any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS)

def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as f:
                return f.read()
        except:
            return None
    except:
        return None

def export_project():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk(ROOT_DIR):
            if should_skip(root):
                continue

            for file in files:
                if not should_include(file):
                    continue

                full_path = os.path.join(root, file)

                content = read_file_safe(full_path)
                if content is None:
                    print(f"Atlandı (okunamadı): {full_path}")
                    continue

                # başlık
                out.write("\n" + "="*80 + "\n")
                out.write(f"FILE: {full_path}\n")
                out.write("="*80 + "\n\n")

                # içerik
                out.write(content)
                out.write("\n\n")

    print(f"✅ Tüm proje aktarıldı: {OUTPUT_FILE}")

if __name__ == "__main__":
    export_project()