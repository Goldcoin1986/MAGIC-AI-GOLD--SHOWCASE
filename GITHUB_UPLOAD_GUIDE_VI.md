# Hướng dẫn đưa repository lên GitHub

## Cách đơn giản bằng trình duyệt

1. Đăng nhập GitHub và chọn **New repository**.
2. Đặt tên: `magic-ai-gold-showcase`.
3. Chọn **Public**.
4. Không tích chọn tạo README hoặc `.gitignore`, vì gói này đã có sẵn.
5. Mở repository vừa tạo → **Add file** → **Upload files**.
6. Giải nén ZIP portfolio trên máy và kéo toàn bộ nội dung bên trong thư mục
   `magic-ai-gold-showcase` lên GitHub.
7. Kiểm tra có `README.md`, `assets`, `docs`, `src`, `tests` rồi mới bấm
   **Commit changes**.

Mô tả repository gợi ý:

> Realtime multi-account monitoring and remote operations dashboard — product, UX, QA and sanitized engineering showcase.

Topics gợi ý:

`product-management`, `dashboard`, `realtime`, `python`, `qa`, `windows`, `portfolio`

## Kiểm tra trước khi bấm Commit

Repository public **không được xuất hiện** các tên sau:

- `.mq5`, `.mqh`, `.ex5`, `.exe`
- `private_key.hex`, `ea_hmac_secret.hex`
- `license.lic`, `.magiclicense`, `remote_connection.json`
- ZIP có chữ `OWNER_ONLY`
- IP VPS, mã ghép nối, số tài khoản hoặc dữ liệu khách hàng thật

Nếu thấy một trong các file trên, dừng upload và xóa khỏi danh sách trước khi commit.
