# Redditor username
REDDITOR = "'moonsprite'"

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

#Redditors_Comments = sqlContext.sql("SELECT thread_id FROM Comments WHERE Comments.author={}".format(REDDITOR))
Redditors_Comments = sqlContext.sql("SELECT subreddit FROM Threads INNER JOIN Comments ON Comments.thread_id=Threads.id WHERE Comments.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Threads  = sqlContext.sql("SELECT subreddit FROM Threads WHERE Threads.author={}".format(REDDITOR)).rdd.map(lambda x: x[0])
Redditors_Subs     = Redditors_Threads.union(Redditors_Comments).distinct()
print Redditors_Subs.collect()