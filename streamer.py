from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials


class TwitterStreamer:
    """Class that streams and processes our live tweets"""
    def stream_tweets(self, filename, hash_tags):
        """This method streams our tweets to a file
        Args:
            filename: name of the file to save the tweets to
            hash_tags: list of hash tags to monitor
        """

        listener = TwitterListener()
        authentication = OAuthHandler(
            twitter_credentials.CONSUMER_KEY,
            twitter_credentials.CONSUMER_SECRET)
        authentication.set_access_token(
            twitter_credentials.ACCESS_TOKEN,
            twitter_credentials.ACCESS_TOKEN_SECRET)

        # Creates an object of the stream class that
        # allows us to be able to pull data from Twitter
        # first arg: the auth object
        # second arg: our listener object
        stream = Stream(authentication, listener)

        # filters the stream based on keywords we want.
        # takes optional keyword arg: track: list of keywords
        # we want to include
        stream.filter(track=hash_tags)


class TwitterListener(StreamListener):
    """Listener class that prints live tweets"""
    def __init__(self, filename):
        self.filename = filename

    def on_data(self, data):
        """If we successfully connect to the Twitter
        feed, stream the content of the data
        Args:
            data: the data from the twitter stream
        """
        try:
            print(data)
            with open(self.filename, 'a') as f:
                f.write(data)
        except BaseException as e:
            print(f"Error on data: {e}")
        return True

    def on_error(self, status):
        """If there's an error, do the content of this
        method with the error
        Args:
            status: the status of the error
        """
        print(status)


if __name__ == '__main__':
    hash_tags = [
        'donald trump',
        'hillary clinton',
        'barrack obama',
        'bernie sanders',
    ]
    filename = 'tweets.json'

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(filename, hash_tags)
