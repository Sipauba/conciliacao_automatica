import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import re
import time

time.sleep(2)

# Definir o caminho do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajuste o caminho conforme necessário

# Definir a expressão regular para encontrar datas
padrao_data = r'\b\d{2}[-./]\d{2}[-./]\d{4}\b'

# Função a ser executada ao encontrar uma data válida
def funcao_ao_encontrar_data(x, y, data):
    # Preencha com a lógica necessária, por exemplo, clicar na posição da data
    pyautogui.moveTo(x, y)  # Mover o mouse para a posição da data
    #pyautogui.click()  # Clicar na posição da data
    print(f"Executando ação na data: {data}, posição: ({x}, {y})")

# Função para verificar a presença de datas válidas
def verificar_datas():
    # Capturar a tela ou parte dela
    screenshot = ImageGrab.grab(bbox=(100, 100, 800, 600))  # Ajuste o bbox conforme necessário
    opencv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Extração de texto e posições com pytesseract
    data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

    encontrou_valido = False  # Controle para verificar se há datas válidas

    for i in range(len(data['text'])):
        text = data['text'][i]
        if text != "":
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            
            # Verificar se o texto é uma data válida
            if re.match(padrao_data, text):
                print(f"Data encontrada: {text} na posição: ({x}, {y})")
                encontrou_valido = True  # Encontrou uma data válida

                # Chamar a função ao encontrar uma data válida
                funcao_ao_encontrar_data(x, y, text)

    return encontrou_valido

# Função para rolar a tela para baixo
def rolar_tela():
    pyautogui.scroll(-500)  # Rolagem para baixo (-500) ajustável conforme a necessidade

# Loop principal
while True:
    if not verificar_datas():
        print("Nenhuma data válida encontrada, rolando a tela...")
        rolar_tela()
        time.sleep(2)  # Aguardar um tempo para a tela rolar antes de nova verificação
    else:
        print("Processando datas válidas...")
        # Após encontrar e processar uma data, o loop continuará buscando novas datas
