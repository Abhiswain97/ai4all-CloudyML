from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

import pandas as pd

getDriverPath = (
    lambda: "C:\\Users\\abhi0\\Downloads\\geckodriver-v0.30.0-win64\\geckodriver.exe"
)

firefoxService = Service(executable_path=getDriverPath())

driver = webdriver.Firefox(service=firefoxService)
driver.get(url="https://www.covid19india.org/")

try:
    WebDriverWait(driver=driver, timeout=15).until(
        expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, "level-vaccinated")
        )
    )
except TimeoutException:
    driver.quit()

summary = driver.find_element(by=By.CLASS_NAME, value="Level").text

cases = list(
    filter(
        lambda x: not x.startswith("+"),
        list(map(lambda x: x.strip(), summary.split("\n"))),
    )
)

full_summary = {
    "Current-Cases": cases[1],
    "Active-Cases": cases[3],
    "Recovered-Cases": cases[5],
}

table = driver.find_element(by=By.CLASS_NAME, value="Table").text
table = table.split("\n")[2:]

data_list = list(filter(lambda x: not ord(x[0]) == 8593, table))

columns = data_list[:7]

new_data_list = data_list[7:]


states_ut = [new_data_list[s] for s in range(0, len(new_data_list), 7)]
confirmed = [new_data_list[s] for s in range(1, len(new_data_list), 7)]
active = [new_data_list[s] for s in range(2, len(new_data_list), 7)]
recovered = [new_data_list[s] for s in range(3, len(new_data_list), 7)]
deceased = [new_data_list[s] for s in range(4, len(new_data_list), 7)]
tested = [new_data_list[s] for s in range(5, len(new_data_list), 7)]

df = pd.DataFrame(
    {
        "State/UT": states_ut,
        "Confirmed": confirmed,
        "Active": active,
        "Recovered": recovered,
        "Deceased": deceased,
        "Tested": tested,
    }
)
df.to_csv("covid19india.csv", index=False)

driver.quit()
