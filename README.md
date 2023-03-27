
Youget - Application for downloading Youtube videos in mp3 and mp4 files

Author: Kyo young Lim
Email: limkyouyou@gmail.com

This application is a free and easy to use youtube videos mp3/mp4 downloader. It is developed as a personal project and although the application is developed for multiple users in mind, it is not intended to be hosted on public domain. 

The Youget project is developed on Django framework and it uses yt-dlp Python module, a youtube_dl fork, to retrieve information and files from Youtube videos. Different models are implemented for its database to store information about the Youtube video and qualities selected by the users. This database helps to summarize what kind of videos and qualities are popular downloads among the users. It also helps to keep track of when the files are downloaded to the server so that the old files can be deleted after some times have passed in order to free up storage in the server. Invalid Youtube URL will be flagged with an error message and the application will not process the url further. Youtube video titles wich contains restricted characters and words for operating system filenames are altered to meet the standards.

To begin using Youget, the user will first enter a valid Youtube video URL, choose a format between mp3 or mp4 then click on 'Process' button. On the next page, if the user chose mp3 file, the application will present two quality options between 128kbps and 320kbps. Whichever option is selected, the application will download the best audio quality available from the target Youtube video then convert it to the quality the user selected. If the user chose mp4, the user will be given all the available video resolutions from the target Youtube video in 480p, 720p, 1080p and up, including all the available codecs for the each resolution. The video's best audio quality available will be selected by default. Note that even though some of the options available are in webm video format, these files will be converted into mp4 format in the end. When the user selects a quality and click on 'Prepare' button, the application will start downloading the file to the server. When the file is downloade, the application will present a 'Download' button to the user which upon clicking it, the application will start downloading the file to the user computer. If needed, the user can reselect a new quality to the same Youtube video then go through the same process to download the file.

If you have any questions or suggestions, feel free to contact me by my email.

loading gif created from https://loading.io/

favicon created from https://favicon.io/