import urllib.request

# URLs oficiais: Mantemos as duas fontes para não perder os canais fechados
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

# Palavras-chave estritas de esporte
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

# Termos bloqueados (lixo, filmes, mtv, etc.)
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
added_links = set()

for line in lines:
  if line.startswith("#EXTINF:"):
    line_lower = line.lower()

    # FILTRAGEM DE NACIONALIDADE:
    # O canal DEVE pertencer ao Brasil (.br, @br, ou ter menções claras ao Brasil/Português do Brasil)
    # Exceção feita para canais globais como CazeTV ou FIFA+ em português se desejado,
    # mas focamos nas tags oficiais do iptv-org que identificam o país.
    is_brazil = (
        ".br" in line_lower
        or "@br" in line_lower
        or "portuguese" in line_lower
        or " brazil" in line_lower
    )

    # Se a linha veio da lista de esportes global, precisamos ser rigorosos se ela é brasileira.
    # (A lista do br.m3u inteira já é do Brasil, mas a sports.m3u mistura o mundo todo).
    # Vamos validar se tem esporte, se não é excluído e se é do Brasil.
    is_excluded = any(ex in line_lower for ex in exclude_keywords)
    is_included = any(inc in line_lower for inc in include_keywords)

    # Se veio do arq do Brasil (br.m3u) ou se passou no crivo de nacionalidade na lista global:
    if is_included and not is_excluded and is_brazil:
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

# Salva o arquivo final limpo
with open("br-sports.m3u", "w", encoding="utf-8") as f:
  f.writelines(filtered_playlist)

print(
    f"Playlist 100% brasileira gerada com sucesso! Total de linhas:"
    f" {len(filtered_playlist)}"
)
