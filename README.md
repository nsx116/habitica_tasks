# Habitica Tasks Exporter

This script retrieves your daily and to-do tasks from the `habitica-user-data.json` file and outputs them as a `.md` (Markdown) file.

## Prerequisites

Before running the script, make sure you have:

- Python 3 installed.
- Your `habitica-user-data.json` file, which contains your Habitica user data.

### Getting the `habitica-user-data.json` File

To get your `habitica-user-data.json` file:

1. Log in to your Habitica account.
2. Go to [Settings → Site Data → Your User Data](https://habitica.com/user/settings/siteData).
3. Click **Learn More** under **User Data** and then click **Download as JSON**.

Alternatively, you can also follow these steps:
- Click on your user icon in the top right corner of the main page.
- Navigate to **Settings → Site Data**.
- Click **Learn More** under **User Data** and then click **Download as JSON**.
- In the **Your User Data** section, click **Download as JSON**.

## How to Use the Script

1. Place the script (`habitica_tasks.py`) and the `habitica-user-data.json` file in the same folder.
2. Run the script using the following command:

   ```bash
   python3 habitica_tasks.py

This will generate a tasks.md file with your tasks in Markdown format.
