import os
from seleniumbase import BaseCase
import logging

class BaseTest(BaseCase):
    logger = None  # تعریف logger به صورت کلاس‌محور

    @classmethod
    def setup_class(cls):
        if cls.logger is None:
            cls.logger = logging.getLogger(__name__)  # استفاده از logger مستقل
        cls.logger.info(f"Setting up {cls.__name__}")

    @classmethod
    def teardown_class(cls):
        cls.logger.info(f"Tearing down {cls.__name__}")

    def setup_method(self, method):
        super().setUp()
        self.logger.info(f"Running {method.__name__}")
        self.set_window_size(1280, 720)

    def teardown_method(self, method):
        self.logger.info(f"Finished {method.__name__}")
        super().tearDown()

    def take_screenshot(self, test_name):
        os.makedirs("screenshots", exist_ok=True)  # ایجاد دایرکتوری
        self.logger.info(f"Saving screenshot for {test_name}")
        self.save_screenshot(f"screenshots/{test_name}.png")

    def save_page_source(self, test_name):
        os.makedirs("screenshots", exist_ok=True)  # ایجاد دایرکتوری
        self.logger.info(f"Saving page source for {test_name}")
        with open(f"screenshots/{test_name}_source.html", "w", encoding="utf-8") as f:
            f.write(self.get_page_source())