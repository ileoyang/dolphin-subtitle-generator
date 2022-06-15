# Dolphin Subtitle Generator

## Prerequisites

* [Python](https://www.python.org/) (3.6+) and [pip](https://pip.pypa.io/)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [FFmpeg](https://ffmpeg.org/)

## Quickstart

```shell
# The test OS is Ubuntu 20.04
$ aws configure  # Enter AWS configurations (access key ID, secret access key, region name)
$ git clone https://github.com/ileoyang/dolphin-subtitle-generator.git  # Download this repository
$ cd dolphin-subtitle-generator
# In config.yaml, fill in the name of the S3 bucket for storing video-related files
dolphin-subtitle-generator$ pip3 install -r requirements.txt  # Install Python packages
dolphin-subtitle-generator$ python3 dolphin.py [path of your video]  # Start the subtitle generator
# After processing, a video with subtitles will be generated in the directory of the input video
```