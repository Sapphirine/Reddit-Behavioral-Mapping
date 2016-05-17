"""
Find subreddit relations based on user posting history
"""

"""
IMPORTANT: update path to database.  On my setup, I have a NFS mounted 
at /data that has my database in it.
"""
DATABASE_PATH = "/data/Reddit2.db"

# Spark stuff
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("Reading Ease")
sc = SparkContext(conf=conf)
from operator import add

# Load and initialize the Context to handle SQL
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load database into dataframe
DATABASE_ENGINE = "jdbc:sqlite:"
Threads_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Threads').load()
Comments_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Comments').load()
Threads_df.registerTempTable("Threads")
Comments_df.registerTempTable("Comments")

# Analyze /r/The_Donald
SUBREDDIT = "'The_Donald'"

# Get Redditors
Trump_Thread_Authors = sqlContext.sql("SELECT author FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Trump_Comment_Authors = sqlContext.sql("SELECT Comments.author FROM Comments INNER JOIN Threads ON Threads.id=Comments.thread_id WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Trump_Authors = Trump_Thread_Authors.union(Trump_Comment_Authors).distinct().map(lambda x: str(x[0])).collect()

Trump_Thread_Subs = sqlContext.sql("SELECT subreddit FROM Threads WHERE author IN {}".format(str(tuple(Trump_Authors)))).rdd
Trump_Comment_Subs = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author IN {}".format(str(tuple(Trump_Authors)))).rdd
Trump_Subs = Trump_Thread_Subs.union(Trump_Comment_Subs).map(lambda x: (x[0], 1)).filter(lambda x: x[0] != 'The_Donald')

Trump_Sub_Count = sorted(Trump_Subs.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

# Print top 10 subs for Trump
print "15 most closely related subs to /r/The_Donald:"
for subcount in Trump_Sub_Count[:15]:
    print subcount
print " "

# Analyze /r/SandersForPresident
SUBREDDIT = "'SandersForPresident'"

# Get Redditors
Sanders_Thread_Authors = sqlContext.sql("SELECT author FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Sanders_Comment_Authors = sqlContext.sql("SELECT Comments.author FROM Comments INNER JOIN Threads ON Threads.id=Comments.thread_id WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Sanders_Authors = Sanders_Thread_Authors.union(Sanders_Comment_Authors).distinct().map(lambda x: str(x[0])).collect()

Sanders_Thread_Subs = sqlContext.sql("SELECT subreddit FROM Threads WHERE author IN {}".format(str(tuple(Sanders_Authors)))).rdd
Sanders_Comment_Subs = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author IN {}".format(str(tuple(Sanders_Authors)))).rdd
Sanders_Subs = Sanders_Thread_Subs.union(Sanders_Comment_Subs).map(lambda x: (x[0], 1)).filter(lambda x: x[0] != 'SandersForPresident')

Sanders_Sub_Count = sorted(Sanders_Subs.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

# Print top 10 subs for Sanders
print "15 most closely related subs to /r/SandersForPresident:"
for subcount in Sanders_Sub_Count[:15]:
    print subcount
print " "

# Analyze /r/hillaryclinton
SUBREDDIT = "'hillaryclinton'"

# Get Redditors
Clinton_Thread_Authors = sqlContext.sql("SELECT author FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Clinton_Comment_Authors = sqlContext.sql("SELECT Comments.author FROM Comments INNER JOIN Threads ON Threads.id=Comments.thread_id WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Clinton_Authors = Clinton_Thread_Authors.union(Clinton_Comment_Authors).distinct().map(lambda x: str(x[0])).collect()

Clinton_Thread_Subs = sqlContext.sql("SELECT subreddit FROM Threads WHERE author IN {}".format(str(tuple(Clinton_Authors)))).rdd
Clinton_Comment_Subs = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author IN {}".format(str(tuple(Clinton_Authors)))).rdd
Clinton_Subs = Sanders_Thread_Subs.union(Clinton_Comment_Subs).map(lambda x: (x[0], 1)).filter(lambda x: x[0] != 'hillaryclinton')

Clinton_Sub_Count = sorted(Clinton_Subs.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

# Print top 10 subs for Clinton
print "15 most closely related subs to /r/hillaryclinton:"
for subcount in Clinton_Sub_Count[:15]:
    print subcount
print " "

# Analyze /r/Kanye
SUBREDDIT = "'Kanye'"

# Get Redditors
Kanye_Thread_Authors = sqlContext.sql("SELECT author FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Kanye_Comment_Authors = sqlContext.sql("SELECT Comments.author FROM Comments INNER JOIN Threads ON Threads.id=Comments.thread_id WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd
Kanye_Authors = Kanye_Thread_Authors.union(Kanye_Comment_Authors).distinct().map(lambda x: str(x[0])).collect()

Kanye_Thread_Subs = sqlContext.sql("SELECT subreddit FROM Threads WHERE author IN {}".format(str(tuple(Kanye_Authors)))).rdd
Kanye_Comment_Subs = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author IN {}".format(str(tuple(Kanye_Authors)))).rdd
Kanye_Subs = Kanye_Thread_Subs.union(Kanye_Comment_Subs).map(lambda x: (x[0], 1)).filter(lambda x: x[0] != 'Kanye')

Kanye_Sub_Count = sorted(Kanye_Subs.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

# Print top 10 subs for Clinton
print "15 most closely related subs to /r/Kanye:"
for subcount in Kanye_Sub_Count[:15]:
    print subcount
print " "