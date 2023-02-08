# Determine similarity cutoff
This folder includes code that helps to find the optimal
similarity cutoff to determine which feedback suggestions will 
be shown to the user.

## How to start
- Get some feedback suggestions from the `/feedback_suggestions` endpoint as described in the other READMEs
- Copy the suggestions in JSON format into a new (.gitignore-d) file called `suggestions.json` in this folder
- Run `python start.py` to start the script. It will delete the contents of suggestions.json file and instead put the suggestions into an SQLite database for faster access. 
Then it will open a Tkinter GUI for you to compare pieces of code.

## How to use the GUI
- The GUI shows two pieces of code side by side. The left one is the code that was submitted by the user, the right one is code from another submission. You can see the assigned similarity on the bottom.
- If you think that the two pieces of code are similar enough to receive the same feedback, click "Accept". If you think that the two pieces of code are not similar enough, click "Reject".
- The accepted + rejected suggestions will be written into the `suggestions.sqlite` database as well. 
- On the bottom you can see the optimal similarity cutoffs based on similarity scores given by CodeBERT. They get points for each rejected suggestion with a lower similarity score and each accepted suggestion with a higher similarity score. The cutoff with the most points is the optimal one.
- In some cases you might have to wait a while between suggestions because the system auto-updates other similar ones based on your previous judgement.