from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

#arguments
podcast_rss = 'http://www2.jfn.co.jp/library/pod/podcast_sl.xml'
write_folder = '/Users/laumandal/Downloads/SL'
use_episode_title_as_filename = True


# create folder if doesn't exist
Path(write_folder).mkdir(parents=True, exist_ok=True)

feed = urllib.request.urlopen(podcast_rss)

tree = ET.parse(feed)
root = tree.getroot()
channel = root[0]

total_eps = len(channel.findall('item'))

print ('*** Starting downloads *** ')
print ('break (ctrl-C or stop button) to stop and continue later')

for (idx,episode) in enumerate(channel.findall('item')):
    title = episode.find('title').text
    url = episode.find('enclosure').get('url')
    fname = title+Path(url).suffix if use_episode_title_as_filename == True else Path(url).name
    write_path = Path(write_folder).joinpath(fname)
    
    if write_path.is_file():
        #don't attempt to redownload existing files
        print(f'Episode {idx+1} of {total_eps}: {title} already downloaded!')
    else:
        #download episode
        print(f'Downloading episode {idx+1} of {total_eps}: {title}', end ='...')
        try:
            urllib.request.urlretrieve(url, write_path)
        except KeyboardInterrupt:
            print ('Cancelled!')
            # Delete partial file and stop downloading
            if write_path.is_file():
                Path(write_path).unlink()
            print('Downloads stopped and partially downloaded file removed.')
            break
            status = "downloads stopped"
        else:
            print('Done')



