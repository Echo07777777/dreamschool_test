import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd


def fetch_exchange_rate(date, currency_code):
    # 创建 Chrome WebDriver 实例
    driver = webdriver.Chrome()

    try:
        # 打开中国银行外汇牌价网站
        driver.get("https://www.boc.cn/sourcedb/whpj/")

        # 等待页面加载完成
        time.sleep(2)

        # 输入起始时间
        date_input = driver.find_element(By.NAME, "erectDate")
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.RETURN)

        # 输入结束时间
        date_input = driver.find_element(By.NAME, "nothing")
        date_input.clear()
        date_input.send_keys(date)
        date_input.send_keys(Keys.RETURN)

        # 找到货币代号输入框并输入货币代码
        currency_input = driver.find_element(By.ID, "pjname")
        currency_input.send_keys(currency_code)
        currency_input.send_keys(Keys.RETURN)

        driver.find_element(By.XPATH, "//*[@id=\"historysearchform\"]/div/table/tbody/tr/td[7]/input").click()

        # 等待页面加载完成
        time.sleep(2)

        # 找到现汇卖出价并获取值
        done = False
        error = False
        while not done and not error:
            for i in range(2, 22):
                try:
                    xpath_expression = "/html/body/div/div[4]/table/tbody/tr[{}]/td[4]".format(i)
                    exchange_rate = driver.find_element(By.XPATH, xpath_expression)
                    rate_text = exchange_rate.text
                    if rate_text:
                        done = True
                        break
                except Exception as e:
                    error = True
                    break
            try:
                driver.find_element(By.CLASS_NAME, "turn_next").click()
            except Exception as e:
                break

        if not done:
            return "not found"

        # 将爬取的数据写入文件
        with open("result.txt", "a") as f:
            f.write(f"Date: {date}\n")
            f.write(f"Currency Code: {currency_code}\n")
            f.write(f"Exchange Rate: {rate_text}\n")

        return rate_text

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # 关闭 WebDriver
        driver.quit()


# 将货币的标准符号转化为货币名称
def change_name(standard_name):
    df = pd.read_csv("name_reference_table.csv", encoding="gbk")
    translation_dict = dict(zip(df["标准名称"], df["中文名称"]))
    chinese_name = translation_dict.get(standard_name, "invalid code")
    return chinese_name


# 将日期转化为以'-'连接的形式
def change_date_format(date):
    formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    return formatted_date


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 fetch_exchange_rate.py <date> <currency_code>")
        sys.exit(1)

    date = sys.argv[1]
    currency_code = sys.argv[2]

    # 转换输入格式
    formatted_date = change_date_format(date)
    chinese_name = change_name(currency_code)

    if chinese_name == "invalid code":
        print("invalid code")
    else:
        exchange_rate = fetch_exchange_rate(formatted_date, chinese_name)
        print(exchange_rate)
