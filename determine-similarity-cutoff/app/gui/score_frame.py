from tkinter import *
from typing import List, Callable

from ..feedback_suggestion import FeedbackSuggestion
from ..find_optimal_split import find_optimal_split
from ..suggestion_score import suggestion_score_functions


class ScoreFrame(Frame):
    def __init__(
            self, master,
            get_accepted: Callable[[], List[FeedbackSuggestion]],
            get_rejected: Callable[[], List[FeedbackSuggestion]]
    ):
        super().__init__(master)
        self.label = None
        self.get_accepted = get_accepted
        self.get_rejected = get_rejected

    def update_score(self):
        accepted = self.get_accepted()
        rejected = self.get_rejected()
        for widget in self.winfo_children():
            widget.destroy()
        self.label = Label(self, text="Scores")
        self.label.pack(side=TOP)
        scoreboard = []
        for name, func in suggestion_score_functions.items():
            split, points = find_optimal_split(accepted, rejected, func)
            scoreboard.append((name, split, points))
        scoreboard.sort(key=lambda x: x[2], reverse=True)
        for name, split, points in scoreboard:
            label = Label(self, text=f"{name}: split at {split:.2f} with {points} points")
            label.pack(side=TOP)
