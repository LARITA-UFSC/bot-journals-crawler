from helpers import crawling


INFORMACAO_E_SOCIEDADE = 1
TRANSINFORMACAO = 2
PERSPECTIVAS_EM_CIENCIAS_DA_INFORMACAO = 3

# https://github.com/LARITA-UFSC/bot-periodicos-capes-ci/issues/6
# 32999
crawling('http://www.ies.ufpb.br/ojs2/index.php/ies/', [doc for doc in range(7000, )], INFORMACAO_E_SOCIEDADE)

# https://github.com/LARITA-UFSC/bot-periodicos-capes-ci/issues/4
# crawling('http://periodicos.puc-campinas.edu.br/seer/index.php/transinfo/', [doc for doc in range(1, 2645)], TRANSINFORMACAO)

# crawling('http://portaldeperiodicos.eci.ufmg.br/index.php/pci/',
#          [doc for doc in range(1, 2702)], PERSPECTIVAS_EM_CIENCIAS_DA_INFORMACAO)
