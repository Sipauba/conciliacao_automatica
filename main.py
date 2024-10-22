import cv2
import pyautogui
import numpy as np
import pytesseract
import time
from PIL import ImageGrab
import re

# Aguarda 3 segundos até iniciar o programa
time.sleep(5)

# Cria duas variáveis com as dimensões da tela
largura_tela, altura_tela = pyautogui.size()

# Carrega a imagem que eu preciso encontrar na tela
campo_dt_compensacao = cv2.imread('dt-compensacao.png',0)

# Tira um print da tela para analisar
print_tela = pyautogui.screenshot()

# Converte o print para um formato que a biblioteca OpenCV reconhece
print_tela_np = np.array(print_tela)
print_tela_gray = cv2.cvtColor(print_tela_np, cv2.COLOR_BGR2GRAY)

# Aplica a correspondência do template
res = cv2.matchTemplate(print_tela_gray, campo_dt_compensacao, cv2.TM_CCOEFF_NORMED)

# Define uma tolerância para considerar a imagem como correta
tolerancia = 0.8
loc = np.where(res >= tolerancia)

# Se encontrar a imagem, salva as coordenadas
if len(loc[0]) > 0:
    # Pega a primeira correspondência (caso tenha mais de uma, ajusta conforme necessário)
    pt = list(zip(*loc[::-1]))[0]
    
    # Calcula o centro da imagem encontrada 
    centro_x_campo_dt_compensacao = pt[0] + campo_dt_compensacao.shape[1] // 2
    centro_y_campo_dt_compensacao = pt[1] + campo_dt_compensacao.shape[0] // 2
    
    pyautogui.moveTo(centro_x_campo_dt_compensacao,centro_y_campo_dt_compensacao)
    
    print(f"Altura da tela: {altura_tela}, Largura da tela: {largura_tela}")
    
    print(f"Campo Data de Compensação identificado. Posição armazenada. X:{centro_x_campo_dt_compensacao}, Y:{centro_y_campo_dt_compensacao}")

else:
    print("Campo Data de Compensação não identificado.")
    
# Define o caminho para o Tesseract no sistema
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Expressão regular para identificar as datas (dd-mm-yyyy, dd.mm.yyyy, dd/mm/yyyy)
padrao_data = r'\b\d{2}[-./]\d{2}[-./]\d{4}\b'


# Muito provavelmente vou precisar usar um WHILE nessa parte do código

def verificar_datas(): 
    # Essas cordenadas informam onde começa e onde termina a região que será printada(x,y,x,y)
    print_regiao_tela = ImageGrab.grab(bbox=(0, centro_y_campo_dt_compensacao + 50, largura_tela // 2, altura_tela - 100))
    
    opencv_image = cv2.cvtColor(np.array(print_regiao_tela), cv2.COLOR_RGB2BGR)
    
    # Extração de texto e posições com pytesseract
    data = pytesseract.image_to_data(print_regiao_tela, output_type=pytesseract.Output.DICT)

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
                conciliar(x, y, text)

    return encontrou_valido

def conciliar(x, y, data):
    # Preencha com a lógica necessária, por exemplo, clicar na posição da data
    print(f"Executando ação na data: {data}, posição: ({x}, {y})")
    
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
