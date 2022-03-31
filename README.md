# Genshin Wish Parser
Extract your wish history and display your rolled 5 stars and current pity count in history locally.

# Setup Environment
1. Have Python 3.9+ installed. (Tested in with Python 3.9)
2. https://chromedriver.chromium.org/downloads. Download the latest chrome driver version that matches your current chrome.
   Place `chromedriver.exe` in somewhere like `C:/chromedriver/`
3. Add the path of chromedriver.exe to Windows System path so our Python script can use the chromedriver. Google how to do so.
4. Run `pip install -r requirements.txt` to install Python dependencies.

# Running the script
1. Start genshin impact and navigate yourself to the wish history screen where you see a table of items. Wish -> History.
2. Next it is time to run our script. Run `python main.py`
   Example output would be:
   ```
   parsing page: 5
   parsing page: 10
   parsing page: 15
   parsing page: 20
   Keqing (5-Star) : 57 rolls
   Pity count : 65
   Total rolls in history : 122
   ```

# Files
- get_wish_link.ps1: This is a powershell script that goes into your Genshin logs to extract a link to your wish history.
  i.e `C:\Users\<user>\AppData\LocalLow\miHoYo\Genshin Impact\output_log.txt`. You can open that file and find the link yourself.
  It is almost as if the wish history Window in game is a web browser.
- json_data.json: This is a generated file with a JSON list of your wish history.