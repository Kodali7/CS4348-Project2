# CS4348 Project 2

Run with Python 3; no extra packages are required:

```sh
python3 project2.py
```

The current version prints three tellers becoming ready, the bank opening,
and five customers choosing deposit or withdrawal and entering. Each customer
introduces itself to a teller, gives its choice when asked, waits for a
completion signal, and leaves. Withdrawals get manager approval one teller at
a time, with a random 5 to 30 ms delay. Both transaction types use the safe,
which holds up to two tellers, with a random 10 to 50 ms delay. The program
exits after all threads finish.
