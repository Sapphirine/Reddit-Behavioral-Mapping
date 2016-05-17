# Tools for reading comprehension
from textstat.textstat import textstat

# Spark stuff
from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("Reading Ease")
sc = SparkContext(conf=conf)

# Load and initialize the Context to handle SQL
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load database into dataframe
DATABASE_PATH = "/home/marshall/Dropbox/OneDrive/Documents/Columbia/AdvancedBigDataAnalytics/project/database/src/Reddit2.db"
DATABASE_ENGINE = "jdbc:sqlite:"
Threads_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Threads').load()
Comments_df = sqlContext.read.format('jdbc').options(url=''.join([DATABASE_ENGINE, DATABASE_PATH]), dbtable='Comments').load()
Threads_df.registerTempTable("Threads")
Comments_df.registerTempTable("Comments")

# Get threads for one subreddit
TrumpThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit='The_Donald'")
TrumpThreads.registerTempTable("trumpThreads")

# Get all comment bodies from comments in /r/The_Donald
TrumpCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN trumpThreads ON trumpThreads.id=Comments.thread_id")

TrumpCommentBodies.foreach(lambda x: print(type(x)))