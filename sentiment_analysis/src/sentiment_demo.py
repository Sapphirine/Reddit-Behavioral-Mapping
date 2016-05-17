"""
IMPORTANT: update path to database.  On my setup, I have a NFS mounted 
at /data that has my database in it.
"""
DATABASE_PATH = "/data/Reddit2.db"

# Tools for sentiment analysis
from sentiment import sentiment

# Spark stuff
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("Reading Ease")
sc = SparkContext(conf=conf)

# Load and initialize the Context to handle SQL
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load database into dataframe
DATABASE_ENGINE = "jdbc:sqlite:"
Threads_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Threads').load()
Comments_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Comments').load()
Threads_df.registerTempTable("Threads")
Comments_df.registerTempTable("Comments")

# Subreddit
SUBREDDIT = "'The_Donald'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentBodies = SubCommentBodies.filter(lambda x: not(x[0].startswith('http')))
SubCommentScores = SubCommentBodies.map(lambda x: sentiment(x[0]))
# Calculate mean
print "Mean sentiment value for /r/The_Donald: %1.2f" % SubCommentScores.mean()

# Subreddit
SUBREDDIT = "'SandersForPresident'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentBodies = SubCommentBodies.filter(lambda x: not(x[0].startswith('http')))
SubCommentScores = SubCommentBodies.map(lambda x: sentiment(x[0]))
# Calculate mean
print "Mean sentiment value for /r/SandersForPresident: %1.2f" % SubCommentScores.mean()

# Subreddit
SUBREDDIT = "'hillaryclinton'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentBodies = SubCommentBodies.filter(lambda x: not(x[0].startswith('http')))
SubCommentScores = SubCommentBodies.map(lambda x: sentiment(x[0]))
# Calculate mean
print "Mean sentiment value for /r/hillaryclinton: %1.2f" % SubCommentScores.mean()

# Subreddit
SUBREDDIT = "'Kanye'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentBodies = SubCommentBodies.filter(lambda x: not(x[0].startswith('http')))
SubCommentScores = SubCommentBodies.map(lambda x: sentiment(x[0]))
# Calculate mean
print "Mean sentiment value for /r/Kanye: %1.2f" % SubCommentScores.mean()

# Subreddit
SUBREDDIT = "'UpliftingNews'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentBodies = SubCommentBodies.filter(lambda x: not(x[0].startswith('http')))
SubCommentScores = SubCommentBodies.map(lambda x: sentiment(x[0]))
# Calculate mean
print "Mean sentiment value for /r/UpliftingNews: %1.2f" % SubCommentScores.mean()