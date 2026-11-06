import threading


CUSTOMER_COUNT = 3
TELLER_ID = 0

# once teller says ready, we make it available
teller_available = threading.Semaphore(0)
# signals that a customer has written its ID for the teller and is ready
customer_ready = threading.Semaphore(0)
# signals that the teller has acknowledged the current customer
introduction_received = threading.Semaphore(0)
# only one thread can print a message at a time to make it easy to understand
output_mutex = threading.Semaphore(1)


# whichever has teller's turn only can write to this
current_customer_id = None


# prints the actions to terminal without mixing messages from other threads
def log(message):
    with output_mutex:
        print(message, flush=True)


# announces readiness, then waits for and acknowledges each customer
def teller(teller_id):
    log(f"Teller {teller_id}: ready to serve")
    teller_available.release()

    for _ in range(CUSTOMER_COUNT):
        log(f"Teller {teller_id}: waiting for a customer introduction")
        customer_ready.acquire()

        customer_id = current_customer_id
        log(f"Teller {teller_id} [Customer {customer_id}]: acknowledges introduction")
        introduction_received.release()

    log(f"Teller {teller_id}: finished introductions")


# each customer takes turn, shares ID, and waits for acknowledgment before giving turn
def customer(customer_id):
    global current_customer_id

    log(f"Customer {customer_id} [Teller {TELLER_ID}]: waiting to select teller")
    teller_available.acquire()
    log(f"Customer {customer_id} [Teller {TELLER_ID}]: selects teller")

    current_customer_id = customer_id
    log(f"Customer {customer_id} [Teller {TELLER_ID}]: introduces itself")
    customer_ready.release()

    introduction_received.acquire()
    log(f"Customer {customer_id} [Teller {TELLER_ID}]: introduction acknowledged")

    # we don't switch the turn until customer receives their acknowledgement
    teller_available.release()


# main driver program
# creates/starts threads and waits for them to finish
def main():
    teller_thread = threading.Thread(target=teller, args=(TELLER_ID,))
    customer_threads = [
        threading.Thread(target=customer, args=(customer_id,))
        for customer_id in range(CUSTOMER_COUNT)
    ]

    teller_thread.start()
    for thread in customer_threads:
        thread.start()

    for thread in customer_threads:
        thread.join()
    teller_thread.join()


if __name__ == "__main__":
    main()
