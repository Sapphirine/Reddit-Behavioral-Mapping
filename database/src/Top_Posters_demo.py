# Spark stuff
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("Reading Ease")
sc = SparkContext(conf=conf)
from operator import add

# Load and initialize the Context to handle SQL
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load database into dataframe
DATABASE_PATH = "/home/marshall/Dropbox/OneDrive/Documents/Columbia/AdvancedBigDataAnalytics/EECSE6895_Final_Project/database/src/Reddit2.db"
DATABASE_ENGINE = "jdbc:sqlite:"
Threads_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Threads').load()
Comments_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Comments').load()
Threads_df.registerTempTable("Threads")
Comments_df.registerTempTable("Comments")

# Analyze /r/The_Donald
SUBREDDIT = "'The_Donald'"

Trump_User = sqlContext.sql("SELECT author, score FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd.reduceByKey(add).takeOrdered(1, key=lambda x: -x[1])[0][0].encode("ascii","ignore")
print "Top poster in /r/{} is {}".format(SUBREDDIT.strip(r"'"), Trump_User)

# Analyze most influential poster
REDDITOR = "'{}'".format(Trump_User)

Redditors_Comments = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Threads  = sqlContext.sql("SELECT subreddit FROM Threads WHERE Threads.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Subs     = Redditors_Threads.union(Redditors_Comments).distinct()
print "{}'s subreddits: ".format(Trump_User)
print Redditors_Subs.collect()
print ' '

# Analyze /r/SandersForPresident
SUBREDDIT = "'SandersForPresident'"

Sanders_User = sqlContext.sql("SELECT author, score FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd.reduceByKey(add).takeOrdered(1, key=lambda x: -x[1])[0][0].encode("ascii","ignore")
print "Top poster in /r/{} is {}".format(SUBREDDIT.strip(r"'"), Sanders_User)

# Analyze most influential poster
REDDITOR = "'{}'".format(Sanders_User)

Redditors_Comments = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Threads  = sqlContext.sql("SELECT subreddit FROM Threads WHERE Threads.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Subs     = Redditors_Threads.union(Redditors_Comments).distinct()
print "{}'s subreddits: ".format(Sanders_User)
print Redditors_Subs.collect()
print ' '

# Analyze /r/hillaryclinton
SUBREDDIT = "'hillaryclinton'"

Clinton_User = sqlContext.sql("SELECT author, score FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd.reduceByKey(add).takeOrdered(1, key=lambda x: -x[1])[0][0].encode("ascii","ignore")
print "Top poster in /r/{} is {}".format(SUBREDDIT.strip(r"'"), Clinton_User)

# Analyze most influential poster
REDDITOR = "'{}'".format(Clinton_User)

Redditors_Comments = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Threads  = sqlContext.sql("SELECT subreddit FROM Threads WHERE Threads.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Subs     = Redditors_Threads.union(Redditors_Comments).distinct()
print "{}'s subreddits: ".format(Clinton_User)
print Redditors_Subs.collect()
print ' '

# Analyze /r/Kanye
SUBREDDIT = "'Kanye'"

Kanye_User = sqlContext.sql("SELECT author, score FROM Threads WHERE Threads.subreddit={}".format(SUBREDDIT)).rdd.reduceByKey(add).takeOrdered(1, key=lambda x: -x[1])[0][0].encode("ascii","ignore")
print "Top poster in /r/{} is {}".format(SUBREDDIT.strip(r"'"), Kanye_User)

# Analyze most influential poster
REDDITOR = "'{}'".format(Kanye_User)

Redditors_Comments = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Threads  = sqlContext.sql("SELECT subreddit FROM Threads WHERE Threads.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Subs     = Redditors_Threads.union(Redditors_Comments).distinct()
print "{}'s subreddits: ".format(Kanye_User)
print Redditors_Subs.collect()
print ' '

# Analyze whole dataset
All_User = sqlContext.sql("SELECT author, score FROM Threads").rdd.reduceByKey(add).takeOrdered(1, key=lambda x: -x[1])[0][0].encode("ascii","ignore")
print "Top poster in whole dataset is {}".format(All_User)

if not All_User in [Sanders_User, Trump_User]:

    # Analyze most influential poster
    REDDITOR = "'{}'".format(All_User)

    Redditors_Comments = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
    Redditors_Threads  = sqlContext.sql("SELECT subreddit FROM Threads WHERE Threads.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
    Redditors_Subs     = Redditors_Threads.union(Redditors_Comments).distinct()
    print "{}'s subreddits: ".format(User)
    print Redditors_Subs.collect()
    print ' '