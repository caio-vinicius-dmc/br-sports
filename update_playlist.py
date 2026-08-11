import urllib.request

# URL oficial da lista de canais do Brasil no projeto iptv-org
url_br = "https://iptv-org.github.io/iptv/countries/br.m3u"

print("Baixando lista do Brasil...")
req = urllib.request.urlopen(url_br)
lines = [line.decode("utf-8") for line in req.readlines()]

# Palavras-chave estritas para canais de esporte no Brasil (incluindo Premiere, TNT Sports, etc.)
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

# Termos que devem ser BLOQUEADOS caso apareçam (para limpar filmes, séries, pluto tv indesejada, etc.)
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

for line in lines:
  if line.startswith("#EXTINF:"):
    line_lower = line.lower()

    # Verifica se tem alguma palavra proibida
    is_excluded = any(ex in line_lower for ex in exclude_keywords)

    # Verifica se tem alguma palavra de esporte desejada
    is_included = any(inc in line_lower for inc in include_keywords)

    if is_included and not is_excluded:
      save_next = True
      current_inf = line
    else:
      save_next = False
  elif save_next:
    if line.startswith("http"):
      filtered_playlist.append(current_inf)
      filtered_playlist.append(line)
    save_next = False

# Salva o resultado refinado
with open("br-sports.m3u", "w", encoding="utf-8") as f:
  f.writelines(filtered_playlist)

print(f"Playlist refinada com sucesso! Total de linhas: {len(filtered_playlist)}")
