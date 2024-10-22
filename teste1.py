import cv2
import pyautogui
import numpy as np

# Carrega a imagem que você quer encontrar
template = cv2.imread('dt-compensacao.png', 0)

# Captura uma screenshot da tela
screenshot = pyautogui.screenshot()

# Converte a screenshot para o formato que o OpenCV usa
screenshot_np = np.array(screenshot)
screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

# Aplica a correspondência do template
res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

# Define um limiar para considerar a correspondência
limiar = 0.8
loc = np.where(res >= limiar)

# Se encontrar a imagem, mova o mouse para o centro dela
if len(loc[0]) > 0:
    # Pega a primeira correspondência (caso tenha mais de uma, ajusta conforme necessário)
    pt = list(zip(*loc[::-1]))[0]
    
    # Calcula o centro da imagem encontrada
    center_x = pt[0] + template.shape[1] // 2
    center_y = pt[1] + template.shape[0] // 2
    
    # Move o mouse para o centro da imagem
    pyautogui.moveTo(center_x, center_y)

    print(f"Imagem encontrada! Mouse movido para ({center_x}, {center_y})")
else:
    print("Imagem não encontrada.")
