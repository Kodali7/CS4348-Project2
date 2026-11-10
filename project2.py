import random
import threading
import time


CUSTOMER_COUNT = 5
TELLER_COUNT = 3

# main waits for all tellers before letting customers enter
tellers_ready = threading.Semaphore(0)
bank_open = threading.Semaphore(0)
# the door is only held while passing through, not during the whole visit
door = threading.Semaphore(2)
# one teller with the manager, two in the safe
manager = threading.Semaphore(1)
safe = threading.Semaphore(2)
# counts the tellers that customers can select
teller_available = threading.Semaphore(0)
# protects the list when tellers or customers change it
available_tellers_mutex = threading.Semaphore(1)
available_tellers = []
# each teller has its own shared id and introduction signals
customer_ready = [threading.Semaphore(0) for _ in range(TELLER_COUNT)]
introduction_received = [threading.Semaphore(0) for _ in range(TELLER_COUNT)]
# separate signals keep the transaction steps in order for each teller
transaction_requested = [threading.Semaphore(0) for _ in range(TELLER_COUNT)]
transaction_ready = [threading.Semaphore(0) for _ in range(TELLER_COUNT)]
transaction_done = [threading.Semaphore(0) for _ in range(TELLER_COUNT)]
customer_left = [threading.Semaphore(0) for _ in range(TELLER_COUNT)]
# only one thread can print a message at a time to make it easy to understand
output_mutex = threading.Semaphore(1)


# only the customer holding a teller's turn can write these shared slots
current_customer_id = [None for _ in range(TELLER_COUNT)]
current_transaction = [None for _ in range(TELLER_COUNT)]


# prints the actions to terminal without mixing messages from other threads
def log(message):
    with output_mutex:
        print(message, flush=True)


# serves one customer at a time and waits for them to leave before the next
def teller(teller_id):
    log(f"Teller {teller_id}: ready to serve")
    with available_tellers_mutex:
        available_tellers.append(teller_id)
    teller_available.release()
    tellers_ready.release()

    while True:
        log(f"Teller {teller_id}: waiting for a customer introduction")
        customer_ready[teller_id].acquire()

        customer_id = current_customer_id[teller_id]
        # main clears the slot only after every customeer is done
        if customer_id is None:
            break
        log(f"Teller {teller_id} [Customer {customer_id}]: acknowledges introduction")
        introduction_received[teller_id].release()

        log(f"Teller {teller_id} [Customer {customer_id}]: asks for transaction")
        transaction_requested[teller_id].release()
        log(f"Teller {teller_id} [Customer {customer_id}]: waiting for transaction")
        transaction_ready[teller_id].acquire()
        transaction = current_transaction[teller_id]
        log(f"Teller {teller_id} [Customer {customer_id}]: received {transaction}")

        if transaction == "withdrawal":
            log(f"Teller {teller_id} [Customer {customer_id}]: goes to manager")
            with manager:
                log(f"Teller {teller_id} [Customer {customer_id}]: getting manager permission")
                time.sleep(random.randint(5, 30) / 1000)
                log(f"Teller {teller_id} [Customer {customer_id}]: received manager permission")

        # both types use the safe before telling customer done
        log(f"Teller {teller_id} [Customer {customer_id}]: goes to safe")
        with safe:
            log(f"Teller {teller_id} [Customer {customer_id}]: enters safe for {transaction}")
            time.sleep(random.randint(10, 50) / 1000)
            log(f"Teller {teller_id} [Customer {customer_id}]: leaves safe")

        log(f"Teller {teller_id} [Customer {customer_id}]: signals transaction completion")
        transaction_done[teller_id].release()

        log(f"Teller {teller_id} [Customer {customer_id}]: waiting for customer to leave")
        customer_left[teller_id].acquire()
        log(f"Teller {teller_id} [Customer {customer_id}]: customer left station")
        with available_tellers_mutex:
            available_tellers.append(teller_id)
        teller_available.release()

    log(f"Teller {teller_id}: finished serving")


# shares an id and transaction, then waits for completion before leaving
def customer(customer_id):
    transaction = random.choice(("deposit", "withdrawal"))
    log(f"Customer {customer_id}: chooses {transaction}")
    log(f"Customer {customer_id}: waiting for bank to open")
    bank_open.acquire()

    log(f"Customer {customer_id}: waiting to enter bank")
    with door:
        log(f"Customer {customer_id}: entering bank through door")
        log(f"Customer {customer_id}: entered bank")

    log(f"Customer {customer_id}: waiting to select teller")
    teller_available.acquire()
    with available_tellers_mutex:
        teller_id = available_tellers.pop(0)
    log(f"Customer {customer_id} [Teller {teller_id}]: selects teller")

    current_customer_id[teller_id] = customer_id
    log(f"Customer {customer_id} [Teller {teller_id}]: introduces itself")
    customer_ready[teller_id].release()

    introduction_received[teller_id].acquire()
    log(f"Customer {customer_id} [Teller {teller_id}]: introduction acknowledged")

    log(f"Customer {customer_id} [Teller {teller_id}]: waiting for transaction request")
    transaction_requested[teller_id].acquire()
    current_transaction[teller_id] = transaction
    log(f"Customer {customer_id} [Teller {teller_id}]: requests {transaction}")
    transaction_ready[teller_id].release()

    log(f"Customer {customer_id} [Teller {teller_id}]: waiting for transaction completion")
    transaction_done[teller_id].acquire()
    log(f"Customer {customer_id} [Teller {teller_id}]: transaction complete")

    log(f"Customer {customer_id} [Teller {teller_id}]: leaves teller")
    customer_left[teller_id].release()

    log(f"Customer {customer_id}: waiting to exit bank")
    with door:
        log(f"Customer {customer_id}: exiting bank through door")
        log(f"Customer {customer_id}: left bank")


# main driver program
# creates/starts threads and waits for them to finish
def main():
    teller_threads = [
        threading.Thread(target=teller, args=(teller_id,))
        for teller_id in range(TELLER_COUNT)
    ]
    customer_threads = [
        threading.Thread(target=customer, args=(customer_id,))
        for customer_id in range(CUSTOMER_COUNT)
    ]

    for thread in teller_threads:
        thread.start()
    for thread in customer_threads:
        thread.start()

    for _ in range(TELLER_COUNT):
        tellers_ready.acquire()
    log("Bank: open")
    for _ in range(CUSTOMER_COUNT):
        bank_open.release()

    for thread in customer_threads:
        thread.join()

    # wake idle tellers after every customer has finished
    for teller_id in range(TELLER_COUNT):
        current_customer_id[teller_id] = None
        customer_ready[teller_id].release()
    for thread in teller_threads:
        thread.join()


if __name__ == "__main__":
    main()
