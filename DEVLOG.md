## 11/06/2026 9:42 am

According to the project details, I have to create a bank with three tellers and 50 customers using threads. The tellers and customers need to communicate through shared information and use semaphores to control to know when each thread can continue. I'm going to use Python to code this project.

For this session, I'm only understanding what I have to do and planning how I can break the project up into parts to work on rather than coding the whole thing. I think for the first part, I want to make the one teller and three customers introducing themselves. I need to think about how the teller will receive each customer's ID and acknowledge the introduction before another customer uses the same shared information.

## 11/06/2026 10:08 am

I finished looking at the requirements and found how I want to split up the project. I'll start with one teller and three customers like I said before to ensure the base functionality works right. Once that works, I'll add the three tellers, waiting customers, and the bank opening and door rules. Then I'll work on the customer transaction part and waiting for that to finish. The next part would be to add the manager functionality for withdrawals and safe for the two types of transactions. The final part will be making sure the code works with all 50 customers, tellers finish, and closing the bank properly.

From the requirements and examples, I realized that semaphores can be used both to limit access and to signal another thread. The manager only allows one teller at a time, while the safe allows two. For the introduction, I need shared information to hold the customer's ID and a signal to let the teller know it is ready to read. I also need to make sure another customer doesn't replace that ID before the teller has received it. Next session, I'll work on the indroduction part and ensure that works before moving on to the more complex sections.

## 11/06/2026 10:17 am

For this session, I plan to create the introduction part with one teller and three customers. Each customer has to wait for the teller, then put its ID in shared information to access, and finally signal that it is ready to introduce itself. The teller will read that ID and acknowledge it. Something I need to make sure is that the next customer can't replace the ID or take someone's acknowledgment. To do this, I think I have to make sure current customer keeps their turn until they receive the acknowledgement for them. To ensure it works, I'll check that each customer is acknowledged once and that all four threads finish.


