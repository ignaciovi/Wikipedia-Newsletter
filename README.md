# Wiki Newsletter ETL Project
This is a personal project that I started due to my interest in Data Engineering. I wanted to learn about:
- AWS
- ETL pipelines
    - Extracting data
    - Transforming data into the format required by the final user. Staging tables and intermediate steps
    - Loading the data to the databases that the final use will fetch
    - Logging. How to properly maintain an ETL and keep documented all actions performed. How to find what is the issue in case of failure
    - Cron pipelines that run every X time
- General database concepts: HA, ACID, scalability and others
- Complex an optimal SQL queries

There were tons of concepts that I wanted to learn, so I decided to start a small personal project to keep a balance between theory-practice and make the learning experience more interesting! I find it easier to learn by doing something that interest me, so that is how I came up with this project idea.

This project started as an idea after I was defeated in a Trivial game. I realised that I don't have much knowledge on History facts, so I came up with the following idea:

Every day, Wikipedia displays a list of events that happened today in previous years. For example:

*1513 – Spanish conquistador Juan Ponce de León sighted land, which he named La Florida, according to a popular legend while searching for the Fountain of Youth.* (From: https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/April_2)

This page will display a list of 5 events that happened in the past on the 2nd of April. Any day can be accessed if you change the month and the day at the end of the URL.

So the idea was the following: "I want to create an ETL that will retrieve the HTML page of Wikipedia in its corresponding day, retrieve the list of 5 events that happened that day and store it in a database. This will repeat every day".
Once retrieved, I thought about two options: send it to my email or display it in a webpage.
Sending it to the email would force me to read it which would make me learn a lot of things at the end of the week. I would call this project something like a "Wikipedia Daily Newsletter".

I could have done any of those 2 ideas, but at the end I got just to the "storing to a database" stage, since I didn't want to have my AWS jobs Active 24/7. I just wanted to see if I could manage to finish this project and run it at least once!

Just as a note, surely there will be a better way to do what I am doing, but as said this was a learning experience. I will try to keep this code updated as I learn new stuff!

Let's talk first about the technologies that I used:

## Luigi
Luigi is a package that helps you build complex pipelines of batch jobs.
After some research, I found that Luigi and Airflow are two of the most popular packages for building pipelines.
Both share similar processes, but I decide to go with Luigi because it is easier to use in Windows. However, I would do more research if I had to do a more complex project, and I would choose the package that best matches my requirements. For now, since this is a small task, I will use Luigi since it is easier to use in Windows.

## AWS
First I was overwhelmed by the number of services that Amazon offers. To narrow my search, I started thinking what are the needs for my problem. I needed: 
- A service to host my pipeline that would run every day
- A place to store intermediate files, outputs of Luigi tasks that are used as inputs in other tasks
- A database to store the data extracted everyday

As a service, EC2 looks to be what I am looking for. EC2 allows to run a virtual server where I can host my pipeline code that will run every day.

As a service to store my date, I found the following options:
- S3: Is an Object Storage, which allows to store objects (self explanatory). You can insert object and read it but not edit it WORM(write once, read many)
- DynamoDB: NoSQL database
- RDS: SQL database

I decided to use RDS because one of my objectives was to learn proper SQL and check out more complex queries (although I am not going to use them in this project, but I will study them).
Just as a note, SQL is normally used for high transaction applications, with complex queries, requiring ACID compliance and without lot of growth (SQL is more expensive to escalate compared to NoSQL). This would normally decide if it is better to choose NoSQL or SQL for a project.

Instead of RDS, I could have used EC2 and installed a database there, but I decided to go for the RDS directly, mainly because AWS already facilitates RDS to use directly as a database and I didn't see the point on spending time on configuring it in a virtual server. The only advantage of using a database in EC2 would be that I would have more control over it, but for my case RDS is just fine.

## ETL
In this section I'm going to discuss the jobs that take part in the Wikipedia Newsletter pipeline:
- RetrieveWikipediaInfo: Retrieves HTML from Wikipedia page and stores it as a txt in S3
- TransformWikipediaInfo: gets previous txt, transforms it and retrieves the five events which will be stored in a CSV in S3. This will have two columns: year and event
- LoadWikipediaInfoSQL: get previous CSV and iterate over it to store the data in a PostgreSQL database

The repository is stored in EC2 which was configured to run "main" file everyday.

An ETL could be summarised as the following
Understand stakeholder problem -> Data exploration (volume, granularity and frequency of data) -> Data modeling (how output looks like) -> Data transformation (filter, standarize, aggregate) -> Data quality (trends, missing data)

I have considered this advice when developing my project.

Some other points that I have learned while developing this project:
- If we had to add data to the database everyday, we would do it incrementally, based on the last time the system extracted data.
Most incremental extract scenarios use a last date modified/timestamp column.
- If you’re extracting during the day/normal business hours, your extract queries can’t disrupt the existing OLTP processes (transactions).
- Capturing Periodic Snapshots of Data is essential to achieve Durability (ACID)
- Coming up with messaging and alert procedures so that any fatal error or verification failure triggered phone calls

### Logs
I learned that logging is a top task that has to be perfomred in Data Engineering. There are lots of events that should be logged:
- Start and stop events
- Status
- Errors and other exceptions
- Audit information: analysis of rows added for example
- Testing and debugging information

When considering how the logging information will be consumed, consider the following:
- Who is the primary audience for these logs? What other audiences might need access to this information?
- How will the data be reviewed? What format delivers the information in the clearest way possible?
- Are there any security concerns that require user-level data filtering?
- Keep data as long as needed, but not more

## Concepts learned
Finally, I wanted to talk about other concepts learned in this project:

I learned about the 3 Vs (Verity, velocity, and volume).
Basically, volume refers to the amount of data, variety refers to the number of types of data and velocity refers to the speed of data processing. According to the 3Vs model, the challenges of big data management result from the expansion of all three properties, rather than just the volume alone.

Using AWS, we require minimal maintenance. Cloud Service Providers will auto-scale for us and eventually lead to less maintenance and cost. AWS can help us managing the 3Vs until certain point, but it is also important to create optimal pipelines and not to do something that is not needed!
Here is important to ask: do I need to retrieve this data? how often do I need to retrieve it?
In this stage, it is important also to consider the analytics part of it and understand if what we are retrieving is what we really need.

In this case we don't need to worry about these concepts, but it is good to keep them in mind!

---

HA (High Availability): A Cloud Databases HA instance group includes a source database instance and one or two replicas. If main fails, other will take the place until main is restored. It is important to create plan B, C, D in case something bad happens. We have to consider all possible failure scenarios. AWS facilitates snapshots, but we have to be proactive and do constant backups of our data (enough data to fix something if it recently failed, but not too much data that would conflict with the 3 Vs (volume in particular). Keep data as long as needed, but not more)

---

To have optimal transaction control, a database system must be ACID compliant, which stands for the following properties: Atomicity, Consistency, Isolation, Durability

**Atomicity**: We can't send a transaction that is half complete. If it stops at the middle of the operation, it will not be done. 

**Consistency**: All data must be consistent after every transaction. It has to follow the rules and constraints established.

**Isolation**: Each transaction must occur independently of other transactions occurring at the same time.

**Durability**: Committed transactions must be fully recoverable in all but the most extreme circumstances. Durability can be achieved by using logs in every possible action performed

In my case, I am doing five inserts in a table each day (one for each of the events displayed). A good method to deal with Atomicity would be to make sure that the five insertions have been completed successfully. We don't want to have this task completed at half.
In order to achieve Durability we would need to log every transaction made. Consistency and Isolation are already achieved.

---

**STAR schema**
STAR schema is the most widely approach used to develop data warehouses. It is divided into:
- Fact tables: contain the measures that users want to aggregate. E.g a sale that includes customerId, dateId, productSoldId, cost
- Dimension tables contain the master table business entities. E.g. there is a table for customer information with columns: customerId, customerName, customerLastName, customerAddress
- We link fact tables with dimension tables via a key. In the example above we would use customerId to link both

---

**Staging step**
A staging area, or landing zone, is an intermediate storage area used for data processing during the extract, transform and load (ETL) process. The data staging area sits between the data source and the data target, which are often data warehouses.

In our case, we only had one table but in more complex project we would need a something in between to the source and the target.

## Conclusion
A summary, as I developed this project I learned a lot of new concepts that were unknown to me before. I am happy that I manage to complete the project and that I learned about AWS (which I was looking to use it since some time ago). Their free tier allows to build almost anything you can think about, so I will start thinking about the next project I want to do! I am sure it will be something more complex and challenging since I now have already the basis of Data Engineering!

Thanks for reading

