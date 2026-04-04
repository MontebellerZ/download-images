import json
import time
import webbrowser
import pyautogui
import os

# Configurações
TEMPO_CARREGAMENTO = 1
TEMPO_SALVAR = 1

CLICKS = [
    {"x": 1890, "y": 154, "t": 0.2},
    {"x": 1600, "y": 120, "t": 1, "img": "adicionar-album.png", "region": (320, 480)},
    {"x": 916, "y": 602, "t": 1},
]

# ------------------ ARQUIVOS ------------------

def carregar_json(nome_arquivo):
    if not os.path.exists(nome_arquivo):
        return []
    with open(nome_arquivo, "r") as f:
        return json.load(f)

def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, "w") as f:
        json.dump(dados, f, indent=2)

# ------------------ AUTOMAÇÃO ------------------

def executar_cliques():
    for click in CLICKS:
        time.sleep(click["t"])

        if "img" not in click:
            pyautogui.click(click["x"], click["y"])
            continue

        x, y = click["x"], click["y"]
        dx, dy = click["region"]

        pos = pyautogui.locateOnScreen(
            click["img"],
            confidence=0.7,
            region=(x, y, dx, dy)
        )

        if not pos:
            raise Exception(f'Imagem não encontrada: {click["img"]}')

        xPos, yPos = pyautogui.center(pos)
        pyautogui.click(xPos, yPos)

def fechar_navegador():
    pyautogui.hotkey('ctrl', 'w')

# ------------------ MAIN ------------------

def main():
    links = carregar_json("links.json")
    feitos = carregar_json("feitos.json")

    print("Iniciando em 5 segundos...")
    time.sleep(5)

    i = 0
    while i < len(links):
        url = links[i]
        print(f"Abrindo {i+1}/{len(links)}: {url}")

        try:
            webbrowser.open(url)

            time.sleep(TEMPO_CARREGAMENTO)

            executar_cliques()

            time.sleep(TEMPO_SALVAR)

            fechar_navegador()

            # ✅ SUCESSO → move o link
            feitos.append(url)
            links.pop(i)

            salvar_json("feitos.json", feitos)
            salvar_json("links.json", links)

            print(f"✔ Sucesso: {url}")

        except Exception as e:
            print(f"❌ Erro no link {url}: {e}")
            i += 1  # só avança se deu erro

    print("Finalizado!")

if __name__ == "__main__":
    main()