#!/bin/bash
echo "Downloading videos from dropbox..."
curl -L -o videos.zip https://www.dropbox.com/sh/3l0doioolhurwdv/AAD_qAuSJM8zjztIhOiveCDBa?dl=1
unzip videos.zip
rm videos.zip
