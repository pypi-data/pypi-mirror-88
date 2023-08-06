Just screenshot allure report and send.
-

usage:
`pip install specious`

```python
from pathlib import Path

from specious.reports import allure_email_handler

result = Path(".").resolve().parent
allure_email_handler(results_dir=result.joinpath("allure-results"),
                     allure_config=dict(
                         protocol="http",
                         host="...",
                         port="...",
                         task="htms-automated-test"
                     ),
                     email_config=dict(
                        sender="...",
                        pwd="...",
                        host="smtphm.qiye.163.com",
                        port=465,
                        smtp_ssl=True,
                        address="...",
                        subject="HTMS AUTOMATED REPORT",
                     ))
```