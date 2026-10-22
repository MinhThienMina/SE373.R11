---
name: refund-policy
description: Tra cứu và áp dụng chính sách hoàn tiền cho khách hàng dựa trên ngày mua hàng, ngày yêu cầu hoàn tiền và trạng thái kích hoạt sản phẩm. Dùng khi người dùng hỏi về quyền lợi hoàn tiền, tính hợp lệ của yêu cầu hoàn tiền, thời hạn hoàn tiền hoặc mức phí hoàn tiền.
---

# Refund policy

Hướng dẫn tra cứu và áp dụng chính sách hoàn tiền đúng phiên bản. Mọi số liệu và điều kiện phải lấy từ tài liệu chính sách đã đọc, không dùng trí nhớ.

## 1. Kiểm tra thông tin đầu vào

Trước khi kết luận, BẮT BUỘC phải có đủ 3 thông tin:

1. **Ngày mua hàng**.
2. **Ngày yêu cầu hoàn tiền**: dùng ngày người dùng nêu trong câu hỏi, không dùng ngày hiện tại của máy.
3. **Trạng thái kích hoạt sản phẩm** (đã kích hoạt hay chưa kích hoạt).

> **QUY TẮC BẮT BUỘC**: Nếu thiếu bất kỳ thông tin nào trong 3 thông tin trên (đặc biệt là trạng thái kích hoạt), PHẢI HỎI LẠI người dùng và chưa kết luận. KHÔNG tự suy diễn hay giả định, ví dụ không tự cho là "chưa kích hoạt".

## 2. Tìm kiếm và đọc tài liệu chính sách

1. Dùng `list_files` với đường dẫn `data/policies` để lấy danh sách tài liệu thực tế. Tên file có thể thay đổi, không được giả định tên file cố định.
2. Dùng `read_file` đọc từng tài liệu chính sách tìm được.
3. Với mỗi tài liệu, xác định:
   - Phạm vi hiệu lực theo ngày mua.
   - Thời hạn cho phép yêu cầu hoàn tiền.
   - Mức phí hoàn tiền (nếu có).
   - Điều kiện về trạng thái kích hoạt.

## 3. Chọn và áp dụng chính sách

1. **Chọn chính sách**: đối chiếu **ngày mua hàng** với phạm vi hiệu lực ghi trong từng tài liệu đã đọc, chọn tài liệu có phạm vi chứa ngày mua. Không chọn theo ngày yêu cầu hoàn. Chú ý ngày biên: đọc kỹ tài liệu xem ngày đó thuộc chính sách nào. Nếu không có tài liệu nào khớp, hoặc có hơn một tài liệu khớp, nói rõ và chưa kết luận.
2. **Tính số ngày đã qua**: chênh lệch ngày lịch giữa **ngày yêu cầu hoàn** và **ngày mua**.
3. **Đối chiếu với chính sách đã chọn**, chỉ dùng số liệu và điều kiện trong tài liệu đó:
   - Số ngày so với thời hạn cho phép (bằng đúng giới hạn vẫn đủ điều kiện về thời gian).
   - Điều kiện về trạng thái kích hoạt.
   - Mức phí hoàn tiền (nếu có).
4. **Kết luận**: đủ điều kiện khi thoả mọi điều kiện của chính sách đã chọn, ngược lại là không đủ điều kiện và nêu rõ điều kiện nào không thoả.

## 4. Cấu trúc câu trả lời

Trước khi viết câu trả lời cuối, đọc `skills/refund-policy/references/answer-template.md` bằng `read_file` và trình bày đúng theo mẫu đó, gồm:

1. Chính sách áp dụng (tên và phạm vi hiệu lực).
2. Số ngày đã qua.
3. Kết luận đủ hay không đủ điều kiện.
4. Phí hoàn tiền theo chính sách đã chọn nếu đủ điều kiện.
5. Đường dẫn tài liệu làm căn cứ, đúng như `list_files` trả về.

Không dùng Bash hay script trong stage này.
