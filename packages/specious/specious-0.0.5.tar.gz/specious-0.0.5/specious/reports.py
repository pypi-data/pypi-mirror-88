import base64
import json
import os
import time
from dataclasses import dataclass
from json import JSONDecodeError
from pathlib import Path
from typing import List

import yagmail
from selenium.webdriver.support.wait import WebDriverWait

from specious import binding

report_template = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>自动化测试执行报告</title>
    <style>
        body {
            background-color: #F3F3F5;
        }
        .content {
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
            border-spacing: 0 20px;
        }
        .stratified {
            font-size:0.80em;
            padding:4px;
        }
        .error {
            font-size:0.80em;
            padding:4px;
            color:red;
        }
        th {
            background-color:#F3F3F5;
            padding:4px;
        }
    </style>
</head>

<body>
    <div>
        <table class="content" align="center" border="0" cellpadding="0" cellspacing="0" width="90%">
            <tbody>
                <tr> </tr>
            </tbody>
        </table>
        <table class="content" bgcolor="#FFFFFF" align="center" border="0" cellpadding="0" cellspacing="0" width="90%">
            <!-- # SUITE -->
            <tr>
                <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="95%">
                        <tr>
                            <td>
                                <table class="stratified" border="1" cellpadding="" cellspacing="" width="100%"
                                    style="border-collapse: collapse;">
                                    <thead>
                                        <tr>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">测试套</p>
                                            </th>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">测试点</p>
                                            </th>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">通过</p>
                                            </th>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">失败</p>
                                            </th>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">阻塞</p>
                                            </th>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">忽略</p>
                                            </th>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">未标识</p>
                                            </th>
                                            <th align="center" width="12.5%">
                                                <p style="margin: 0;">通过率</p>
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {result_row}
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <!-- # GRAPH -->
            <tr>
                <td>
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="95%">
                        <tr>
                            <td>
                                <table class="stratified" border="0" cellpadding="" cellspacing="" width="100%"
                                    style="border-collapse: collapse;">
                                    <tr>
                                        <td align="left">
                                            <img src="data:image/png;base64,{STATUS}" alt="STATUS" width="100%"/>
                                        </td>
                                        <td align="left">
                                            <img src="data:image/png;base64,{SEVERITY}" alt="SEVERITY" width="100%"/>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td align="left">
                                            <img src="data:image/png;base64,{DURATION}" alt="DURATION" width="100%"/>
                                        </td>
                                        <td align="left">
                                            <img src="data:image/png;base64,{TREND}" alt="TREND" width="100%"/>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        <table class="content" align="center" border="0" cellpadding="0" cellspacing="0" width="90%">
            <tbody><tr> </tr></tbody>
        </table>
    </div>
</body>
</html>
"""

row_template = """
<tr>
    <td align="center">
        <p style="margin: 0;">{name}</p>
    </td>
    <td align="center">
        <p style="margin: 0;">{tests}</p>
    </td>
    <td align="center">
        <p style="margin: 0;">{passed}</p>
    </td>
    <td align="center">
        <p style="margin: 0;">{failed}</p>
    </td>
    <td align="center">
        <p style="margin: 0;">{broken}</p>
    </td>
    <td align="center">
        <p style="margin: 0;">{skipped}</p>
    </td>
    <td align="center">
        <p style="margin: 0;">{unknown}</p>
    </td>
    <td align="center">
        <p style="margin: 0;">{rate}</p>
    </td>
</tr>
"""


def allure_results(results_dir):
    files = [f for f in os.listdir(results_dir) if f.endswith("result.json")]
    results_list = []
    for f in files:
        f = os.path.join(results_dir, f)
        try:
            results_list.append(json.load(open(f, "rb")))
        except JSONDecodeError:
            pass
    return results_list


@dataclass
class Results:
    passed: int
    failed: int
    broken: int
    skipped: int
    unknown: int

    @property
    def tests(self):
        return (
            self.passed + self.failed + self.broken + self.skipped + self.unknown
        )  # noqa

    @property
    def rate(self):
        return "{:.2f}%".format(self.passed / self.tests * 100)


def get_group_results(results_dir, suit):
    """获取allure执行结果中以史诗划分的执行信息"""
    groups: dict = {}
    # 初始化结果行
    for r in allure_results(results_dir):
        for label in r.get("labels"):
            name = label.get("name")
            value = label.get("value")
            if name == suit and value not in groups.keys():
                groups.setdefault(label.get("value"), Results(0, 0, 0, 0, 0))  # noqa
    # 获取每行执行数据
    for group_name, group_value in groups.items():
        for r in allure_results(results_dir):
            for label in r.get("labels"):
                name = label.get("name")
                value = label.get("value")
                if name == suit and value == group_name:
                    if r.get("status") == "passed":
                        group_value.passed += 1
                    elif r.get("status") == "failed":
                        group_value.failed += 1
                    elif r.get("status") == "broken":
                        group_value.broken += 1
                    elif r.get("status") == "skipped":
                        group_value.skipped += 1
                    elif r.get("status") == "unknown":
                        group_value.unknown += 1
    # 获取每行
    table = ""
    summery = Results(0, 0, 0, 0, 0)
    for name, row in groups.items():
        row_content = row_template.format(
            name=name,
            tests=row.tests,
            passed=row.passed,
            failed=row.failed,
            broken=row.broken,
            skipped=row.skipped,
            unknown=row.unknown,
            rate=row.rate,
        )

        summery.passed += row.passed
        summery.failed += row.failed
        summery.broken += row.broken
        summery.skipped += row.skipped
        summery.unknown += row.unknown

        table += row_content
    # 汇总行
    table += row_template.format(
        name="汇总",
        tests=summery.tests,
        passed=summery.passed,
        failed=summery.failed,
        broken=summery.broken,
        skipped=summery.skipped,
        unknown=summery.unknown,
        rate=summery.rate,
    )
    return table


class AllureGraph:
    def __init__(self, url):
        self.driver = binding.launch(headless=True, infobars=True, mirrors=True)  # noqa
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(10)

    def base64pics(self, locators: List[str] = None) -> list:
        pics2base64 = []
        if not locators:
            locators = [
                "[data-id='status-chart']",
                "[data-id='severity']",
                "[data-id='duration']",
                "[data-id='history-trend']",
            ]
        scroll = "arguments[0].scrollIntoViewIfNeeded(true)"
        for index, locate in enumerate(locators):
            from selenium.webdriver.support import expected_conditions as ec

            element = WebDriverWait(self.driver, 10, 0.5).until(
                ec.visibility_of_element_located(("css selector", locate))
            )
            self.driver.execute_script(scroll, element)
            element.screenshot(f"{index}.png")
            with open(f"{index}.png", "rb") as pic64:
                pic = base64.b64encode(pic64.read()).decode("utf-8")
                pics2base64.append(pic)
            os.remove(Path(".").resolve().joinpath(f"{index}.png"))
        return pics2base64


def report_content(
    allure_url,
    results_dir,
    suit="epic",
):
    content = report_template.replace(
        "{result_row}", get_group_results(results_dir, suit)
    )  # noqa

    content = content.replace("\r", "")
    content = content.replace("\n", "")
    content = content.replace("\t", "")

    allure = AllureGraph(allure_url)
    content = content.replace("{STATUS}", allure.base64pics()[0])
    content = content.replace("{SEVERITY}", allure.base64pics()[1])
    content = content.replace("{DURATION}", allure.base64pics()[2])
    content = content.replace("{TREND}", allure.base64pics()[3])

    return content


def email(
    user,
    password,
    host,
    port,
    smtp_ssl,
    to,
    subject,
    content,
):
    yag = yagmail.SMTP(
        user, password, host=host, port=int(port), smtp_ssl=bool(smtp_ssl)
    )  # noqa
    yag.send(to, subject, [content])
    yag.close()


def allure_email_handler(results_dir, allure_config: dict, email_config: dict):
    graph_url = (
        f"{allure_config.get('protocol')}://"
        + f"{allure_config.get('host')}:"
        + f"{allure_config.get('port')}/job/"
        + f"{allure_config.get('task')}/allure/#graph"
    )
    content = report_content(
        allure_url=graph_url,
        results_dir=results_dir,
        suit="epic",
    )
    return email(
        email_config.get("sender"),
        email_config.get("pwd"),
        email_config.get("host"),
        email_config.get("port"),
        email_config.get("smtp_ssl"),
        email_config.get("address"),
        email_config.get("subject"),
        content=content,
    )
