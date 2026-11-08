# CS4348 Project 2

Run with Python 3; no extra packages are required:

```sh
python3 project2.py
```

The current version prints three tellers becoming ready, the bank opening,
and five customers choosing deposit or withdrawal and entering. Each customer
introduces itself to a teller, gives its choice when asked, waits for a
completion signal, and leaves. This stage only simulates the conversation;
manager and safe actions will be added later. The program exits after all
threads finish.
