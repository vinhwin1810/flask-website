# Sử dụng một base image Python có phiên bản tương thích
FROM python:3.9

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả các tệp từ thư mục hiện tại vào thư mục /app trong container
COPY . /app

# Cài đặt các phụ thuộc của ứng dụng
RUN pip install --no-cache-dir -r requirements.txt

# Khai báo cổng mà ứng dụng sẽ lắng nghe
EXPOSE 5000

# Khởi chạy ứng dụng Flask
CMD ["python", "app.py"]
