# Wiki TimeBox ETL Project
This is a personal project that I started due to my interest in Data Engineering. I wanted to learn about:
- AWS
- ETL pipelines
    - Extracting data
    - Transforming data into the format needed to by the final user. Staging tables and intermediate steps
    - Loading the data to the databases that the final use will fetch
    - Logging. How to properly maintain an ETL and keep documented all actions performed. How to find what is the issue in case of failure
    - Cron pipelines, run every X time
- General database concepts: HA, ACID, scalability and others
- Complex an optimal SQL queries

There were tons of stuff that I wanted to learn, so I decided to do it with a small personal project. I find it easier to learn by applying things to something that interest me so that is how I came up with this project.

This project started as an idea after I was defeated in Trivial!
I realised that I don't have much knowledge on History facts, so I came up with the following:

Every day, Wikipedia displays a list of events that happened this year in the past. For example:

https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/April_2

This will display a list of 5 events that happened in the past on 2nd of April. Any day can be accessed if you change the month and the day in the URL.

So the idea was the following: "I want to create an ETL that will retrieve the HTML page of Wikipedia in its corresponding day, retrieve the list of 5 events that happened that day and store it in a database".
Once retrieved, I thought about two options: send it to my email or display it in a webpage.
Sending it to the email would force me to read it. If I read the email everyday, I would learn a lot of things!

I could have done any of those but I got just to the "storing to a database" stage, since I didn't want to have my jobs Active 24/7. I just wanted to see if I could manage to finish this!

Just as a note, surely there will be a better way to do what I am doing, but as said this was a learning experience. I will try to keep this code updated as I learn new stuff!

Let's talk first about the technologies that I used:

## Luigi
Luigi is a package that helps you build complex pipelines of batch jobs.
After some research, I found that Luigi and Airflow are two of the most popular packages for building pipelines.
Both share similar processes, but I decide to go with Luigi because it is easier to use in Windows. However, I would do more research if I had to do a more complex project, and I would choose a package that matches my requirements. For now, since this is a small task, I will go with Luigi

## AWS
First I was overwhelmed by the number of services that Amazon offers. To narrow my search, I started thinking what are the needs for my problem. I needed: 
- A service to host my pipeline that would run every day
- A place to store intermediate files, outputs of Luigi tasks that are used as inputs in other tasks
- A database to store the data extracted everyday

As a service, EC2 looks like it is what I am looking for. EC2 allows to run a virtual server where I can host my pipeline code that will run every day

For the database I found the following options:
- S3: Is an Object Storage, which allows to store objects (self explanatory). You can insert object and read it but not edit it WORM(write once, read many)
- DynamoDB: NoSQL database
- RDS: SQL database

I decided to use RDS because one of my objectives was to learn proper SQL and check out more complex queries.
Instead of RDS, I could have used EC2 and installed a database there, but I decided to go for the RDS directly, mainly because AWS already facilitates RDS to use directly a database and I didn't see the point on spending time on configuring it in a virtual server. The only advantage would be that I would have more control over it, but for my case RDS is just fine.



## Concepts learned
Finally, I wanted to talk about other concepts learned in this project

I learned about the 3 Vs (Verity, velocity, and volume).
AWS which may not be a worry in this small project but are good to keep in mind!

HA (High Availability): A Cloud Databases HA instance group includes a source database instance and one or two replicas. If main fails, other will take the place until main is restored

To have optimal transaction control, a database system must be ACID compliant, which stands for the following properties: Atomicity, Consistency, Isolation, Durability

**Atomicity**: We cant send a transaction that is half complete. Black or white. A transaction must be completed. If it stops at midoperation, it will not be done. 

**Consistency**: All data must be consistent after every transaction. Database has always to be consistent. Any data written to the database must be valid according to all defined rules and constraints. Follow the rules

**Isolation**: Each transaction must occur independently of other transactions occurring at the same time.

**Durability**: Committed transactions must be fully recoverable in all but the most extreme circumstances. Write-ahead logs provide absolute data durability until data is eventually written into permanent data and index files. Durability can be achieved by flushing the transaction's log records to non-volatile storage before acknowledging commitment.

### Pipeline framework selection
We use Luigi


### Pipeline structure
Staging step
Loading step
