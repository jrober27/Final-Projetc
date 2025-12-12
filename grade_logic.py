import csv
import os
from PyQt6.QtWidgets import *
from grade_gui import *

# letter grade logic
def get_letter_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

class GradeController:
    def __init__(self, ui):
        self.ui = ui
        #submit button
        self.ui.submit_Button.clicked.connect(self.save)
        # update score input boxes when attempts changes
        self.ui.Number_of_attempts_input.textChanged.connect(self._update_score_boxes)
        # hide messages and score boxes at start
        self._hide_messages()
        self._hide_score_boxes()

    def _hide_messages(self):
        self.ui.enter_student_name_text.hide()
        self.ui.enter_valid_number_of_attempts_text.hide()
        self.ui.enter_valid_score_text.hide()
        self.ui.Grades_submmitted_text.hide()

    def _hide_score_boxes(self):
        self.ui.Score_one_input.hide()
        self.ui.score_one_text.hide()
        self.ui.score_two_input.hide()
        self.ui.score_two_text.hide()
        self.ui.score_three_input.hide()
        self.ui.score_three_text_2.hide()
        self.ui.score_four_input_2.hide()
        self.ui.score_four_text_3.hide()

    def _update_score_boxes(self):
        text = self.ui.Number_of_attempts_input.text().strip()
        if not text.isdigit():
            self._hide_score_boxes()
            return
        attempts = int(text)
        self._hide_score_boxes()
        if attempts >= 1:
            self.ui.Score_one_input.show()
            self.ui.score_one_text.show()
        if attempts >= 2:
            self.ui.score_two_input.show()
            self.ui.score_two_text.show()
        if attempts >= 3:
            self.ui.score_three_input.show()
            self.ui.score_three_text_2.show()
        if attempts >= 4:
            self.ui.score_four_input_2.show()
            self.ui.score_four_text_3.show()

    def save(self):
        self._hide_messages()

        try:
            name, attempts, scores = self._read_inputs()
        except ValueError:
            return
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Unexpected error: {e}")
            return

        best = max(scores)
        grades = [get_letter_grade(s) for s in scores]

        # summary stats for csv
        highest = max(scores)
        average = sum(scores) / len(scores)

        try:
            self._append_csv("grades.csv", name, attempts, scores, grades,
                             highest, average)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"File error: {e}")
            return

        self.ui.Grades_submmitted_text.show()
        self._clear_inputs()

    def _read_inputs(self):
        # name validation
        name = self.ui.Student_name_input.text().strip()
        if not name or not all(ch.isalpha() or ch.isspace() for ch in name):
            self.ui.enter_student_name_text.show()
            QMessageBox.warning(None, "Invalid Name", "Name must contain only letters and spaces.")
            raise ValueError("bad name")

        # validate attempts
        attempts_text = self.ui.Number_of_attempts_input.text().strip()
        if not attempts_text.isdigit():
            self.ui.enter_valid_number_of_attempts_text.show()
            QMessageBox.warning(None, "Invalid Attempts", "Attempts must be a number between 1 and 4.")
            raise ValueError("bad attempts")
        attempts = int(attempts_text)
        if attempts < 1 or attempts > 4:
            self.ui.enter_valid_number_of_attempts_text.show()
            QMessageBox.warning(None, "Invalid Attempts", "Attempts must be between 1 and 4.")
            raise ValueError("bad attempts")

        # validate scores
        raw_scores = [
            self.ui.Score_one_input.text().strip(),
            self.ui.score_two_input.text().strip(),
            self.ui.score_three_input.text().strip(),
            self.ui.score_four_input_2.text().strip(),
        ]
        selected = raw_scores[:attempts]
        scores = []
        for s in selected:
            if not s.isdigit():
                self.ui.enter_valid_score_text.show()
                QMessageBox.warning(None, "Invalid Score", "Scores must be numbers between 0 and 100.")
                raise ValueError("bad score")
            val = int(s)
            if val < 0 or val > 100:
                self.ui.enter_valid_score_text.show()
                QMessageBox.warning(None, "Invalid Score", "Scores must be between 0 and 100.")
                raise ValueError("bad score")
            scores.append(val)

        return name, attempts, scores

    def _append_csv(self, filename, name, attempts, scores, grades,
                    highest, average):
        # pad to 4 columns
        padded_scores = scores + [""] * (4 - len(scores))
        padded_grades = grades + [""] * (4 - len(grades))

        final_score = average
        final_grade = get_letter_grade(int(round(average)))
        highest_grade = get_letter_grade(highest)

        # check if file is new or empty
        file_is_new = not os.path.exists(filename) or os.path.getsize(filename) == 0

        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # header row
            if file_is_new:
                writer.writerow(["Name", "Score 1", "Score 2", "Score 3", "Score 4", "Final", "Highest"])

            # student row
            writer.writerow([name] + padded_scores + [int(round(average)), highest])

            # grade row aligned under same headers
            writer.writerow(["Grades"] + padded_grades + [final_grade, highest_grade])

    def _clear_inputs(self):
        self.ui.Student_name_input.clear()
        self.ui.Number_of_attempts_input.clear()
        self.ui.Score_one_input.clear()
        self.ui.score_two_input.clear()
        self.ui.score_three_input.clear()
        self.ui.score_four_input_2.clear()
