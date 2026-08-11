import urllib.request

# Fontes oficiais do repositório
urls = [
    "https://iptv-org.github.io/iptv/countries/br.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u"
]

lines = []
for url in urls:
    try:
        req = urllib.request.urlopen(url)
        lines.extend([line.decode("utf-8") for line in req.readlines()])
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

filtered_playlist = ["#EXTM3U\n"]
added_links = set()
save_next = False
current_inf = ""

# Padrões exatos extraídos da sua lista que identificam os canais que te interessam
identificadores_brasil = [
    ".br@", 
    "@br", 
    "@portuguese", 
    "cazetv", 
    "premiere", 
    "sportv", 
    "combate", 
    "tnt", 
    "bandsports", 
    "canal do inter", 
    "ge fast", 
    "nsports"
]

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # 1. Verifica se a linha pertence à categoria de esportes
        is_sport = (
            'group-title="sports"' in line_lower or 
            "sport" in line_lower or 
            "futebol" in line_lower or 
            "combate" in line_lower
        )
        
        # 2. Trava estrita de país/idioma (só passa se contiver os identificadores acima)
        is_br = any(identificador in line_lower for identificador in identificadores_brasil)
        
        if is_sport and is_br:
            save_next = True
            current_inf = line
        else:
            save_next = False
            
    elif save_next:
        if line.startswith("http"):
            # O set() garante que não entrem URLs duplicadas
            if line not in added_links:
                filtered_playlist.append(current_inf)
                filtered_playlist.append(line)
                added_links.add(line)
        save_next = False

# Salva o arquivo final
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Limpeza concluída com sucesso! Total de canais salvos: {len(filtered_playlist) // 2}")
