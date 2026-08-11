import urllib.request
import re

# Usamos a categoria global de esportes combinada com a do Brasil
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

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # Pega tudo o que é esporte ou contenha marcas esportivas globais e nacionais
        is_sport = 'group-title="sports"' in line_lower or "sport" in line_lower or "futebol" in line_lower
        
        # Garante a captura de redes de esporte e variações de premiere/tnt esportes
        has_target = bool(re.search(r'\b(sportv|espn|premiere|tnt|combate|bandsports|cazetv|nsports|ge fast|futebol|fox sports|paramount)\b', line_lower))
        
        # Filtra para trazer o Brasil e canais de esporte gerais úteis
        is_br = 'tvg-country="br"' in line_lower or '.br"' in line_lower or '.br@' in line_lower or 'portuguese' in line_lower
        
        if is_sport or has_target or is_br:
            save_next = True
            current_inf = line
        else:
            save_next = False
            
    elif save_next:
        if line.startswith("http"):
            if line not in added_links:
                filtered_playlist.append(current_inf)
                filtered_playlist.append(line)
                added_links.add(line)
        save_next = False

# =====================================================================
# INJEÇÃO AUTOMÁTICA DOS SEUS CANAIS DE PREMIERE E TNT ESPORTES
# Como o GitHub remove canais pagos das listas públicas por DMCA,
# coloque os seus links funcionais aqui embaixo. O robô vai embutir
# eles na sua playlist todos os dias de forma automatizada.
# =====================================================================
canais_extras_obrigatorios = """
#EXTINF:-1 tvg-id="PremiereClube.br" group-title="Sports",Premiere (Futebol Nacional)
http://SEU_LINK_DO_PREMIERE_AQUI.m3u8
#EXTINF:-1 tvg-id="TNTSports.br" group-title="Sports",TNT Sports Brasil
http://SEU_LINK_DA_TNT_SPORTS_AQUI.m3u8
"""

filtered_playlist.append(canais_extras_obrigatorios)

# Salva o arquivo final no repositório
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Processo finalizado! Total de canais gerados: {len(filtered_playlist) // 2}")
