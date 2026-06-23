# 使用官方的 Python 輕量版環境
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 將套件清單複製進去並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 將你寫的所有程式碼複製進 Docker
COPY . .

# 預設啟動指令 (等一下會在 docker-compose 覆寫它)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]