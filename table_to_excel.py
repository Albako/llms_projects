from openpyxl import Workbook

# markdown_table = """
# | Name    | Age | Occupation    | Favorite Hobby   |
# |---------|-----|---------------|------------------|
# | Alice   | 28  | Engineer      | Paiting          |
# | Bob     | 35  | Doctor        | Cycling          |
# | Charlie | 42  | Teacher       | Hiking           |
# | David   | 30  | Photographer  | Chess            |"""

def create_excel(markdown_table, excel_file_name):

    rows = markdown_table.split("\n")
    spreadsheet=[]
    for index,row in enumerate(rows):
        if index==1:
            continue
        split_rows = row.split("|")
        spreadsheet.append(split_rows[1:-1]) # skip first & last element

    wb = Workbook()
    ws = wb.active

    for row in spreadsheet:
        ws.append(row)
        
    wb.save(f"{excel_file_name}.xlsx")
    print("Table saved succsesfully")