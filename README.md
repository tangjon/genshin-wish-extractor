# Genshin Wish Parser
Extract your wish history and display your rolled 5 stars and current pity count in history.

# Setup
1. https://chromedriver.chromium.org/downloads. Download the latest chrome driver version that matches your current chrome.
   Place `chromedriver.exe` in somewhere like `C:/chromedriver/`
2. Add the path of chromedriver.exe to path so our Python script can use the chromedriver.
3. Run `pip install -r requirements.txt` to install Python dependencies.
4. Next Run `python main.py`. If everything is good you should have some output like
```
Keqing (5-Star) : 57 rolls
Pity count : 65
Total rolls in history : 122
```

# Files
- get_wish_link.ps1: This is a powershell script that goes into your Genshin logs to extract a link to your wish history.
  i.e `C:\Users\<user>\AppData\LocalLow\miHoYo\Genshin Impact\output_log.txt`. You can open that file and find the link yourself.
  It is almost as if the wish history Window in game is a web browser.
- json_data.json: This is a generated file with a JSON list of your wish history.