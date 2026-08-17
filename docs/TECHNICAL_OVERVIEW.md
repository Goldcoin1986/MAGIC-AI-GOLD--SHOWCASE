# Technical overview

## Luồng dữ liệu

1. Desktop Agent tạo snapshot cho từng nguồn.
2. Snapshot được thay thế atomic để reader không thấy file đang ghi dở.
3. Runtime kiểm tra schema, identity và thời điểm nguồn cập nhật.
4. API cung cấp detail, overview, health và trạng thái điều khiển.
5. Dashboard chỉ render dữ liệu đã chuẩn hóa.

## Freshness

Nguồn sống được xác định bằng thời điểm file/snapshot thật sự thay đổi, không chỉ
dựa vào đồng hồ bên trong payload. Ba trạng thái chính:

| Trạng thái | Ý nghĩa |
|---|---|
| ONLINE | Snapshot vẫn cập nhật trong ngưỡng heartbeat |
| STALE | Dữ liệu đã chậm; cần cảnh báo nhưng vẫn có thể quan sát |
| OFFLINE | Nguồn ngừng cập nhật quá ngưỡng cho phép |

## Host/Remote

- Dashboard luôn dùng một origin cục bộ ổn định.
- Router đổi backend giữa Runtime local và Remote tunnel.
- Mỗi lần đổi backend làm tăng epoch.
- Request/response thuộc epoch cũ bị loại bỏ.
- Token và lịch sử mã ghép nối không nằm trong bản portfolio.

## Điều khiển an toàn

- Không cung cấp API public để tự động phát tín hiệu giao dịch.
- Thao tác nhạy cảm yêu cầu xác nhận rõ ràng.
- Mỗi command có ID và cần ACK từ Agent.
- Khi dừng entry, hệ thống vẫn có thể quản lý trạng thái đang tồn tại.

## Testing

Các nhóm kiểm thử của sản phẩm thật bao gồm contract/schema, API, multi-source,
freshness, malformed JSON, Host/Remote switching, license, Windows packaging,
JavaScript syntax và regression UI. Code trong repository public có bộ test nhỏ
để minh họa cách khóa hợp đồng dữ liệu đầu vào.
