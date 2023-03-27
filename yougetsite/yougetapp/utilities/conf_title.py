restricted_words = ['NUL', 'nul']
restricted_chars = ['/', ':', '*', '?', '"', '＂', '<', '>', '|', '.', '—', '\\']

def swap_restricted_char(char: str, res_char_list: list):
    if char in res_char_list:
        return '-'
    return char

def clean_char(char: str):
    if len(char.encode('utf-8')) <= 3:
        return True
    return False

def conf_title(title: str):
    cleaned_chars = ''.join(map(lambda x : swap_restricted_char(x, restricted_chars), filter(lambda y : clean_char(y), title))).strip()
    return ' '.join([word for word in cleaned_chars.split(' ') if word not in restricted_words]).strip()