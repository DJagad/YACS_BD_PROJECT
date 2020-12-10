# YACS_BD_PROJECT
Yet Another Centralized Schedular

So now in our design we have 3 files for the implementation of YACS master.py, worker.py and requests.py. We are using the config.json file for the machine config
The job requests are received on the port 5000 and listens to the updates on port 5001

# Code to run Master - python3 Master.py config.json {Scheduling Algorithm}

# How to Run the Master File

So now in our master.py this is how our implementation goes like, first we make our own dictionaries to store the worker details like their id’s, the slots and free slots

Then using a helper LaunchTask function which is used in the scheduling algorithms to send the tasks to the workers. First we are decrementing the number of free slots for the workers based on their id’s then make a socket connection with the workers and add the job details then we note the start time for logs, send task to the worker close the connection.

Then we are using 3 scheduling algorithms Random scheduling, Round Robin Scheduling and LeastLoaded Scheduling

In Random we are picking randomly among the workers and if the picked worker has no free slots it randomly picks another

In Round Robin Scheduling we are assigning the tasks to the workers in a circular manner and if there are no free slots pick the next worker in the order

In Least Loaded Scheduling we are first making a copy of the config workers and then we are sorting based on number of free slots, if no worker has free slot wait for 1s and try again otherwise it just assigns the task to the worker with most free slots

pickScheduler() is just used to pick the scheduling algorithm to choose based on the argument passed as command line argument
Now comes the main part where we talk about threads

Thread1 addressRequests(): So in the first thread we are allocating to a function called addressRequests() which is in master, so from the flow chart we can get a basic idea, so what we are trying to do is first we make a socket connection with jRSocket this connection is to receive job requests from request.py, so now we read the job request, increment the number of job count, record the job start time and then we add the job to the scheduling pool. Then finally based on the scheduler we assign the map tasks.

Thread2 updateSlots():  So in the second thread we are allocating to a function called updateSlots() which is in the master, so as we can refer to the flow chart below to understand things, so in this thread we first make jUSocket Connection to listen to the updates from the woker.py, so we are reading the task completion info and then basically updating the task logs, then convert the worker id to index in the config dictionary we made in the beginning, then increment the number of free slots for the respective worker, now in the updated config file, we are comparing and checking if job type is M then it is map task so we remove the respective job’s mapper task from the scheduling pool otherwise it means it was a reducer task compare the task id’s and then remove respective job’s reducer task from the list and then finally when no mapper and no reducer tasks are left we are updating the duration of the job and remove the job from the scheduling pool and decrement the job count and then close the connection.

Thread3 monitorReduce(): So in the third thread we are allocating to a function called monitorReduce() which is in the master, first we make a list to keep track of reduce tasks that have already been scheduled, now we make a copy of scheduling pool, then we are comparing the status and job id which are not scheduled that is to check if all map tasks are complete and not already scheduled, then we add the task to list of scheduled tasks and then pick a scheduling algorithm which is passed as the argument. We can refer to the flowchart below to understand the workflow.

# Code to run Master - python3 worker.py {Worker_Port} {Worker_Id}

Now let’s checkup on the worker threads 

Thread4 bag_of_tasks(): This thread we are allocating for con_ect() function until the requests are sent.
Con_ect() function: In this function we are basically adding the task requests to the JSON String and giving to the mod function.
mod() Function: This function will help to simulate the start time and add the task in the jt_pool.
We are reading the task details, noting down the entry time for the task and then adding the task id and task start time onto the execution pool if the task exists, can refer to the below chart for the workflow.

Thread5 simulate(): This thread we are allocating for simulate() function, so in this function we are first making a copy of the jt_pool and then decrementing the duration and showing the current time for the task we are decrementing till the duration becomes 0 when it becomes 0 we update with the status that the task has been finished in the worker we note down the end time in the jt_pool then we make the socket connection and dump the modified jt_pool and close the socket communication and delete jt_pool of that task id
