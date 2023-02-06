from tkinter import Tk
from typing import List, Callable

from .feedback_suggestion import FeedbackSuggestion
from .gui.compare_gui import CompareGUI


def run_manual_comparison(
        suggestions: List[FeedbackSuggestion],
        on_accept: Callable[[FeedbackSuggestion], None],
        on_reject: Callable[[FeedbackSuggestion], None],
        get_accepted: Callable[[], List[FeedbackSuggestion]],
        get_rejected: Callable[[], List[FeedbackSuggestion]]
):
    suggestions = suggestions.copy()

    def next_suggestion():
        if len(suggestions) == 0:
            print("No more suggestions!")
            return
        suggestion = suggestions.pop()
        gui.set_suggestion(suggestion)

    def do_and_next(func, suggestion: FeedbackSuggestion):
        func(suggestion)
        # look for exactly the same code and do the same
        for s in suggestions:
            if s.code == suggestion.code and s.originally_on_code == suggestion.originally_on_code:
                suggestions.remove(s)
                func(s)
        next_suggestion()

    def accept_and_next(suggestion: FeedbackSuggestion):
        do_and_next(on_accept, suggestion)

    def reject_and_next(suggestion: FeedbackSuggestion):
        do_and_next(on_reject, suggestion)

    root = Tk()
    gui = CompareGUI(root, accept_and_next, reject_and_next, get_accepted, get_rejected)
    next_suggestion()
    gui.master.mainloop()
    root.destroy()
