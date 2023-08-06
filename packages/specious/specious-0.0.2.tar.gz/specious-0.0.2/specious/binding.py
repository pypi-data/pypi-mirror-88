from enum import Enum, unique
from typing import Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import IEDriverManager

mirrors_url = "http://npm.taobao.org/mirrors/chromedriver"
mirrors_release = "http://npm.taobao.org/mirrors/chromedriver/LATEST_RELEASE"


@unique
class BrowserType(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    IE = "ie"


def launch(
    name: str = "chrome",
    executable_path: str = None,
    grid_url: str = None,
    headless: bool = False,
    sandbox: bool = False,
    window_size: str = "1366x768",
    incognito: bool = False,
    infobars: bool = False,
    dev_shm_usage: bool = False,
    mirrors: bool = False,
    **kwargs,
):
    def get_options(options: Union[ChromeOptions, FirefoxOptions, IeOptions]):
        if headless:
            options.add_argument("--headless")
        if not sandbox:
            options.add_argument("--no-sandbox")
        if window_size:
            options.add_argument(f"--window-size={window_size}")
        if not incognito:
            options.add_argument("--incognito")
        if not infobars:
            options.add_argument("--disable-infobars")
        if not dev_shm_usage:
            options.add_argument("--disable-dev-shm-usage")
        return options

    if name == BrowserType.CHROME.value:
        chrome_options = get_options(ChromeOptions())
        if not executable_path and not mirrors:
            executable_path = ChromeDriverManager().install()
        elif not executable_path and mirrors:
            executable_path = ChromeDriverManager(
                url=mirrors_url,
                latest_release_url=mirrors_release,
            ).install()
        if grid_url:
            return webdriver.Remote(
                command_executor=grid_url,
                desired_capabilities=DesiredCapabilities.CHROME.copy(),
                options=chrome_options,
                **kwargs,
            )
        return webdriver.Chrome(executable_path, options=chrome_options, **kwargs)
    elif name == BrowserType.FIREFOX.value:
        firefox_options = get_options(FirefoxOptions())
        if not executable_path:
            executable_path = GeckoDriverManager().install()
        if grid_url:
            return webdriver.Remote(
                command_executor=grid_url,
                desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
                options=firefox_options,
                **kwargs,
            )
        return webdriver.Firefox(executable_path, options=firefox_options, **kwargs)
    elif name == BrowserType.IE.value:
        ie_options = get_options(IeOptions())
        if not executable_path:
            executable_path = IEDriverManager().install()
        if grid_url:
            ca = DesiredCapabilities.INTERNETEXPLORER.copy()
            return webdriver.Remote(
                command_executor=grid_url,
                desired_capabilities=ca,
                options=ie_options,
                **kwargs,
            )
        return webdriver.Ie(executable_path, options=ie_options, **kwargs)
