import os
import subprocess
import sys
import time
import uuid

import boto3
import yaml


def upload_video():
    """
    Upload the video to S3 Bucket.
    """
    s3_client = boto3.client("s3")
    # Create the bucket if not exists (idempotent).
    s3_client.create_bucket(Bucket=s3_bucket_name)
    s3_client.upload_file(video_path, s3_bucket_name, uniq_id)


def get_subtitle():
    """
    Get the subtitle from the video by Amazon Transcribe.
    """
    transcribe_client = boto3.client("transcribe")
    transcribe_client.start_transcription_job(
        TranscriptionJobName=uniq_id,
        Media={
            'MediaFileUri': f"s3://{s3_bucket_name}/{uniq_id}"
        },
        OutputBucketName=s3_bucket_name,
        OutputKey=uniq_id,
        LanguageCode='en-US',
        Subtitles={
            'Formats': [
                'srt'
            ],
            'OutputStartIndex': 1
        }
    )
    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=uniq_id)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("In progress...")
        time.sleep(5)
    s3_client = boto3.client("s3")
    # Download the generated subtitle file from S3 Bucket.
    s3_client.download_file(s3_bucket_name, f"{uniq_id}.srt", f"{video_path_prefix}.srt")


def burn_subtitle():
    """
    Burn the subtitle to generate a new video.
    """
    cmd = f"ffmpeg -i {video_path} -filter:v subtitles={video_path_prefix}.srt {video_path_prefix}-sub.mp4"
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python dolphin.py [video path]")
        sys.exit()
    video_path = sys.argv[1]
    video_path_prefix = os.path.splitext(video_path)[0]
    # Use a unique id to identify files to avoid collisions.
    uniq_id = uuid.uuid4().hex
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        s3_bucket_name = config["s3-bucket-name"]
    upload_video()
    get_subtitle()
    burn_subtitle()
