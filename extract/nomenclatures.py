import pandas as pd


class NomenclaturesFile:
    """Данные из справочника номенклатур"""

    def get_nomenclatures(self) -> dict:
        columns = [
            "Маркетплейс",
            "Артикул НАШ на площадке",
            "Тип изделия",
            "Наименование позиции",
            "Универсальный артикул",
        ]
        file_path = "extract/Справочник номенклатур.xlsx"
        df = pd.read_excel(file_path, usecols=columns)
        result = {}
        for i in zip(df[columns[0]], df[columns[1]], df[columns[2]], df[columns[3]], df[columns[4]]):
            result[i[1]] = {"Маркетплейс": i[0], "Группа": i[2], "Название товара": i[3], "Универсальный артикул": i[4]}
        return result
