import sys
from PyQt6 import *
from projectgui import *
from logic import *

class VotingApp(QMainWindow):
    """
    Main application window for the voting gui.
    """

    def __init__(self) -> None:
        """
        Initialize the VotingApp, set up the UI, and connect signals.
        """
        super().__init__()
        self.ui = Ui_voting_menu()
        self.ui.setupUi(self)
        self.vote_manager = VoteManager()

        self.ui.pushButton.clicked.connect(self.submit_vote)


    def submit_vote(self) -> None:
        """
        Triggered when the user clicks the submit button.
        Handles vote validation and recording.
        :return:
        """
        handle_vote_submission(self.ui, self.vote_manager, self)

def main() -> None:
    """
    Entry point of the application. Creates and runs the GUI app
    """
    app = QApplication(sys.argv)
    window = VotingApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()