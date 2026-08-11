import urllib.request

# URL oficial da lista de canais do Brasil no projeto iptv-org
url_br = "https://iptv-org.github.io/iptv/countries/br.m3u"

print("Baixando lista oficial do Brasil...")
try:
    req = urllib.request.urlopen(url_br)
    lines = [line.decode("utf-8") for line in req.readlines()]
except Exception as e:
    print(f"Erro ao baixar a lista: {e}")
    lines = []

# Palavras-chave para identificar canais de esportes brasileiros na lista
include_keywords = [
    "sport",
    "espn",
    "bandsports",
    "combate",
    "conmebol",
    "f1",
    "gazeta esportiva",
    "paramount",
    "cazetv",
    "nsports",
    "fifa+",
    "ge fast",
    "futebol",
]

# Termos para bloquear conteúdos que não são de esporte
exclude_keywords = [
    "filmes",
    "series",
    "comedy",
    "desenho",
    "gospel",
    "noticias",
    "jornal",
]

filtered_playlist = ["#EXTM3U\n"]
save_next = False
added_links = set()

for line in lines:
    if line.startswith("#EXTINF:"):
        line_lower = line.lower()
        
        # Verifica se o canal é da categoria de esportes ou contém termos esportivos
        is_sports_group = 'group-title="sports"' in line_lower
        has_keyword = any(keyword in line_lower for keyword in include_keywords)
        is_excluded = any(exclude in line_lower for exclude in exclude_keywords)
        
        if (is_sports_group or has_keyword) and not is_excluded:
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
# ÁREA DE CANAIS MANUAIS (Opcional)
# Como o iptv-org não indexa Premiere e TNT abertos, você pode colá-los aqui:
# =====================================================================
canais_manuais = """#EXTINF:-1 tvg-id="Premiere.br" group-title="Sports",Premiere (1080p)
#COLOQUE_SEU_LINK_DO_PREMIERE_AQUI
#EXTINF:-1 tvg-id="TNTSports.br" group-title="Sports",TNT Sports (1080p)
#COLOQUE_SEU_LINK_DO_TNT_AQUI
"""

# Se quiser ativar os manuais, basta descomentar a linha abaixo:
# filtered_playlist.append(canais_manuais)

# Salva o resultado final no arquivo m3u que o seu GitHub vai hospedar
with open("br-sports.m3u", "w", encoding="utf-8") as f:
    f.writelines(filtered_playlist)

print(f"Playlist gerada com sucesso! Total de linhas salvas: {len(filtered_playlist)}")
