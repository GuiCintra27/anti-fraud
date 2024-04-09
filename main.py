from extract_csv_data import extractCsvData
from sheets_api import pushToSheets
from risk_analysis import riskAnalysis
from class_to_list import classToList as cla

rows, Indexes, cards, users = extractCsvData("data.csv")

if len(rows) == 0:
    print("Não foram encontrados dados na base de dados.")

else:
    print(f"Total de transações encontradas: {len(rows)}")

    print("Iniciando análise de risco")
    suspectUsers, suspectCards, suspectUsersDic, suspectCardsDic = riskAnalysis(
        rows, Indexes, cards, users)
    print("Análise concluída")

    # retry = 0
    # try:
    #     print("Iniciando login no google sheets")
    #     pushToSheets(rows, Indexes,
    #                  cla(suspectUsers), suspectUsersDic, cla(suspectCards), suspectCardsDic)

    # except Exception as e:
    #     if retry < 3:
    #         retry += 1
    #         print(
    #             f"Erro ao realizar operação. Tentativa {retry} de 3")
    #         pushToSheets(rows, Indexes,
    #                      cla(suspectUsers), suspectUsersDic, cla(suspectCards), suspectCardsDic)
    #     else:
    #         print("Erro ao realizar operação")
    #         print(e)
