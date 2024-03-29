#!/bin/sh

#Copyright 2021 Xailient Inc.
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
#documentation files (the "Software"), to deal in the Software without restriction, including without 
#limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
#of the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or 
#substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
#INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
#AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
#DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# sh sample_videos.sh path_to_videos <every_ith_frame> <framerate>

# Given a folder of videos this script will sample every ith frame
# and create a new videos at a chosen framerate.

# Need ffmpeg and extract_frames_from_videp.py script

mkdir temp_frames || { echo 'Directory temp_frames exists, remove to run this program' ; exit 1; }
mkdir output_videos || { echo 'Directory output_videos exists, remove to run this program' ; rm -r temp_frames; exit 1; }

path_to_vids="$1"
ith="$2"
framerate="$3"

vid_list=$(ls "$path_to_vids")

num_videos=$(ls "$path_to_vids" | wc -l)

count=1
for f in $vid_list ;do
    echo "Video number: $count/$num_videos"
    file_path="$path_to_vids/$f"
    folder_name=$(echo "$f" | sed 's/\.[a-zA-Z]*$//')
    python3 extract_frames_from_videp.py --every "$ith" --output_path "$(pwd)/temp_frames" "$file_path"
    ffmpeg -framerate "$framerate" -i "temp_frames/$folder_name/frame_%d.jpg" "output_videos/$folder_name.mp4"
    count=$((count + 1))
done

rm -r temp_frames