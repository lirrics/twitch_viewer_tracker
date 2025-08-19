# twitch_viewer_tracker
A Python script to monitor and log Twitch channel chatters over time using the Twitch Helix API


This script snapshots all current chatters in a given channel at regular intervals, logs statistics, and builds a final roster of everyone who appeared during the session.<br><br>


__Features__

- Connects to the Twitch Helix API

- Automatically refreshes OAuth tokens if expired

- Snapshots all chatters in a channel at a configurable interval

- Logs chatter counts over time in JSONL format

- Exports a final roster of unique chatters with their first/last seen timestamps<br><br>

__Output__

<ins>chatters_YYYY-MM-DD.jsonl</ins>

JSON file outputted containing the timestamps and user count.

<ins>chatters_YYYY-MM-DD_roster.json</ins>

JSON file outputted of all viewers with details such as user id, username, first seen and last seen.<br><br>

__Prequisites__

- Python 3.8+

- 'requests' library -
*`pip install requests`*
- Twitch Application (Developer Console) and relevant details.<br><br>

<ins>Creating Twitch Application</ins>

1. https://dev.twitch.tv/console
2. Applications on left-hand pane
   > Name: YOUR_APPLICATION_NAME
   
   > OAuth Redirect URLs: http://localhost
   
   > Client Type: Confidential
3. Create
4. Click Manage on your created application
5. Note down Client ID and Client Secret (click New Secret)<br><br>

<ins>Authorising Application</ins>

1. Navigate to the following URL but change YOUR_CLIENT_ID to your noted down client ID.

   https://id.twitch.tv/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost&response_type=code&scope=chat:read+chat:edit+moderator:read:chatters

2. Authorize the request
3. The site won't be reachable as it's routing to a non-existent web server. Note down the code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx value in the URL bar of your browser.
4. Enter the following command in a terminal, replacing YOUR_CLIENT_ID, YOUR_CLIENT_SECRET and URL_CODE with your values.
   
   *`curl -X POST "https://id.twitch.tv/oauth2/token" -d "client_id=YOUR_CLIENT_ID" -d "client_secret=YOUR_CLIENT_SECRET" -d "code=URL_CODE" -d "grant_type=authorization_code" -d "redirect_uri=http://localhost"`*
   
6. Note down the access_token and refresh_token values returned.

<ins>Retrieving User ID</ins>

1. Enter the following command into a terminal, replacing YOUR_CLIENT_ID, YOUR_ACCESS_TOKEN and USERNAME with your values

   *`curl -H "Client-ID: YOUR_CLIENT_ID" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -X GET "https://api.twitch.tv/helix/users?login=USERNAME"`*

2. Note down your User ID<br><br>

<ins>Final Steps</ins>

You now have all the information required to customize the python script to your own.

1. Open the Python script in your chosen code editor.
2. At the top of the script, replace the following with your own values.

CLIENT_ID
CLIENT_SECRET
USER_ID
ACCESS_TOKEN 
REFRESH_TOKEN

3. Now simply start up your stream and open a terminal.
4. Navigate the directory where the python script is stored.
5. Run *`py twitch_viewer_tracker`*
6. When your stream ends simply CTRL+C the terminal and find your outputted files in the same folder the python script is stored.




  



