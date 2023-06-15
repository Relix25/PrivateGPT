import gspread
from gspread.exceptions import WorksheetNotFound


class SpreadsheetManager:
    def __init__(
      self,
      spreadsheet_key: str,
      question: str,
      answer: str,
      source: str,
      time: int,
      start_from: int,
      end_at: int,
      tab: int,
    ) -> None:
        self.spreadsheet_key = spreadsheet_key
        # questions column letter
        self.question = question
        # answers column letter
        self.answer = answer
        # ditto
        self.source = source
        # ditto
        self.time = time

        # worksheet index
        self.tab = tab

        # starting row
        self.start_from = start_from
        # final row
        self.end_at = end_at
        self.gc = None
        self.sheet = None

    def authenticate(self) -> None:
        self.gc = gspread.service_account(filename='credential.json')
        self.spreadsheet = self.gc.open_by_key(self.spreadsheet_key)
        self.sheet = self.spreadsheet.get_worksheet(self.tab)

    def get_questions(self):
      # generator yielding questions values
      for i in range(self.start_from, self.end_at + 1):
        yield self.sheet.acell(f"{self.question}{i}").value

    def send_answer(self, question_index: int, answer, source, time) -> None:
        current_row = self.start_from + question_index  # + 1

        cell_answer = f"{self.answer}{current_row}"
        cell_source = f"{self.source}{current_row}"
        cell_time = f"{self.time}{current_row}"

        self.sheet.update(cell_answer, answer)
        self.sheet.update(cell_source, source)
        self.sheet.update(cell_time, time)
