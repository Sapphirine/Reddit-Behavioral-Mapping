# Download sqlite-jdbc-3.8.11.2.jar in /opt/spark/jars
# Launch pyspark as:
#   SPARK_CLASSPATH=/opt/spark/jars/sqlite-jdbc-3.8.11.2.jar IPYTHON=1 pyspark

# Load and initialize the Context to handle SQL
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load database into dataframe
df = sqlContext.read.format('jdbc').options(url='jdbc:sqlite:/home/ubuntu/Reddit.db', dbtable='Threads').load() # Assuming database is in /home/ubuntu

# Load data from threads into a temporary table to work with
df.registerTempTable("Threads")

# Play with data
results = sqlContext.sql("SELECT id, ups from Threads") # Gives us a PipelinedRDD with two columns, one of type String and the other of type Int 
results.show() # Print Thread ids and number of upvotes
all_ups = results.map(lambda result: result[1]) # Load all upvodes as a PiplinedRDD of ints
all_ups.sum() # Sum all upvotes
all_ups.foreach(lambda up: print up) # Apply function to each element in PiplinedRDD
