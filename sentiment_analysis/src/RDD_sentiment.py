from sentiment import sentiment

# Subreddit
SUBREDDIT = "'The_Donald'"

# Spark stuff
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("Reading Ease")
sc = SparkContext(conf=conf)

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

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentBodies = SubCommentBodies.filter(lambda x: not(x[0].startswith('http')))
SubCommentScores = SubCommentBodies.map(lambda x: sentiment(x[0]))
# Calculate mean
print SubCommentScores.mean()