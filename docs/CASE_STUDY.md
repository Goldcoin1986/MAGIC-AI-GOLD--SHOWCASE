# Case study — từ nhu cầu vận hành đến sản phẩm có thể kiểm thử

## Bối cảnh

Khi nhiều tiến trình MT5 chạy trên một VPS, người vận hành khó quan sát nhanh tài
khoản nào đang hoạt động, nguồn nào đã ngừng cập nhật và thay đổi nào thực sự đến
từ Agent. Việc điều khiển qua Remote Desktop cũng chậm và bất tiện trên màn hình nhỏ.

## Mục tiêu sản phẩm

1. Một màn hình cho tối đa 10 nguồn dữ liệu.
2. Trạng thái phải phản ánh dữ liệu thật, không dùng animation để giả lập online.
3. Dữ liệu lỗi hoặc cũ không được hiển thị như dữ liệu mới.
4. Laptop có thể xem Runtime trên VPS mà không mở trực tiếp localhost ra Internet.
5. Thao tác có ảnh hưởng phải xác nhận và có phản hồi từ Agent.

## Giải pháp

- Agent xuất snapshot riêng cho từng nguồn bằng thao tác ghi atomic.
- Runtime phát hiện snapshot, chuẩn hóa schema và cung cấp API cục bộ.
- Dashboard dùng change token/long-poll để nhận thay đổi nhanh nhưng không gây tải lớn.
- Remote Gateway chỉ chuyển tiếp API cần thiết qua phiên đã xác thực.
- Connection epoch loại response đến trễ khi người dùng vừa đổi Host/Remote.
- Bộ test mô phỏng dữ liệu thiếu, JSON lỗi, nguồn stale, nhiều tài khoản và mất mạng.

## Các vòng cải tiến tiêu biểu

- Thay ATR/Tick khó hiểu bằng Start/End và lot khởi đầu.
- Spread hiển thị theo dạng hiện tại/giới hạn để người dùng hiểu trong vài giây.
- Xử lý số tiền lớn và hậu tố đơn vị không tràn khung.
- Giảm độ trễ EA → Runtime → Dashboard bằng change token và long-poll.
- Sửa đổi cổng Remote theo cơ chế rebind; tự quay lại cổng cũ nếu bind thất bại.
- Thêm lịch sử địa chỉ/mã ghép nối nhưng chỉ lưu sau khi xác thực thành công.

## Kết quả học được

- Một giao diện đẹp không đủ nếu trạng thái không có nguồn dữ liệu xác định.
- Thông báo “đã nhận lệnh” phải dựa trên ACK, không dựa vào việc API đã nhận request.
- Các lỗi vận hành thực tế thường nằm ở ranh giới giữa Agent, file, API và giao diện.
- Kiểm thử hồi quy quan trọng hơn việc sửa riêng một ảnh chụp giao diện.

## Phạm vi trách nhiệm

Product design, requirement definition, UX direction, data mapping, acceptance
criteria, scenario testing và release validation. Việc triển khai được thực hiện
theo quy trình AI-assisted development có kiểm tra và sửa lỗi lặp lại.
