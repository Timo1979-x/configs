import glob
import os
from datetime import datetime
from datetime import timezone

def generate():
    domains = set()
    
    # Собираем все домены из файлов vpn-domains-*.txt
    files = glob.glob('data/vpn-domains-*.txt')
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                domain = line.strip()
                if domain and not domain.startswith('#'):
                    domains.add(domain)

    # Формат AutoProxy требует специального заголовка
    output_content = f"[AutoProxy 0.2.9]\n! generated at {datetime.now(timezone.utc)}\n\n"
    
    # Добавляем домены. 
    # Префикс || означает "сам домен и все поддомены"
    for domain in sorted(list(domains)):
        output_content += f"||{domain}\n"

    # Сохраняем в файл
    output_path = 'data/lists/AutoProxy-vpn-domains.list'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)

if __name__ == "__main__":
    generate()
