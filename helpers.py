def load_text(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        return f.readlines()
