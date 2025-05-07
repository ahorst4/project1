import sys
from PyQt6 import *
from projectgui import *
from logic import *

class VotingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_voting_menu()
        self.ui.setupUi(self)
        self.vote_manager = VoteManager()

        self.ui.pushButton.clicked.connect(self.submit_vote)


    def submit_vote(self):
        handle_vote_submission(self.ui, self.vote_manager, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VotingApp()
    window.show()
    sys.exit(app.exec())