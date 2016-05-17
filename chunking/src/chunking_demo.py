"""
IMPORTANT: update path to database.  On my setup, I have a NFS mounted 
at /data that has my database in it.
"""
DATABASE_PATH = "/data/Reddit2.db"

# Imports
import nltk
from nltk import pos_tag

# Function to perform chunking
def chunk(text):
    
    try:
        tagged_sent = pos_tag(text.split())
        return [word for word, pos in tagged_sent if pos == 'NNP']
    except:
        return []

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

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

Chunked_Comments = SubCommentBodies.map(lambda x:(1, chunk(x[0]))).filter(lambda x: len(x) > 0).flatMapValues(lambda x: x).map(lambda x: (x[1], x[0]))
Chunked_Count = sorted(Chunked_Comments.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

print "Top 20 proper nouns in /r/The_Donald:"
for x in Chunked_Count[:20]:
    print x
    
# Analyze /r/SandersForPresident
SUBREDDIT = "'SandersForPresident'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

Chunked_Comments = SubCommentBodies.map(lambda x:(1, chunk(x[0]))).filter(lambda x: len(x) > 0).flatMapValues(lambda x: x).map(lambda x: (x[1], x[0]))
Chunked_Count = sorted(Chunked_Comments.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

print "Top 20 proper nouns in /r/SandersForPresident:"
for x in Chunked_Count[:20]:
    print x
    
# Analyze /r/hillaryclinton
SUBREDDIT = "'hillaryclinton'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

Chunked_Comments = SubCommentBodies.map(lambda x:(1, chunk(x[0]))).filter(lambda x: len(x) > 0).flatMapValues(lambda x: x).map(lambda x: (x[1], x[0]))
Chunked_Count = sorted(Chunked_Comments.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

print "Top 20 proper nouns in /r/hillaryclinton:"
for x in Chunked_Count[:20]:
    print x
    
# Analyze /r/Kanye
SUBREDDIT = "'Kanye'"

# Get threads for one subreddit
SubThreads = sqlContext.sql("SELECT * FROM Threads WHERE subreddit={}".format(SUBREDDIT))
SubThreads.registerTempTable("SubThreads")

# Get all comment bodies from comments in /r/The_Donald with more than 100 upvotes
SubCommentBodies = sqlContext.sql("SELECT body FROM Comments INNER JOIN SubThreads ON SubThreads.id=Comments.thread_id WHERE Comments.ups > 100").rdd

Chunked_Comments = SubCommentBodies.map(lambda x:(1, chunk(x[0]))).filter(lambda x: len(x) > 0).flatMapValues(lambda x: x).map(lambda x: (x[1], x[0]))
Chunked_Count = sorted(Chunked_Comments.foldByKey(0, add).collect(), key=lambda x: x[1])[::-1]

print "Top 20 proper nouns in /r/Kanye:"
for x in Chunked_Count[:20]:
    print x