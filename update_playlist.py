import urllib.request
import re

# Baixa a lista mestre global do iptv-org
url = "https://iptv-org.github.io/iptv/index.m3u"

print("Baixando a lista mestre completa...")
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

# Marcas principais permitidas globalmente (mesmo que venham de fora)
marcas_globais = ["sportv", "espn", "premiere", "tnt", "combate", "bandsports", "cazetv", "nsports", "ge fast"]

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # 1. Verifica se é um canal nacional/português ou focado no Brasil
        is_br = (
            'tvg-country="br"' in line_lower or 
            '.br"' in line_lower or 
            '.br@' in line_lower or 
            'portuguese' in line_lower
        )
        
        # 2. Verifica se é da categoria de esportes
        is_sport = 'group-title="sports"' in line_lower or "sport" in line_lower or "futebol" in line_lower
        
        # 3. Verifica se o nome do canal bate exatamente com as marcas globais de interesse
        tem_marca_global = bool(re.search(r'\b(' + '|'.join(marcas_globais) + r')\b', line_lower))
        
        # Regra de aprovação limpa:
        # - Ou é um canal de esporte genuinamente brasileiro/português
        # - Ou é uma das marcas globais permitidas (sem puxar lixo de outras categorias gringas)
        if (is_br and is_sport) or tem_marca_global:
            # Trava de segurança para impedir lixo internacional que não seja brasileiro
            if not is_br and not any(m in line_lower for m in ["espn", "cazetv", "premiere", "sportv", "tnt"]):
                save_next = False
            else:
                save_next = True
                current_inf = line
        else:
            save_next = False
            
    elif save_next:
        if line.startswith("http"):
            # Evita links duplicados
            if line not in added_links:
                filtered_playlist.append(current_inf)
                filtered_playlist.append(line)
                added_links.add(line)
        save_next = False

# Salva o arquivo final limpo (sem linhas extras no final)
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Processo concluído! Total de canais salvos: {len(filtered_playlist) // 2}")
