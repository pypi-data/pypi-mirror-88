from selenium import webdriver
from selenium.webdriver import Proxy
import time
from base64 import b64decode

FIREFOX_PREFERENCES = {
    "dom.popup_maximum": 0,
    "browser.download.folderList": 2,
    "browser.download.panel.shown": False,
    "privacy.popups.showBrowserMessage": False,
    "browser.download.manager.showWhenStarting": False,
    "browser.helperApps.neverAsk.saveToDisk": ".mp3 audio/mpeg",
}


def _browser_class_and_options(browser_type):
    Options = None
    if browser_type == 'firefox':
        from selenium.webdriver.firefox.webdriver import WebDriver
        from selenium.webdriver.firefox.options import Options
    elif browser_type == 'chrome':
        from selenium.webdriver.chrome.webdriver import WebDriver
        from selenium.webdriver.chrome.options import Options
    elif browser_type == 'ie':
        from selenium.webdriver.ie.webdriver import WebDriver
        from selenium.webdriver.ie.options import Options
    elif browser_type == 'webkitgtk':
        from selenium.webdriver.webkitgtk.webdriver import WebDriver
        from selenium.webdriver.webkitgtk.options import Options
    elif browser_type == 'edge':
        from selenium.webdriver.edge.webdriver import WebDriver
    elif browser_type == 'opera':
        from selenium.webdriver.opera.webdriver import WebDriver
    elif browser_type == 'safari':
        from selenium.webdriver.safari.webdriver import WebDriver
    elif browser_type == 'blackberry':
        from selenium.webdriver.blackberry.webdriver import WebDriver
    elif browser_type == 'phantomjs':
        from selenium.webdriver.phantomjs.webdriver import WebDriver
    elif browser_type == 'android':
        from selenium.webdriver.android.webdriver import WebDriver
    elif browser_type == 'remote':
        from selenium.webdriver.remote.webdriver import WebDriver
    else:
        raise ValueError("Unsupported browser type '{}'.".format(browser_type))

    return WebDriver, Options


def open_browser(
    url, browser_type, headless=False, proxy_conf={}, **browser_kargs
):
    ''' Quick shortcut to open a <url> using a particular
        <browser_type>.

        Return a Selector (sQ) object bound to the browser.
        '''
    # make 'driver' and alias of the standard 'executable_path'
    tmp = browser_kargs.pop('driver', None)
    if tmp is not None and 'executable_path' not in browser_kargs:
        browser_kargs['executable_path'] = tmp

    from .selectq import Selector
    WebDriver, Options = _browser_class_and_options(browser_type)
    if Options is None:
        warnings.warn(
            "The browser '{}' does not support custom options.".
            format(browser_type)
        )

    if 'options' not in browser_kargs and Options is not None:
        proxy = Proxy(proxy_conf)

        options = Options()
        options.headless = headless
        if proxy_conf:
            options.proxy = proxy

        browser_kargs['options'] = options

    driver = WebDriver(**browser_kargs)

    sQ = Selector(driver)
    sQ.browser.get(url)

    return sQ


def wait_for(cnd, *, step=1, timeout=30, take_screenshot=False):
    ''' Wait for the given condition to be true checking every <step> seconds
        and waiting up to <timeout> seconds.

        Raises TimeoutError if the condition is not met.

        If <take_screenshot> is True, a base64 encoded PNG image of the
        screen is taken on timeout and saved in the exception under
        the 'screenshot' attribute.

        If <take_screenshot> is a string, the screenshot is saved to disk
        where <take_screenshot> is the path to the file. The image is still
        saved in the exception.

        '''
    from .selectq import Selection
    if isinstance(cnd, Selection):
        raise TypeError(
            "Make the check explicit: 'selection != 0' for example"
        )

    from .predicates import Cond
    if not isinstance(cnd, Cond):
        raise TypeError(
            "Expected a condition, instead received '{}'.".format(type(cnd))
        )

    hold = bool(cnd)
    sleep = time.sleep
    left = timeout
    while not hold and left > 0:
        sleep(step)
        left -= step
        hold = bool(cnd)

    if not hold:
        err = TimeoutError(
            "{} is still false after {} secs.".format(cnd, timeout)
        )
        if take_screenshot:
            err.screenshot = cnd.sel.browser.driver.get_screenshot_as_base64()
            if isinstance(take_screenshot, str):
                with open(take_screenshot, 'wb') as f:
                    f.write(b64decode(err.screenshot.encode('ascii')))

        raise err

    return
