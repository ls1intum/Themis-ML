# Inject Testing Data
This is a simple script to inject testing data into a running instance of the
Feedback Suggestion server.

You can provide the server URL and the URL that this temporary server will be
available at. This will then notify the ThemisML endpoint and point it to itself
for downloading the submissions found in the `test-submissions` folder.

## Usage
### Starting up the server(s)
You will need to start two servers locally: The ThemisML main server and the "Inject Testing Data" server.
The testing data server will behave like an Artemis instance in the sense that it provides endpoints 
for downloading submissions. It also has development endpoints for you that will be talked about later.

### Setting up test submissions
The test submissions are stored in the `test-submissions` folder.
Each folder in there represent a submission.
The folder names should follow the following format:

`<exercise-id>_<participation-id>`

Example: `1-1`

Please note that all participation IDs have to be unique, even with different exercise IDs!

You can then put the same file into both folders and slightly change the code in one or both of them.

### Adding test feedbacks
Add a test feedback to a submission by opening a code file in the submission and adding a comment formatted like this 
to the respective line:
```
// feedback: <feedback-text>
```

This will be picked up as feedback and stored in the database.
To actually notify the ThemisML server of the change (and store the feedback),
visit http://localhost:8001/notify_for_exercise/<exercise_id> in your browser.
This will notify the ThemisML server of all submissions for the given exercise ID.

It will fetch the feedback and the Test Injection Server will respond with your
feedback comments.

### Verifying That Feedback Was Added
Open the `feedback` database in Postgres to verify that the feedback was added.

## Getting a Feedback Suggestion
To get a feedback suggestion, send a POST request to 
http://localhost:8000/feedback_suggestion. Include a JSON body of 
```
{
    "token": "not_needed_here",
    "server": "http://localhost:8001",
    "exercise_id": <some id>,
    "participation_id": <some other id>
}
```
The `server` property will instruct ThemisML to think of the Inject Testing Data server as the Artemis server.