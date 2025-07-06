from pages.dashboard_page import DashboardPage
from tests.base_test import BaseTest
import pytest

class TestDashboard(BaseTest):
    def test_dashboard_loaded_module(self, login_module=pytest.param("Admin")):
        dashboard = DashboardPage(self)
        dashboard.verify_dashboard_loaded()

    def test_dashboard_loaded_function(self, login_function=pytest.param("Admin")):
        dashboard = DashboardPage(self)
        dashboard.verify_dashboard_loaded()