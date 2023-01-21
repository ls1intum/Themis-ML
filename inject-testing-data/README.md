# Inject Testing Data
This is a simple script to inject testing data into a running instance of the
Feedback Suggestion server.

You can provide the server URL and the URL that this temporary server will be
available at. This will then notify the ThemisML endpoint and point it to itself
for downloading the submissions found in the `test-submissions` folder.

Warning: The server will essentially expose its whole filesystem!
Don't run it publically.