The script retrieves dailys and todos from habitica-user-data.json and prints
them as .md file. Put the script and habitica-user-data.json to the same 
folder and run: python3 habitica_tasks.py. Output file's name is tasks.md. If
you want to retrieve data for particular month of a year, uncomment specified
line in merge_and_write(habitica_data_file) function below.

To get habitica-user-data.json: login to your habitica and download 
your user data as json by the link: https://habitica.com/user/settings/siteData, 
or:
User icon in top right of main page - Settings - Site Data - Your User Data - 
Click Learn More - User Data - Download as JSON
