#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import sys

#Variables that contains the user credentials to access Twitter API 
access_token = "1534389271-ck2opVGCmXelDUy80ym8qRNd1cHF6PwtYOxFLWb"
access_token_secret = "N2Xnf92PuesciSJE3F2BLwcrdnrdgvliivBs2AIJRXzEK"
consumer_key = "LIoTnzwswQQxD5k02tovLtZ2v"
consumer_secret = "TB3i1v9GO0WSzJwRNJwuSG1WkUl6FjN20GQNhMqxcWrm8DmpFO"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    #def __init__(self, filepath):
    #    self.outfile = open(filepath,'a')

    def on_status(self, status):
#        print ''.join(("AUTHOR: ", status.author))
        print ''.join(("STATUS: ", status.text))
#        self.outfile.write(status.author)
#        self.outfile.write(status.text)
        return True

    def on_error(self, status):
        print ''(("ERROR: ", status))
#        self.outifle.write(''.join(["|ERROR_START|", status, "|ERROR_END|"]))
        
#    def __del__(self):
#        self.outifle.close()


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[sys.argv[1]])
