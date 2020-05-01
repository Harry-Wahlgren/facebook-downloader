import requests
from yaspin import yaspin
import argparse
import datetime
import time
import sys
import re

def main():
    regex = re.compile(r"([hs]d)_src:\"(.*?)\"")
    my_parser = argparse.ArgumentParser(description='Download Facebook videos')
    my_parser.add_argument('Url',
                       metavar='url',
                       type=str,
                       help='the url to the video')
    args = my_parser.parse_args()
    inputUrl = args.Url

    with yaspin(text="Processing source code", color="green") as sp:
        try:
            r = requests.get(inputUrl)
        except:
            sp.color = "red"
            sp.fail("x")
            sp.write("Failed processing source code")
            sys.exit()
            
        result = re.search(regex, r.text)
        quality = result.group(1)
        url = result.group(2)
        sp.ok("✔")

    with yaspin(text="Downloading video", color="green") as sp:
        try:
            download = requests.get(url)
        except:
            sp.color = "red"
            sp.fail("x")
            sp.write("Failed downloading video")
            sys.exit()
        sp.ok("✔")
    
    title = str(datetime.datetime.now().strftime('%m%d%y%H:%M:%S')) + quality

    with yaspin(text="Writing file", color="green") as sp:
        try:
            with open(f'./{title}.mp4', "wb") as f:
                f.write(download.content)
        except:
            sp.color = "red"
            sp.fail("x")
            sp.write("Failed writing file")
            sys.exit()
        sp.ok("✔")

main()