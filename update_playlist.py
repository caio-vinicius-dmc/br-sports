import urllib.request

# Varreremos as duas maiores listas do projeto para garantir que nada passe despercebido
urls = [
    "https://iptv-org.github.io/iptv/countries/br.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

lines = []
for url in urls:
    print(f"Baixando fonte: {url}")
    try:
        req = urllib.request.urlopen(url)
        lines.extend([line.decode("utf-8") for line in req.readlines()])
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

filtered_playlist = ["#EXTM3U\n"]
added_links = set()
save_next = False
current_inf = ""

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # 1. Identifica se é conteúdo de esporte
        is_sport = 'group-title="sports"' in line_lower or "sport" in line_lower or "futebol" in line_lower
        
        # 2. Lista das marcas premium e nacionais que você quer caçar
        is_premium_br = any(marca in line_lower for marca in [
            "premiere", "sportv", "tnt sports", "combate", "bandsports", 
            "cazetv", "nsports", "ge fast", "espn"
        ])
        
        # 3. Confirmação de nacionalidade brasileira
        is_br = ".br" in line_lower or "@br" in line_lower or "brazil" in line_lower or "portuguese" in line_lower
        
        # 4. Trava de segurança absoluta contra canais estrangeiros (Espanha, Argentina, EUA, etc)
        is_foreign = any(gringo in line_lower for gringo in [
            ".ar", ".mx", ".us", ".uk", ".es", ".cl", ".co", ".pe", ".uy", ".pt",
            "premier league", "pluto tv", "smithsonian", "voyager", "mtv"
        ])
        
        # --- MOTOR DE DECISÃO ---
        is_valid = False
        
        # Regra A: Se é do Brasil E (é esporte OU marca famosa), tá aprovado.
        if is_br and (is_sport or is_premium_br):
            is_valid = True
            
        # Regra B: Se tem o nome de uma marca famosa (ex: Premiere), mas o repositório 
        # esqueceu de colocar a tag ".br", a gente aprova DESDE QUE não tenha tag gringa (.us, .ar).
        elif is_premium_br and not is_foreign:
            is_valid = True
            
        # Regra C: O bloqueio final. Se caiu no filtro de país estrangeiro, bloqueia.
        if is_foreign and not is_br:
            is_valid = False

        if is_valid:
            save_next = True
            current_inf = line
        else:
            save_next = False
            
    elif save_next:
        if line.startswith("http"):
            # O 'set' (added_links) garante que não teremos canais duplicados 
            # já que estamos buscando em duas listas diferentes.
            if line not in added_links:
                filtered_playlist.append(current_inf)
                filtered_playlist.append(line)
                added_links.add(line)
        save_next = False

# Salva o arquivo final
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Playlist extraída! Total de links válidos salvos: {len(filtered_playlist) // 2}")
