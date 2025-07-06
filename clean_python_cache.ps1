# پاکسازی پوشه‌ها و فایل‌های کش پایتون در کل پروژه

Write-Host "در حال پاکسازی فایل‌ها و پوشه‌های کش پایتون..."

# حذف __pycache__ و زیرپوشه‌های آن
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# حذف .pytest_cache
Get-ChildItem -Path . -Recurse -Directory -Filter ".pytest_cache" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# حذف .mypy_cache
Get-ChildItem -Path . -Recurse -Directory -Filter ".mypy_cache" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# حذف فایل‌های .pyc و .pyo
Get-ChildItem -Path . -Recurse -Include *.pyc,*.pyo -File | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "پاکسازی با موفقیت انجام شد ✅"
