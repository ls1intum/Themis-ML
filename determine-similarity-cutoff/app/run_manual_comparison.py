from bisect import *
from tkinter import Tk
from typing import List, Callable

from .feedback_suggestion import FeedbackSuggestion
from .find_optimal_split import find_optimal_split
from .gui.compare_gui import CompareGUI
from .suggestion_score import suggestion_score


def equal_except_whitespace(s1: str, s2: str) -> bool:
    return "".join(s1.split()) == "".join(s2.split())


def run_manual_comparison(
        suggestions: List[FeedbackSuggestion],
        on_accept: Callable[[FeedbackSuggestion], None],
        on_reject: Callable[[FeedbackSuggestion], None],
        get_accepted: Callable[[], List[FeedbackSuggestion]],
        get_rejected: Callable[[], List[FeedbackSuggestion]]
):
    suggestions = suggestions.copy()
    # sort once to only find later
    suggestions.sort(
        key=lambda s: s.similarity_score
    )

    def pop_suggestion(opt_split: float) -> FeedbackSuggestion:
        # finds the first suggestion with a similarity score greater than the optimal split
        i = bisect_left(suggestions, opt_split, key=lambda s: s.similarity_score)
        suggestion = suggestions.pop(i)
        return suggestion

    def next_suggestion():
        if len(suggestions) == 0:
            print("No more suggestions!")
            return
        accepted = get_accepted()
        rejected = get_rejected()
        opt_split, _ = find_optimal_split(accepted, rejected, suggestion_score)
        suggestion = pop_suggestion(opt_split)
        gui.set_suggestion(suggestion)
        if suggestion.code == suggestion.originally_on_code:
            print("Skipping suggestion because it is the same as the original code")
            accept_and_next(suggestion)
        for a in accepted:
            if a.code == suggestion.code:
                print("Skipping suggestion because it is the same as an accepted code")
                accept_and_next(suggestion)
        for r in rejected:
            if r.code == suggestion.code:
                print("Skipping suggestion because it is the same as a rejected code")
                reject_and_next(suggestion)

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
