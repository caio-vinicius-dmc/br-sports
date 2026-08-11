import urllib.request
import re

# Usando a lista mestre (index.m3u) que contém TODOS os links do repositório
url = "https://iptv-org.github.io/iptv/index.m3u"

print("Baixando a lista mestre completa (isso pode levar alguns segundos)...")
try:
    req = urllib.request.urlopen(url)
    lines = [line.decode("utf-8") for line in req.readlines()]
except Exception as e:
    print(f"Erro ao baixar a lista: {e}")
    lines = []

filtered_playlist = ["#EXTM3U\n"]
added_links = set()
save_next = False
current_inf = ""

# Marcas e palavras-chave que você quer garantir na busca
marcas_alvo = ["premiere", "tnt", "sportv", "espn", "combate", "bandsports", "cazetv", "nsports", "ge fast"]

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # 1. Identificadores FORTES de que o canal é do Brasil ou em Português
        is_br = (
            'tvg-country="br"' in line_lower or 
            '.br"' in line_lower or 
            '.br@' in line_lower or 
            'tvg-language="portuguese"' in line_lower
        )
        
        # 2. Identificadores de Esporte
        is_sport = (
            'group-title="sports"' in line_lower or 
            "sport" in line_lower or 
            "futebol" in line_lower
        )
        
        # 3. Verifica se tem as marcas específicas (usando regex \b para pegar a palavra exata)
        has_marca = bool(re.search(r'\b(premiere|tnt|sportv|espn|combate|bandsports|cazetv|nsports|ge fast)\b', line_lower))
        
        # 4. Trava de segurança: impede que a TNT do México ou ESPN dos EUA entrem por acidente
        is_foreign = bool(re.search(r'tvg-country="(us|uk|ar|mx|es|pt|cl|co|pe|uy|bo|ec)"', line_lower))

        is_valid = False
        
        # Lógica principal de decisão:
        if is_br and (is_sport or has_marca):
            # É do Brasil e é esporte (ou marca famosa). Aprovado.
            is_valid = True
        elif has_marca and not is_foreign:
            # Tem a marca que você quer, a lista não diz que é BR, mas também não tem tag de país gringo. Aprovado.
            is_valid = True

        if is_valid:
            save_next = True
            current_inf = line
        else:
            save_next = False
            
    elif save_next:
        if line.startswith("http"):
            # O 'set' evita que links iguais entrem duplicados na sua lista
            if line not in added_links:
                filtered_playlist.append(current_inf)
                filtered_playlist.append(line)
                added_links.add(line)
        save_next = False

# Salva o arquivo final
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Filtragem da lista mestre concluída! Total de canais salvos: {len(filtered_playlist) // 2}")
