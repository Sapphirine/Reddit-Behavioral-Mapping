# Load and initialize the Context to handle SQL
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load database into dataframe
Threads_df = sqlContext.read.format('jdbc').options(url='jdbc:sqlite:/home/ubuntu/Reddit2.db', dbtable='Threads').load()
Comments_df = sqlContext.read.format('jdbc').options(url='jdbc:sqlite:/home/ubuntu/Reddit2.db', dbtable='Comments').load()
Threads_df.registerTempTable("Threads")
Comments_df.registerTempTable("Comments")

# Get threads for one subreddit
TrumpThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit='The_Donald'")
TrumpThreads.registerTempTable("trumpThreads")

# Get all comment bodies from comments in /r/The_Donald
TrumpCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN trumpThreads ON trumpThreads.id=Comment.thread_id")