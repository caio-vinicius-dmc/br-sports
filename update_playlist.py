import urllib.request
import re

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

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # 1. É canal de esportes?
        is_sport = (
            'group-title="sports"' in line_lower or 
            "sport" in line_lower or 
            "futebol" in line_lower or 
            "combate" in line_lower
        )
        
        # 2. Tem as tags oficiais do Brasil do iptv-org?
        is_br_tag = ".br@" in line_lower or '.br"' in line_lower or "@portuguese" in line_lower
        
        # 3. Tem o nome das marcas brasileiras? 
        # O uso do \b (word boundary) impede que "nsports" dê match dentro de "winsports"
        is_br_marca = bool(re.search(r'\b(cazetv|premiere|sportv|combate|tnt|bandsports|ge fast|nsports|canal do inter)\b', line_lower))
        
        if is_sport and (is_br_tag or is_br_marca):
            # Filtro extra de segurança para matar canais do exterior que podem ter burlado as regras acima
            is_foreign = re.search(r'tvg-id="[^"]+\.(us|uk|co|bh|tr|sk|ge|bj|fr|iq|cy|qa|ma|ve|sv|mx|ar|az|cn|do|au|cl|cz|hn|ua|vn|dz|gr|nl|dk|ca|ie|cr)\b', line_lower)
            
            if is_foreign and not is_br_tag:
                save_next = False
            else:
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
# INJEÇÃO MANUAL DE CANAIS FECHADOS (PREMIERE, TNT, ETC)
# Como o iptv-org exclui esses canais por direitos autorais,
# você adiciona eles aqui. Substitua os links abaixo pelos seus links reais.
# =====================================================================
canais_premium = """#EXTINF:-1 tvg-id="Premiere.br" group-title="Sports",Premiere
http://COLE_AQUI_O_SEU_LINK_DO_PREMIERE.m3u8
#EXTINF:-1 tvg-id="TNTSports.br" group-title="Sports",TNT Sports
http://COLE_AQUI_O_SEU_LINK_DA_TNT.m3u8
"""

filtered_playlist.append(canais_premium)

# Salva o arquivo final
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Limpeza concluída! Total de canais salvos: {len(filtered_playlist) // 2}")
