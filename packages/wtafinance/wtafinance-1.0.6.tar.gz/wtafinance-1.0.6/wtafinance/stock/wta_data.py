from wtafinance.finance_api import stock,filedata_source_process


def wta_api(secret_key,secret_id):
    instance = stock.DataApi(secret_key,secret_id)
    return instance


def wta_file(RootPath):
    instance = filedata_source_process.MianClass(RootPath)
    return instance