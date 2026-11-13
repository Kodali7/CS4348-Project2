# CS4348 Project 2

Run with Python 3; no extra packages are required:

```sh
python3 project2.py
```

The program starts three teller threads and 50 customer threads. The bank opens
after all three tellers are ready. Each customer chooses deposit or withdrawal
and waits a random 0 to 100 ms before trying to enter, introduces itself to a
teller, gives its choice when asked, waits for a completion signal, and leaves.
Withdrawals get manager approval one teller at a time, with a random 5 to 30 ms
delay. Both transaction types use the safe, which holds up to two tellers, with
a random 10 to 50 ms delay. The door allows two customers to pass through at a
time, and customers wait when all tellers are busy. Semaphores protect shared
resources and signal each step between a teller and customer.

After all 50 customers have left, the main thread signals the tellers to stop
and joins them. The program prints `Bank: closed` after all threads finish.
