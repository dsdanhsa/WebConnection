import os

# Đường dẫn đến thư mục locale của dự án Django
locale_dir = r'search-ms:displayname=Search%20Results%20in%20site-packages&crumb=location:E%3A%5CSQL%5CWebConnection%5Cvenv%5CLib%5Csite-packages\\locale'

# Lặp qua tất cả các thư mục con trong thư mục locale
for root, dirs, files in os.walk(locale_dir):
    for file in files:
        # Kiểm tra nếu tệp có phần mở rộng là .mo
        if file.endswith('.mo'):
            # Xóa tệp
            os.remove(os.path.join(root, file))

print("Đã xóa tất cả các tệp .mo thành công!")
