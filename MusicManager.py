from win10toast import ToastNotifier
import pafy, vlc, time, feedparser, random

class Player:

    def __init__(self, volume=50):
        self.volume = volume
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()

    def _PlayUrl(self, url):
        video = pafy.new(url)
        best = video.audiostreams[0]
        length = video.length
        title = video.title
        author = video.author
        return best.url, length, title, author

    def _notify(self, title, msg):
        toaster = ToastNotifier()
        toaster.show_toast(title, msg, icon_path='YouTube.ico', duration=10, threaded=True)

    def play(self, url):

        playurl, length, title, author = self._PlayUrl(url)

        Media = self.Instance.media_new(playurl)
        Media.get_mrl()
        self.player.set_media(Media)


        print('Playing\n'+title)
        self._notify('YouTube Radio', title+'\nby '+author)
        self.player.play()
        vlc.libvlc_audio_set_volume(self.player,self.volume)
        time.sleep(length)

class YouTube():

    def __init__(self, channels=None):
        self.channels = channels

    def getvideos(self, channels):

        if type(channels) == str:
            channel_feed = "https://www.youtube.com/feeds/videos.xml?channel_id="+channels
            feed = feedparser.parse(yt_feed)
            allvideos = [video['id'].replace("yt:video:", "") for video in feed['entries']]
        else:

            allvideos = []

            for channel in channels:

                videos = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id="+channel)['entries']
                for video in videos:
                    allvideos.append(video['id'].replace("yt:video:", ""))

        return allvideos

if __name__ == '__main__':

    #Channels
    channels = ['UCJrOtniJ0-NWz37R30urifQ', #Alan Walker
                'UCa10nxShhzNrCE1o2ZOPztg', #Trap Nation
                'UC_aEa8K-EOJ3D6gOs7HcyNg', #NoCopyRightSounds
                ]

    Shuffle = True
    Repeat = True

    player = Player()
    youtube = YouTube()

    while True:

        if Shuffle:
            random.shuffle(channels)

        videos = youtube.getvideos(channels)

        print('total videos', len(videos))

        if Shuffle:
            random.shuffle(videos)

        for video in videos:
                player.play(video)

        if not Repeat:
            break
