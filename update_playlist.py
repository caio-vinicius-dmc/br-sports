import urllib.request

# Usamos APENAS a lista oficial do Brasil, garantindo zero conteúdo estrangeiro
url_br = "https://iptv-org.github.io/iptv/countries/br.m3u"

print("Baixando lista oficial do Brasil...")
req = urllib.request.urlopen(url_br)
lines = [line.decode("utf-8") for line in req.readlines()]

# Palavras-chave amplas para capturar tudo que é esporte ou canais esportivos no Brasil
include_keywords = [
    "sport",
    "espn",
    "bandsports",
    "premiere",
    "combate",
    "conmebol",
    "f1",
    "tnt",
    "gazeta esportiva",
    "paramount",
    "cazetv",
    "nsports",
    "fifa+",
    "ge fast",
    "futebol",
]

# Exclui termos que não são de esporte e que possam vir na lista do Brasil
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
current_inf = ""

for line in lines:
  if line.startswith("#EXTINF:"):
    line_lower = line.lower()

    # Verifica se o canal é da categoria de esportes ou se o nome contém alguma palavra-chave esportiva
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
      filtered_playlist.append(current_inf)
      filtered_playlist.append(line)
    save_next = False

# Salva o resultado limpo
with open("br-sports.m3u", "w", encoding="utf-8") as f:
  f.writelines(filtered_playlist)

print(
    f"Playlist nacional filtrada com sucesso! Total de canais:"
    f" {len(filtered_playlist) // 2}"
)
