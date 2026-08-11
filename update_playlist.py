import urllib.request

# URLs oficiais usadas pelo projeto iptv-org
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

# Termos essenciais para abranger todo o esporte nacional e canais fechados populares
include_keywords = [
    "sport",
    "espn",
    "bandsports",
    "premiere",
    "combate",
    "conmebol",
    "f1",
    "sportv",
    "tnt",
    "gazeta esportiva",
    "paramount",
    "cazetv",
    "nsports",
    "fifa+",
    "ge fast",
    "futebol",
]

# Termos para bloquear conteúdos estrangeiros ou indesejados que não têm relação com o Brasil
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
    # Bloqueia idiomas estrangeiros comuns que poluem a lista global de esportes:
    "russia",
    "ukraine",
    "greek",
    "cyprus",
    "pk sports",
    "india",
    "arab",
    "turkey",
    "polish",
    "hungary",
    "romania",
    "czech",
    "vietnam",
    "china",
]

filtered_playlist = ["#EXTM3U\n"]
save_next = False
current_inf = ""
added_links = set()

for line in lines:
  if line.startswith("#EXTINF:"):
    line_lower = line.lower()

    is_excluded = any(ex in line_lower for ex in exclude_keywords)
    is_included = any(inc in line_lower for inc in include_keywords)

    # Se o canal for do Brasil (tem .br / @br / portuguese) OU se for um canal fechado
    # global importante (como Premiere, TNT Sports, ESPN) que queremos capturar:
    is_target_channel = (
        "br" in line_lower
        or "portuguese" in line_lower
        or "premiere" in line_lower
        or "tnt" in line_lower
        or "espn" in line_lower
        or "sportv" in line_lower
        or "combate" in line_lower
        or "bandsports" in line_lower
        or "cazetv" in line_lower
    )

    if is_included and not is_excluded and is_target_channel:
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

# Salva o resultado atualizado
with open("br-sports.m3u", "w", encoding="utf-8") as f:
  f.writelines(filtered_playlist)

print(
    f"Playlist ajustada com sucesso! Total de canais salvos:"
    f" {len(filtered_playlist)}"
)
