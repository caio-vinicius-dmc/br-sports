import urllib.request

# URL oficial da lista de canais do Brasil no projeto iptv-org
url_br = "https://iptv-org.github.io/iptv/countries/br.m3u"

print("Baixando lista do Brasil...")
req = urllib.request.urlopen(url_br)
lines = [line.decode("utf-8") for line in req.readlines()]

# Palavras-chave para identificar canais de esportes brasileiros
keywords = [
    "sport",
    "espn",
    "bandsports",
    "premiere",
    "combate",
    "conmebol",
    "f1",
    "sportv",
    "gazeta esportiva",
    "paramount",
]

filtered_playlist = ["#EXTM3U\n"]
save_next = False
current_inf = ""

for line in lines:
  if line.startswith("#EXTINF:"):
    # Verifica se alguma palavra-chave está presente no título/metadados do canal
    if any(keyword in line.lower() for keyword in keywords):
      save_next = True
      current_inf = line
    else:
      save_next = False
  elif save_next:
    if line.startswith("http"):
      filtered_playlist.append(current_inf)
      filtered_playlist.append(line)
    save_next = False

# Salva o resultado filtrado em um novo arquivo m3u
with open("br-sports.m3u", "w", encoding="utf-8") as f:
  f.writelines(filtered_playlist)

print(
    f"Playlist gerada com sucesso! Total de linhas salvas:"
    f" {len(filtered_playlist)}"
)
