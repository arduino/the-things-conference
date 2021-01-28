#!/bin/bash

upload_command="edge-impulse-uploader"
data_folder="data"
output_size=48

if [ -z "$1" ]
then
      echo "Usage: $0 video1.mp4 video2.mp4 ..."
      exit 0
fi

if ! command -v ffmpeg &> /dev/null ;then
	echo "Command 'ffmpeg' could not be found."
	echo "Follow the instructions here https://ffmpeg.org/download.html to install it"
	exit
fi

echo "Do you want to upload the extracted images to Edge Impulse (y/n)?"
read answer

if [ "$answer" != "${answer#[Yy]}" ] ;then	 
	upload=true
	if ! command -v $upload_command &> /dev/null ;then
		echo "Command '$upload_command' could not be found."
		echo "Install the Edge Impulse CLI with: npm install -g edge-impulse-cli"
		exit
	fi
fi

# Create folder which will contain the image assets
mkdir $data_folder

# Process all supplied video files
for inputfile in "$@"
do    
	filename=$(basename -- "$inputfile")
	filename="${filename%.*}"
	mkdir "$data_folder/$filename"

	# Extract frames from video file using ffmpeg
	# Parameters:
	# -ss 00:00:01 Skips the first second
	# -r 5.0 sets a framerate of 5 which is enough to extract different images for training
	# -vf scale=w:h scales the target image down to improve performance
	ffmpeg -i $inputfile -ss 00:00:01 -r 5.0 -vf scale=$output_size:$output_size "$data_folder/$filename/$filename-"%04d.jpg -hide_banner

	# Upload images to Edge Impulse and split them into training and test data
	if [ "$upload" = true ] ; then		
		$upload_command --label $filename --category split "$data_folder/$filename/*.jpg"
	fi	

done
