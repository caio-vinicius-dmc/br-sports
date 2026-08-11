import urllib.request

# Usando a lista mestre (index.m3u) que contém TODOS os links do repositório
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

# Todas as marcas que você exige que entrem na lista (sem restrição de país)
marcas_obrigatorias = [
    "sportv",
    "espn",
    "premiere",
    "premier",
    "tnt",
    "combate",
    "bandsports",
    "cazetv",
    "nsports",
    "ge fast",
    "futebol"
]

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # REGRA 1: O canal contém alguma das marcas obrigatórias?
        tem_marca = any(marca in line_lower for marca in marcas_obrigatorias)
        
        # REGRA 2: O canal é de esporte E tem indicativo de ser do Brasil/Português?
        is_br = 'tvg-country="br"' in line_lower or '.br"' in line_lower or '.br@' in line_lower or 'portuguese' in line_lower
        is_sport = 'group-title="sports"' in line_lower or "sport" in line_lower
        is_br_sports = is_br and is_sport
        
        # Se passar na Regra 1 OU na Regra 2, salva na lista
        if tem_marca or is_br_sports:
            save_next = True
            current_inf = line
        else:
            save_next = False
            
    elif save_next:
        if line.startswith("http"):
            # Evita que URLs idênticas se repitam na lista
            if line not in added_links:
                filtered_playlist.append(current_inf)
                filtered_playlist.append(line)
                added_links.add(line)
        save_next = False

# Salva o arquivo final
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Filtro atualizado! Total de canais salvos: {len(filtered_playlist) // 2}")
