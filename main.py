from extract_csv_data import extractCsvData
from sheets_api import pushToSheets
from risk_analysis import riskAnalysis

rows, Indexes, cards, users = extractCsvData("data.csv")

if len(rows) == 0:
    print("Não foram encontrados dados na base de dados.")

else:
    print(f"Total de transações encontradas: {len(rows)}")

    print("Iniciando análise de risco")
    suspectUsers, suspectCards = riskAnalysis(rows, Indexes, cards, users)

    try:
        print("Iniciando login no google sheets")
        pushToSheets(rows, Indexes.transaction_amount)

    except Exception as e:
        print("Erro ao realizar operação")
        print(e)
