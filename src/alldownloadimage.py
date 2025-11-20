import requests
from bs4 import BeautifulSoup
import os

# URL da pasta de sprites desejada
url = "DIGITE_A_URL_AQUI"
# Pasta local para salvar os arquivos
save_dir = "DIR_DESTINO"

# Cria a pasta se não existir
os.makedirs(save_dir, exist_ok=True)

# Faz a requisição da página
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# Percorre todos os links da página
for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.endswith(".gif"):
        gif_url = url + href  # Monta a URL completa
        filename = os.path.join(save_dir, href)  # Caminho local para salvar

        print(f"Baixando {href}...")
        try:
            with requests.get(gif_url, stream=True) as r:
                r.raise_for_status()  # Garante que o download falhará em caso de erro HTTP
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except Exception as e:
            print(f"Erro ao baixar {href}: {e}")

print("Download concluído!")
