from playwright.sync_api import sync_playwright, Playwright
import time
from src.helper import capturar_base_de_dados

browser = None
page = None

def realizar_home( playwright: Playwright, params ):

  global browser
  global page

  chromium = playwright.chromium
  browser = chromium.launch( headless=params.playwright.headless )
  page = browser.new_page()
  page.goto( params.rpa_challenge.url )

def iniciar_desafio( params ):
  page.get_by_text( params.rpa_challenge.texto_botao_iniciar_desafio, exact=True ).click()

def baixar_massa_de_dados( params ):
  dados_para_trabalhar = capturar_base_de_dados( params.rpa_challenge.url_download_excel )
  return dados_para_trabalhar

def efetuar_inputs_dos_dados( params, dados_para_processar ):

  nome_dos_inputs = dados_para_processar.keys()

  for _, linha in dados_para_processar.iterrows():
    for input in nome_dos_inputs:

      page.evaluate(
        """
          ( [input, valor] ) => {
            document.evaluate(
              `//label[text()="${input.trim()}"]`,
              document, null,
              XPathResult.FIRST_ORDERED_NODE_TYPE, 
            ).singleNodeValue.nextElementSibling.value = valor;
          }
        """,
        [ input, linha[input] ]
      )

    page.get_by_text( params.rpa_challenge.texto_botao_submit, exact=True ).click()
  
  time.sleep( 5 )

def capturar_resultado( params ):
  return page.locator(
    params.rpa_challenge.locator_resultado_final
  ).inner_text()

def start( params ):
  try:
    with sync_playwright() as playwright:

      realizar_home( playwright, params )

      if( not browser or not page ):
        raise Exception( 'Falha ao inicializar navegador' )

      iniciar_desafio( params )
      dados_para_processar = baixar_massa_de_dados( params )
      efetuar_inputs_dos_dados( params, dados_para_processar )
      resultado_final = capturar_resultado( params )

      print("\033[92m" + resultado_final + "\033[0m")

  except Exception as e:
    print( str( e ) )