from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET
import argparse

#main function
def download_podcasts(podcast_rss, write_folder='/', use_episode_titles_as_filename=False):
    """
    Download podcasts to a local folder. 
    Parameters
    - podcast_rss (str): the address of the podcast's rss xml file
    - write_folder (str): the local folder to save the files in
    - use_episode_titles_as_filename(bool): if true, use the episode titles (which can be more readable) as the filenames
    """

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
        fname = title+Path(url).suffix if use_episode_titles_as_filename == True else Path(url).name
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
            else:
                print('Done')

if __name__ == "__main__":

    # handle command line args
    parser = argparse.ArgumentParser(description="Download podcast files to a speicified folder.")
    parser.add_argument("podcast_rss", help="xml file of the podcast rss feed")
    parser.add_argument("-f","--folder", help="folder to save the podcasts in")
    parser.add_argument("-t","--titles_as_filename",action="store_true", help="use episode titles as filenames")
    args = parser.parse_args()

    podcast_rss = args.podcast_rss
    kwargs = {}
    if args.folder:
        kwargs['write_folder'] = args.s3_model_artifact
    if args.folder:
        kwargs['use_episode_title_as_filename'] = True

    download_podcasts(podcast_rss, **kwargs)


