import json
import subprocess
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def navigate_to_next_page(driver):
    """
    Navigate to the next wish page
    :param driver: the driver
    :rtype: str
    """
    selector = "to-next"
    element = driver.find_element(By.CLASS_NAME, selector)
    element.click()
    time.sleep(1.5)
    return get_current_page_number(driver)


def get_current_page_number(driver):
    navigation_buttons = driver.find_elements(By.CLASS_NAME, "page-item")
    assert len(navigation_buttons) == 3
    page_number = navigation_buttons[1].text
    return page_number


def get_table(driver):
    """
    Get wishes in the table
    :param Webdriver driver:
    :return:
    """
    selector = "log-item-row"
    wish_rows = driver.find_elements(By.CLASS_NAME, selector)

    res = []
    for row in wish_rows:
        res.append(
            {
                "item_type": row.find_element(By.CLASS_NAME, "type").text,
                "wish_item_name": row.find_element(By.CLASS_NAME, "name").text,
                "wish_type": row.find_element(By.CLASS_NAME, "wish").text,
                "time_receive": row.find_element(By.CLASS_NAME, "time").text
            },
        )
    return res


def switch_banner_page(driver, banner):
    options = {
        "event": 301,
        "weapon": 302
    }
    if banner not in options:
        raise Exception("Unrecognized banner")
    banner_id = options[banner]
    dropdown = driver.find_element(By.CLASS_NAME, "selected-val")
    dropdown.click()
    time.sleep(0.5)

    driver.find_element(By.CLASS_NAME, f"item[data-id='{banner_id}']").click()
    time.sleep(0.5)


def get_wishes(wish_url, banner="character"):
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.minimize_window()
    driver.get(wish_url)
    time.sleep(4)
    current_page_number = get_current_page_number(driver)
    last_page_number = ""
    
    if banner != "character":
        switch_banner_page(driver, banner)

    wish_list = []
    while current_page_number != last_page_number:
        if int(current_page_number) % 5 == 0:
            print("parsing page: " + current_page_number)
        page_wishes = get_table(driver)
        wish_list.extend(page_wishes)
        last_page_number, current_page_number = current_page_number, navigate_to_next_page(driver)
        time.sleep(1)
    driver.close()
    return wish_list


def get_five_star_weapon_list():
    driver = get_driver()
    URL = "https://genshin-impact.fandom.com/wiki/Category:5-Star_Weapons"
    driver.get(URL)

    elements = driver.find_elements(By.CLASS_NAME, "category-page__member")

    weapon_list = []
    for element in elements:
        weapon_name = element.text
        weapon_list.append(weapon_name)
    driver.close()
    return weapon_list


def parse_wish_json(json_data):
    FIVE_STAR_WEAPON_PREFIXES = get_five_star_weapon_list()
    total_rolls = 0
    five_star_count = 0
    for wish in reversed(json_data):
        five_star_count += 1
        total_rolls += 1
        item_type = wish['item_type']
        item_name = wish['wish_item_name'].split("(")[0].strip()
        if item_type == "Character":
            if "5" in item_name:
                print(item_name, ":", five_star_count, "rolls")
                five_star_count = 0
        elif item_type == "Weapon":
            if "5" in item_name or item_name in FIVE_STAR_WEAPON_PREFIXES:
                print(item_name, ":", five_star_count, "rolls")
                five_star_count = 0

    print("Pity count", ":", five_star_count)
    print("Total rolls in history", ":", total_rolls)


def get_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.minimize_window()

    return driver


if __name__ == '__main__':
    wish_json_data = ""

    if len(sys.argv) >= 2:
        command = sys.argv[1]
        if len(sys.argv) == 2:
            if command == "PARSE_JSON":
                with open("wish_data.json", 'r') as f:
                    data = json.load(f)
                    parse_wish_json(data)
        elif len(sys.argv) >= 3:
            arg = sys.argv[2]
            if command == "PARSE_URL":
                wish_json_data = get_wishes(arg)
                parse_wish_json(wish_json_data)
            elif command == "BANNER":
                raw_output = subprocess.check_output('powershell.exe -ExecutionPolicy Bypass -File ./get_wish_link.ps1')
                url = raw_output.decode()
                wish_json_data = get_wishes(url, banner=arg)
                parse_wish_json(wish_json_data)

    elif len(sys.argv) == 1:
        raw_output = subprocess.check_output('powershell.exe -ExecutionPolicy Bypass -File ./get_wish_link.ps1')
        url = raw_output.decode()
        wish_json_data = get_wishes(url)
        parse_wish_json(wish_json_data)

    if wish_json_data:
        with open("wish_data.json", "w") as f:
            json.dump(wish_json_data, f, indent=4)
