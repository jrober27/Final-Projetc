from vote_gui import *
import csv
from PyQt6.QtWidgets import *


class Logic:
    def __init__(self, ui):
        self.ui = ui
        # Connect the submit button
        self.ui.SubmitVote.clicked.connect(self.save)
        # Hide all status messages initially
        self._hide_messages()

    def _hide_messages(self):
        self.ui.AlreadyVotedText.hide()
        self.ui.Vali_id_text.hide()
        self.ui.Vote_submitted_txt.hide()
        self.ui.Select_candidate_text.hide()

    def save(self):
        self._hide_messages()
        voter_id = self.ui.IDinput.text().strip()
        candidate = None
        if self.ui.JohnButton.isChecked():
            candidate = "John"
        elif self.ui.JaneButton.isChecked():
            candidate = "Jane"

        # Valid
        if not (len(voter_id) == 8 and voter_id.isdigit()):
            self.ui.Vali_id_text.show()
            self._clear_inputs()
            return

        if candidate is None:
            self.ui.Select_candidate_text.show()
            self._clear_inputs()
            return

        if self._has_voted(voter_id):
            self.ui.AlreadyVotedText.show()
            self._clear_inputs()
            return

        # Save vote
        with open("votergui.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([voter_id, candidate])

        self.ui.Vote_submitted_txt.show()
        self._clear_inputs()

    def _has_voted(self, voter_id: str) -> bool:
        try:
            with open("votergui.csv", "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0] == voter_id:
                        return True
        except FileNotFoundError:
            return False
        return False

    def _clear_inputs(self):
        """Clear all input fields and reset candidate selection."""
        self.ui.IDinput.clear()
        self.ui.JohnButton.setAutoExclusive(False)
        self.ui.JaneButton.setAutoExclusive(False)
        self.ui.JohnButton.setChecked(False)
        self.ui.JaneButton.setChecked(False)
        self.ui.JohnButton.setAutoExclusive(True)
        self.ui.JaneButton.setAutoExclusive(True)
