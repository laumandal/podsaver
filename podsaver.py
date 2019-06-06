from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

podcast_rss = 'http://www2.jfn.co.jp/library/pod/podcast_sl.xml'

write_folder = '/Users/me/Downloads/SL'
# create folder if doesn't exist
Path(write_folder).mkdir(parents=True, exist_ok=True)

feed = urllib.request.urlopen(podcast_rss)

tree = ET.parse(feed)
root = tree.getroot()
channel = root[0]

total_eps = len(channel.findall('item'))

for (idx,episode) in enumerate(channel.findall('item')):
    title = episode.find('title').text
    url = episode.find('enclosure').get('url')
    fname = Path(url).name
    write_path = Path(write_folder).joinpath(fname)
    print(f'Downloading episode {idx+1} of {total_eps}: {title}', end ='...')
    urllib.request.urlretrieve(url, write_path)
    print('Done')

print('All episodes downloaded')
