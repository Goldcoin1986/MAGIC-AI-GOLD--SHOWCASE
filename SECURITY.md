# Security policy

Repository này chỉ chứa dữ liệu giả lập và code minh họa đã làm sạch.

Không gửi lên issue, pull request hoặc commit:

- Khóa ký license, HMAC secret, activation code hoặc license thật.
- Token Remote, mã ghép nối, IP VPS hoặc cấu hình khách hàng.
- File MQ5/MQH/EX5, EXE thương mại hoặc chiến lược giao dịch.
- Snapshot, log, số tài khoản hoặc thông tin nhận dạng của khách hàng.

Nếu một secret từng bị commit, xóa file ở commit mới là chưa đủ. Cần thu hồi hoặc
thay khóa, sau đó làm sạch toàn bộ lịch sử Git trước khi tiếp tục sử dụng repository.

Vui lòng báo cáo vấn đề bảo mật trực tiếp cho chủ sở hữu thay vì tạo public issue.
