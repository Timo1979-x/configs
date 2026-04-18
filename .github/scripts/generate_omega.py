import json
import glob
import os

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

    # Базовая структура ProxySwitchy Omega
    config = {
        # Профиль прокси (настройте параметры под себя здесь или позже в браузере)
        "+auto switch": {
          "color": "#99dd99",
          "defaultProfileName": "direct",
          "name": "auto switch",
          "profileType": "SwitchProfile",
          "revision": "19da17c0e34",
          "rules":[]
        },
        # Основной профиль переключения
        "+sing-box-proxy": {
          # "auth": {
          #   "fallbackProxy": {
          #     "password": "1",
          #     "username": "1"
          #   }
          # },
          "bypassList": [
            {
              "conditionType": "BypassCondition",
              "pattern": "127.0.0.1"
            },
            {
              "conditionType": "BypassCondition",
              "pattern": "::1"
            },
            {
              "conditionType": "BypassCondition",
              "pattern": "localhost"
            }
          ],
          "color": "#99ccee",
          "fallbackProxy": {
            "host": "sing-box-proxy",
            "port": 1080,
            "scheme": "http"
          },
          "name": "sing-box-proxy",
          "profileType": "FixedProfile",
          "revision": "19da17b640a"
        },
        "schemaVersion": 2
    }

    # Создаем правила для каждого домена
    for domain in sorted(list(domains)):
        rules = config["+auto switch"]["rules"]
        rules.append({
            "condition": {
                "conditionType": "HostWildcardCondition",
                "pattern": f"*.{domain}"
            },
            "profileName": "sing-box-proxy"
        })

    # Записываем результат
    output_path = 'data/lists/OmegaOptions.bak'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    generate()
