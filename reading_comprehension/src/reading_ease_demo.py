# Tools for reading comprehension
from textstat.textstat import textstat

def analyze(text):
    
    # Automatically reject if no input
    if text.isspace():
        return -1.0
    if text.startswith('http'):
        return -1.0
    
    # Analyze text
    try:
        x = textstat.flesch_reading_ease(text)
    except:
        return -1.0
    
    # Keep outputs valid
    if not isinstance(x, float):
        return -1.0
    if x < 0:
        return -1.0
    if x > 100:
        return 100.0
    
    return x

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

# Analyze /r/The_Donald
SUBREDDIT = "'The_Donald'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentScores = SubCommentBodies.map(lambda x: analyze(x[0]))
# Remove invalid values
SubCommentScores = SubCommentScores.filter(lambda x: x > 0)
# Calculate mean
print "Flesch Reading Ease score for /r/The_Donald: %2.2f" % SubCommentScores.mean()

# Analyze /r/SandersForPresident
SUBREDDIT = "'SandersForPresident'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentScores = SubCommentBodies.map(lambda x: analyze(x[0]))
# Remove invalid values
SubCommentScores = SubCommentScores.filter(lambda x: x > 0)
# Calculate mean
print "Flesch Reading Ease score for /r/SandersForPresident: %2.2f" % SubCommentScores.mean()

# Analyze /r/hillaryclinton
SUBREDDIT = "'hillaryclinton'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentScores = SubCommentBodies.map(lambda x: analyze(x[0]))
# Remove invalid values
SubCommentScores = SubCommentScores.filter(lambda x: x > 0)
# Calculate mean
print "Flesch Reading Ease score for /r/hillaryclinton: %2.2f" % SubCommentScores.mean()

# Analyze /r/Kanye
SUBREDDIT = "'Kanye'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

# Create new RDD of analyzed values
SubCommentScores = SubCommentBodies.map(lambda x: analyze(x[0]))
# Remove invalid values
SubCommentScores = SubCommentScores.filter(lambda x: x > 0)
# Calculate mean
print "Flesch Reading Ease score for /r/Kanye: %2.2f" % SubCommentScores.mean()