from src.robo import start
from dotmap import DotMap
import sys
import json

def main():

  ambiente = 'producao'
  
  if len( sys.argv ) == 2 and sys.argv[1] != 'desenvolvimento':
    sys.exit( 1 )

  if len( sys.argv ) == 2:
    ambiente = sys.argv[1]

  parametrizacao = None

  with open( f"./src/{ambiente}.json" ) as env:
    parametrizacao = DotMap( json.load( env ) )

  start( parametrizacao )

if __name__ == '__main__':
  main()