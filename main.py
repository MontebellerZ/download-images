import json
import time
import webbrowser
import pyautogui

# Configurações
TEMPO_CARREGAMENTO = 1  # segundos para esperar o site abrir
TEMPO_SALVAR = 1  # segundos para esperar o site abrir

# Posições de clique (ajuste para sua tela)
CLICKS = [
    {"x": 1890, "y": 154, "t": 0.2},
    {"x": 1600, "y": 120, "t": 1, "img": "adicionar-album.png", "region": (320, 480)},
    {"x": 916, "y": 602, "t": 1},
]

def carregar_links():
    with open("links.json", "r") as f:
        return json.load(f)

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
    # Fecha aba atual (Ctrl + W)
    pyautogui.hotkey('ctrl', 'w')

def main():
    links = carregar_links()

    print("Iniciando em 5 segundos... (mova o mouse para o canto para abortar)")
    time.sleep(5)

    for i, url in enumerate(links):
        print(f"Abrindo {i+1}/{len(links)}: {url}")
        
        webbrowser.open(url)

        time.sleep(TEMPO_CARREGAMENTO)

        executar_cliques()

        time.sleep(TEMPO_SALVAR)

        fechar_navegador()

    print("Finalizado!")

if __name__ == "__main__":
    main()