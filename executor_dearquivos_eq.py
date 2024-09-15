from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Função para esperar até que um novo arquivo apareça no diretório de downloads
def wait_for_downloads(download_dir, timeout=30):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(download_dir):
            if fname.endswith('.crdownload'):  # Arquivo temporário de download do Chrome
                dl_wait = True
        seconds += 1
    return not dl_wait

# Solicita ao usuário para inserir as datas de início e fim
data_inicio = input("Digite a data de início (formato: dd/mm/yyyy): ")
data_fim = input("Digite a data de fim (formato: dd/mm/yyyy): ")

# Configurações do WebDriver
download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
options = Options()
prefs = {'download.default_directory': download_dir}
options.add_experimental_option('prefs', prefs)

# Usando o webdriver_manager para gerenciar o EdgeDriver
service = Service(EdgeChromiumDriverManager().install())
navegador = webdriver.Edge(service=service, options=options)

try:
    # Abre a página de login
    navegador.get('https://portal.professor24h.com.br/#/login')

    # Insere e-mail e senha
    email_input = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
    email_input.send_keys('instituicao@escrevendonaquarentena.org')

    senha_input = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
    senha_input.send_keys('EQinstituicao2022')

    entrar_input = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div/div/div[2]/form/div[3]/div[2]/button')))
    entrar_input.click()

    # Espera até concluir o login
    WebDriverWait(navegador, 10).until(
        EC.url_to_be('https://portal.professor24h.com.br/#/escola/dashboard'))
    
    time.sleep(5)

    menu_opções = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/header/div/div[1]/button[1]')))
    menu_opções.click()

    # Navega para a página de redações
    navlink_redacoes = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div[1]/ul/li[5]/a')))
    navlink_redacoes.click()

    WebDriverWait(navegador, 10).until(
        EC.url_to_be('https://portal.professor24h.com.br/#/redacoes'))

    # Insere as datas de início e fim
    click_datas = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/main/div/div[1]/div/div/form/div/div[1]/div/div[2]/div/span/span/span')))
    click_datas.click()

    data_inicio_input = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div/input')))
    data_inicio_input.send_keys(data_inicio)

    data_fim_input = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/input')))
    data_fim_input.send_keys(data_fim)

    # Realiza a busca
    busca = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/main/div/div[1]/div/div/form/div/div[2]/button')))
    busca.click()

    # Seleciona todas as redações
    check = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/main/div/div[1]/div/div/div[3]/div[3]/div[1]/div[3]/div/div/div/div/div/div/table/thead/tr/th[1]/span/div/span[1]/label/span[1]/input')))
    check.click()

    # Exporta para CSV
    botao_csv = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/main/div/div[1]/div/div/div[3]/div[3]/div[1]/div[2]/div[2]/button')))
    botao_csv.click()

    baixar_csv = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/ul/li[3]/a')))
    baixar_csv.click()

    # Espera até que o arquivo seja baixado
    if wait_for_downloads(download_dir):
        print("Arquivo baixado com sucesso! :)")
        file_path = os.path.join(download_dir, 'nome_do_arquivo.csv')  # Substitua pelo nome correto do arquivo
        folder_id = '1kXgLV3bHPPeVp-qhh8w_bjMdxGfYaVrK'  # Substitua pelo ID da pasta no Google Drive

        # Faz o upload para o Google Drive
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = service_account.Credentials.from_service_account_file('credential.json', scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': 'nome_do_arquivo.csv', 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='text/csv')

        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'Arquivo enviado para o Google Drive com ID: {file.get("id")}')

    else:
        print("Tempo de espera esgotado. O arquivo não foi baixado. :(")

    time.sleep(20)

except Exception as e:
    print('Erro:', e)

finally:
    navegador.quit()
