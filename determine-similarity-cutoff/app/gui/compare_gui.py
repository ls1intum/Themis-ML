import time
from tkinter import *
from typing import Callable, List

from .score_frame import ScoreFrame
from ..feedback_suggestion import FeedbackSuggestion


# shows suggestion.originally_on_code and suggestion.code side by side
class CompareGUI:
    suggestion: FeedbackSuggestion

    def __init__(
            self, master,
            on_accept, on_reject,
            get_accepted: Callable[[], List[FeedbackSuggestion]],
            get_rejected: Callable[[], List[FeedbackSuggestion]]
    ):
        self.on_accept = on_accept
        self.on_reject = on_reject

        self.master = master
        self.master.title("Compare")

        self.code_frame = Frame(master)
        self.code_frame.pack(side=TOP)

        self.orig_code = Text(self.code_frame, height=50, width=100)
        self.orig_code.pack(side=LEFT)
        self.orig_code.insert(END, "original")

        self.code = Text(self.code_frame, height=50, width=100)
        self.code.pack(side=LEFT)
        self.code.insert(END, "compare against this")

        self.explainer = Label(
            self.master,
            text="Accept if these code snippets are similar enough to receive the same feedback."
        )
        self.explainer.pack(side=TOP)

        self.score = Label(self.master, text="Score: 0")
        self.score.pack(side=TOP)

        self.button_frame = Frame(master)
        self.button_frame.pack(side=TOP)

        self.accept_button = Button(self.button_frame, text="Accept", command=self.accept)
        self.accept_button.pack(side=LEFT)
        self.reject_button = Button(self.button_frame, text="Reject", command=self.reject)
        self.reject_button.pack(side=LEFT)

        self.score_frame = ScoreFrame(master, get_accepted, get_rejected)
        self.score_frame.pack(side=TOP)
        self.score_frame.update_score()

        # take focus
        self.master.focus_set()

    def set_suggestion(self, suggestion: FeedbackSuggestion):
        self.suggestion = suggestion
        self.orig_code.delete(1.0, END)
        self.orig_code.insert(END, suggestion.originally_on_code)
        self.code.delete(1.0, END)
        self.code.insert(END, suggestion.code)
        self.score.config(text="Score: " + str(suggestion.similarity_score))

    def button_visual_feedback(self):
        self.accept_button.config(state=DISABLED)
        self.reject_button.config(state=DISABLED)
        self.master.update()
        time.sleep(0.5)
        self.accept_button.config(state=NORMAL)
        self.reject_button.config(state=NORMAL)

    def accept(self):
        self.on_accept(self.suggestion)
        self.score_frame.update_score()
        self.button_visual_feedback()

    def reject(self):
        self.on_reject(self.suggestion)
        self.score_frame.update_score()
        self.button_visual_feedback()
