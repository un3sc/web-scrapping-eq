# WEB SCRAPPING EQ

Este projeto é um script Python que automatiza o processo de download de arquivos usando o Selenium com o navegador Edge e faz o upload desses arquivos para o Google Drive utilizando a Google Drive API.

## Funcionalidades

- Utiliza o Selenium para gerenciar o navegador Edge e realizar downloads.
- Espera até que o download seja concluído antes de continuar.
- Faz upload automático dos arquivos baixados para o Google Drive.
  
## Pré-requisitos

- [Python 3.x](https://www.python.org/downloads/)
- [Selenium](https://www.selenium.dev/)
- [WebDriver Manager](https://pypi.org/project/webdriver-manager/)
- [Google API Client](https://googleapis.dev/python/google-api-core/latest/index.html)

## Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure suas credenciais do Google Drive:

   - Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
   - Ative a API do Google Drive.
   - Baixe o arquivo `credentials.json` e coloque na pasta do projeto.

## Como usar

1. Execute o script:

   ```bash
   python executor_dearquivos_eq.py
   ```

2. O script abrirá o navegador Edge, fará o download dos arquivos e os carregará automaticamente no Google Drive.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request.

---

Este README oferece uma descrição clara do propósito do script, como instalá-lo e como usá-lo. Se precisar de mais detalhes ou ajustes, é só avisar!
 
