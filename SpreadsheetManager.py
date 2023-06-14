"""import gspread

gc = gspread.service_account()

sh = gc.open_by_key("1R10Z_F1Nh8HSzcnms1MtIIAaEgazXpBm22ZAjAruyGs")

name = 'WizardLM'
template_name = 'Template'

# Check if the worksheet already exists
worksheet_exists = False
for worksheet in sh.worksheets():
    if worksheet.title == name:
        worksheet_exists = True
        break

# If the worksheet doesn't exist, create it
if not worksheet_exists:
    template_worksheet = sh.worksheet(template_name)
    new_worksheet = template_worksheet.duplicate(insert_sheet_index=1, new_sheet_name=name)
    print(f"Worksheet '{name}' created successfully by copying '{template_name}'!")
else:
    print(f"Worksheet '{name}' already exists.")

# sh.share('<EMAIL>', perm_type='user', role='writer')"""

import gspread
from gspread.exceptions import WorksheetNotFound


class SpreadsheetManager:
    def __init__(self, spreadsheet_key) -> None:
        self.spreadsheet_key = spreadsheet_key
        self.gc = None
        self.sh = None

    def authenticate(self) -> None:
        self.gc = gspread.service_account(filename='credential.json')
        self.sh = self.gc.open_by_key(self.spreadsheet_key)

    def create_worksheet(self, name) -> str:
        global worksheet
        template_name = "Template"
        worksheet_exists = False
        try:
            worksheet = self.sh.worksheet(name)
            worksheet_exists = True
        except WorksheetNotFound:
            pass

        if not worksheet_exists:
            template_worksheet = self.sh.worksheet(template_name)
            new_worksheet = template_worksheet.duplicate(insert_sheet_index=1, new_sheet_name=name)
            print(f"Worksheet '{name}' created successfully by copying '{template_name}'!")
            return new_worksheet
        else:
            print(f"Worksheet '{name}' already exists.")
            return worksheet

    def send_answer(self, question, answer, name) -> None:
        # Get the current value in A1 and increment it by 1
        current_row = int(self.sh.worksheet(name).get('A2').first()) + 1

        # Put the question in B2, the answer in C2 (or in the corresponding columns)
        cell_question = f"B{current_row}"
        cell_answer = f"C{current_row}"
        self.sh.worksheet(name).update(cell_question, question)
        self.sh.worksheet(name).update(cell_answer, answer)

        # Update the value in A1 with the new row position
        self.sh.worksheet(name).update("A2", current_row)
