## 11/06/2026 9:42 am

According to the project details, I have to create a bank with three tellers and 50 customers using threads. The tellers and customers need to communicate through shared information and use semaphores to control to know when each thread can continue. I'm going to use Python to code this project.

For this session, I'm only understanding what I have to do and planning how I can break the project up into parts to work on rather than coding the whole thing. I think for the first part, I want to make the one teller and three customers introducing themselves. I need to think about how the teller will receive each customer's ID and acknowledge the introduction before another customer uses the same shared information.

## 11/06/2026 10:08 am

I finished looking at the requirements and found how I want to split up the project. I'll start with one teller and three customers like I said before to ensure the base functionality works right. Once that works, I'll add the three tellers, waiting customers, and the bank opening and door rules. Then I'll work on the customer transaction part and waiting for that to finish. The next part would be to add the manager functionality for withdrawals and safe for the two types of transactions. The final part will be making sure the code works with all 50 customers, tellers finish, and closing the bank properly.

From the requirements and examples, I realized that semaphores can be used both to limit access and to signal another thread. The manager only allows one teller at a time, while the safe allows two. For the introduction, I need shared information to hold the customer's ID and a signal to let the teller know it is ready to read. I also need to make sure another customer doesn't replace that ID before the teller has received it. Next session, I'll work on the indroduction part and ensure that works before moving on to the more complex sections.

## 11/06/2026 10:17 am

For this session, I plan to create the introduction part with one teller and three customers. Each customer has to wait for the teller, then put its ID in shared information to access, and finally signal that it is ready to introduce itself. The teller will read that ID and acknowledge it. Something I need to make sure is that the next customer can't replace the ID or take someone's acknowledgment. To do this, I think I have to make sure current customer keeps their turn until they receive the acknowledgement for them. To ensure it works, I'll check that each customer is acknowledged once and that all four threads finish.

## 11/06/2026 10:47 am

The introduction part is now in project2.py. The teller and customer functions are in the same file like needed with the required parts like shared ID, semaphores, and code that starts and joins the threads. The customer keeps its turn until it receives the teller's acknowledgment, before letting the next customer take over. For printing, we also use a semaphore so that messages won't get mixed together.

The checks passed with different customer start orders. Each customer was acknowledged once, and then all threads finished properly. I didn't see any failures come up during these checks. The next part I want to work on is the three tellers, waiting customers, and bank opening and door rules.

## 11/08/2026 2:13 pm

For this session, I plan to expand the introduction part to three tellers with IDs 0, 1, and 2. Customers need to wait until all three tellers are ready before entering the bank. I'll need to keep track of tellers that are available and protect that shared information with a semaphore so that two customers can't select the same teller. Additionally, each teller will also need their own shared customer ID and introduction signals for the acknowledgment to go to the right customer. If all tellers are busy, then the customers should have to wait.

I'll need to add a door semaphore that allows two customers to pass through at a time for entering and exiting. Once customer passes through door, it should be released for use. I will also check that no customer enters before the bank opens, no teller is assigned to two customers at once, each customer gets the correct acknowledgment, and all threads finish properly.

## 11/08/2026 2:59 pm

I expanded the introduction part so now we include the three tellers and five customers beofre we slowly get to the final result. The main thread waits for all three tellers to signal that they're ready before opening bank for customers. I used a semaphore to count available tellers, and another one protects the list of teller IDs while they change. Also, each teller has their own shared customer ID and introduction signals. Like stated, the customer keeps the teller's turn until they receives acknowledgment, before making the teller available again for others. I also added the door semaphore for both entry and exit and release it after the customer passes through.

From running the program, it showed that customers waited for the bank to open, each customer got an acknowledgment from the teller they selected, and no teller was assigned to two customers at the same time. The door also stayed within limit of 2, and all threads finished without problems. I used a stop signal after all customers finished so the tellers could stop waiting. Next, I'll work on customers choosing deposit or withdrawal and having the conversation with the teller to complete the transaction.

## 11/08/2026 3:00 pm

For this session, I plan to add onto the introduction part by adding the transaction conversation. I'll make each customer randomly choose deposit or withdrawal before entering the bank. Then, after the introduction, the teller will ask what transaction the customer wants and wait for the answer. Then, I'll use shared information for the transaction and semaphores to signal when each step can continue. The customer will have to wait for the teller to say the transaction is done, and the teller will wait for the customer to leave the station before becoming available again. I'll make previous rules apply here also.

I'll keep three tellers and five customers while working on this part to make it a little easier for me to check. I'll check the printed messages to make sure the transaction is requested before the customer gives it, the teller receives the correct choice, and the customer leaves only after proper completion (signal from teller). I'll also check that the previous parts that are working still continue to work after this. I think for this part that should be enough and then I'll focus on building upon it.
