import re
from PIL import ImageGrab
import pytesseract
import pyautogui

# Defina o caminho para o Tesseract no sistema
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajuste o caminho no seu sistema

# Expressão regular para identificar as datas (dd-mm-yyyy, dd.mm.yyyy, dd/mm/yyyy)
padrao_data = r'\b\d{2}[-./]\d{2}[-./]\d{4}\b'

# Capture uma área da tela (ajuste o bbox conforme necessário)
screenshot = ImageGrab.grab(bbox=(100, 100, 800, 600))  # Área de captura da tela

# Use pytesseract para obter os dados com as posições de cada palavra
data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

# Variáveis para armazenar as coordenadas da data encontrada
x, y, w, h = None, None, None, None

# Percorre o texto extraído e verifica se o padrão de data está presente
for i in range(len(data['text'])):
    if re.search(padrao_data, data['text'][i]):
        # Se uma data for encontrada, captura as coordenadas
        x = data['left'][i] + 100  # Adiciona o offset da posição da captura (100, 100)
        y = data['top'][i] + 100
        w = data['width'][i]
        h = data['height'][i]
        print(f'Data encontrada: {data["text"][i]} nas coordenadas: ({x}, {y})')
        break

# Se a data foi encontrada, move o mouse para a posição
if x and y:
    # Calcula a posição central da data
    x_centro = x + w // 2
    y_centro = y + h // 2

    # Move o mouse para o centro da data
    pyautogui.moveTo(x_centro, y_centro)
    print(f'O mouse foi movido para a data.')
else:
    print(f'Nenhuma data encontrada com o padrão {padrao_data}.')
