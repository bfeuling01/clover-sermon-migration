# Sermon Migration

Python script to migrate sermons from Clover to Sermon Audio

## REQUIREMENTS

1. Install Beautiful Soup (bs4)
2. Add the Sermon API key to API_KEY
3. Add the URL for the site that hosts the sermons to download in SOURCE_URL

## OVERVIEW

If you are using Clover to host your sermons and are wanting to move them over to SermonAudio, this script will migrate those sermons for you

## SPECIFICS

The script will:
1. Reach out to the designated Sermon Hosting site that uses Clover as the file storer
2. Scrape the site for potential endpoints that the sermons are located at
3. Pull the metadata for each sermon
4. Download the sermon
5. Create the sermon in Sermon Audio
6. Upload the video to Sermon Audio

## EXCEPTIONS

- If there are any issues in getting the video or information about the video, the script will show an EXCEPTION in the output.
The user will need to manual upload those sermons to Sermon Audio as a result
- When the script is done, or as it is being run, you will need to manually delete the downloaded videos after they have been uploaded
