import requests
import pandas as pd
from io import BytesIO

def capturar_base_de_dados( url_de_download: str ):

  response = requests.get( url_de_download )

  if( response.status_code != 200 ):
    raise Exception( 'Falha ao baixar a planilha' )

  return pd.read_excel(
    BytesIO( response.content )
  )