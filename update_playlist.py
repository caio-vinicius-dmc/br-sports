import urllib.request

# URLs oficiais: Lista do Brasil E a lista global de esportes do iptv-org
urls = [
    "https://iptv-org.github.io/iptv/countries/br.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
]

lines = []
for url in urls:
  print(f"Baixando fonte: {url}")
  try:
    req = urllib.request.urlopen(url)
    lines.extend([line.decode("utf-8") for line in req.readlines()])
  except Exception as e:
    print(f"Erro ao baixar {url}: {e}")

# Palavras-chave para incluir canais de esporte (incluindo variações do Premiere)
include_keywords = [
    "sport",
    "espn",
    "bandsports",
    "premiere",
    "combate",
    "conmebol",
    "f1",
    "sportv",
    "tnt sports",
    "gazeta esportiva",
    "paramount",
    "cazetv",
    "nsports",
    "fifa+",
    "ge fast",
]

# Termos bloqueados para evitar conteúdo indesejado (filmes, séries, etc.)
exclude_keywords = [
    "smithsonian",
    "voyager",
    "jornada nas estrelas",
    "pluto tv",
    "comedy central",
    "filmes",
    "mtv",
    "nickelodeon",
    "nick jr",
]

filtered_playlist = ["#EXTM3U\n"]
save_next = False
current_inf = ""
added_links = (
    set()
)  # Para evitar canais duplicados caso apareçam nas duas listas

for line in lines:
  if line.startswith("#EXTINF:"):
    line_lower = line.lower()
    is_excluded = any(ex in line_lower for ex in exclude_keywords)
    is_included = any(inc in line_lower for inc in include_keywords)

    if is_included and not is_excluded:
      save_next = True
      current_inf = line
    else:
      save_next = False
  elif save_next:
    if line.startswith("http"):
      if line not in added_links:  # Evita duplicidade
        filtered_playlist.append(current_inf)
        filtered_playlist.append(line)
        added_links.add(line)
    save_next = False

# Salva o arquivo final atualizado
with open("br-sports.m3u", "w", encoding="utf-8") as f:
  f.writelines(filtered_playlist)

print(
    f"Playlist combinada e gerada com sucesso! Total de linhas:"
    f" {len(filtered_playlist)}"
)
