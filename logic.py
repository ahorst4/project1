from PyQt6.QtWidgets import *
from projectgui import *
import csv



class Voter:
    """
    Represents a voter in the system.
    """

    def __init__(self, voter_id: str):
        """
        Initialize a voter object.

        :param voter_id: The unique ID of the voter.
        """
        self.__voter_id = voter_id

    def get_voter_id(self) -> str:
        """
        Get the voter's ID.

        :return: Voter ID as a string.
        """
        return self.__voter_id

class Candidate:
    """
    Represents a candidate.
    """

    def __init__(self, name: str):
        """
        Initialize a candidate object.

        :param name: Name of the candidate.
        """
        self.name = name


class VoteManager:
    """
    Manages voting logic and csv file storage.
    """

    def __init__(self, file_path: str = 'votes.csv'):
        """
        Initialize the VoteManager with an optional csv file path.

        :param file_path: Path to the csv file storing votes.
        """
        self.file_path: str = file_path
        self.voted_ids: set[str] = self._load_voter_ids()

    def _load_voter_ids(self) -> set[str]:
        """
        Load existing voter IDs to not have multiple.

        :return: Set of previously used voter IDs.
        """
        try:
            with open(self.file_path, mode='r', newline='') as file:
                return {row[0] for row in csv.reader(file) if row}
        except FileNotFoundError:
            return set()


    def is_valid_voter_id(self, voter_id: str) -> bool:
        """
        Check that the voter IDs are numeric and not reused.

        :param voter_id: Voter's ID to validate.
        :return: True if valid, False otherwise.
        """
        return voter_id.isdigit() and voter_id not in self.voted_ids

    def record_vote(self, voter: Voter, candidate: Candidate) -> None:
        """
        Record a vote in the csv file.

        :param voter: Voter object containing ID.
        :param candidate: Candidate object containing name.
        :raises IOError: If the vote cannot be recorded.
        """
        try:
            with open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([voter.get_voter_id(), candidate.name])
            self.voted_ids.add(voter.get_voter_id())
        except Exception as e:
            raise IOError(f'Failed to save vote: {e}')


def handle_vote_submission(ui: Ui_voting_menu, vote_manager:VoteManager, parent_window) -> None:
    """
    Handle the logic when a user submits their vote from the gui.

    :param ui: The UI instance from projectgui.py.
    :param vote_manager: Instance of VoteManager for vote processing.
    :param parent_window: The main application window.
    """
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
