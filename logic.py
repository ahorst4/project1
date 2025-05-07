from PyQt6.QtWidgets import *
from projectgui import *
import csv



class Voter:
    def __init__(self, voter_id):
        self.__voter_id = voter_id

    def get_voter_id(self):
        return self.__voter_id

class Candidate:
    def __init__(self, name):
        self.name = name


class VoteManager:
    def __init__(self, file_path: str = 'votes.csv'):
        self.file_path = file_path
        self.voted_ids = self._load_voter_ids()

    def _load_voter_ids(self):
        try:
            with open(self.file_path, mode='r', newline='') as file:
                return {row[0] for row in csv.reader(file) if row}
        except FileNotFoundError:
            return set()


    def is_valid_voter_id(self, voter_id):
        return voter_id.isdigit() and voter_id not in self.voted_ids

    def record_vote(self, voter: Voter, candidate: Candidate):
        try:
            with open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([voter.get_voter_id(), candidate.name])
            self.voted_ids.add(voter.get_voter_id())
        except Exception as e:
            raise IOError(f'Failed to save vote: {e}')


def handle_vote_submission(ui: Ui_voting_menu, vote_manager:VoteManager, parent_window):
    voter_id = ui.id_input.text().strip()
    if not vote_manager.is_valid_voter_id(voter_id):
        QMessageBox.warning(parent_window, 'Invalid ID', 'ID is either invalid or already used.')
        return

    if ui.john_button.isChecked():
        candidate = Candidate('John')
    elif ui.jane_button.isChecked():
        candidate = Candidate('Jane')
    else:
        QMessageBox.warning(parent_window, 'No Candidate', 'Please select a candidate.')
        return

    try:
        voter = Voter(voter_id)
        vote_manager.record_vote(voter, candidate)
        QMessageBox.information(parent_window, 'Vote Submitted', 'Your vote has been recorded.')

        ui.id_input.clear()
        ui.john_button.setAutoExclusive(False)
        ui.john_button.setChecked(False)
        ui.john_button.setAutoExclusive(True)

        ui.jane_button.setAutoExclusive(False)
        ui.jane_button.setChecked(False)
        ui.jane_button.setAutoExclusive(True)

    except Exception as e:
        QMessageBox.critical(parent_window, 'Error', f'An error occurred while saving your vote: {e}')
