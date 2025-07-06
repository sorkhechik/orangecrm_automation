# Automated Testing Suite for OrangeHRM

## Prerequisites
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`

## Project Structure
- `config/config.py`: Configuration file with base URL.
- `data/test_data.yaml`: Test data (usernames, passwords) in YAML format.
- `pages/`: Page Object Model classes for login and dashboard pages.
- `tests/conftest.py`: P conserva Pytest fixtures for test setup, including automatic login.
- `tests/test_login.py`: Test cases for login functionality (successful and invalid login).
- `tests/test_dashboard.py`: Test cases for dashboard functionality.
- `requirements.txt`: Project dependencies.
- `README.md`: Project documentation.

## Running Tests
1. Ensure dependencies are installed: `pip install -r requirements.txt`
2. Run tests using: `pytest tests/ -v --setup-show`

## Test Modules
1. **TestLogin**: Two independent tests for login functionality:
   - `test_successful_login`: Tests successful login with valid credentials.
   - `test_invalid_login`: Tests failed login with invalid credentials.
2. **TestDashboard**: Tests dashboard elements and navigation to Admin page, starting from a logged-in state.

## Notes
- Uses SeleniumBase for browser automation.
- Uses Pytest for test execution and fixtures.
- Login is managed automatically via a Pytest fixture in `conftest.py` for tests requiring a logged-in state.
- Follows Page Object Model (POM) design pattern for maintainability.
- Configuration data (URL) is stored in `config/config.py`.
- Test data (usernames, passwords) is stored in `data/test_data.yaml`.
- Tests for pages other than login (e.g., dashboard) start from a logged-in state using the `login` fixture.