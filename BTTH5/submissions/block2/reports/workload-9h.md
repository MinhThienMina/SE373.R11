# Báo cáo kiểm tra chất lượng và tải công việc: `data/workload.csv`

Công cụ: `skills/csv-quality/scripts/check_csv.py` | exit code: 0

## 1. Kiểm tra tải công việc (Ngưỡng: 9.0 giờ)

### Tổng giờ theo người

| Người phụ trách | Tổng giờ | Trạng thái quá tải |
| --------------- | --------- | ------------------ |
| Lan | 9.0 | Trong định mức |
| Minh | 3.0 | Trong định mức |

### Danh sách người quá tải

Không có ai vượt ngưỡng 9.0 giờ.

### Các dòng bị loại khỏi tính toán

| Dòng (Line) | Task ID | Lý do loại |
| ----------- | ------- | ---------- |
| 5 | T04 | invalid_hours |
| 6 | T02 | duplicate_id |
| 7 | T05 | missing_owner |

## 2. Tổng quan chất lượng dữ liệu

| Chỉ số | Giá trị |
| ----------------------------------- | -------------------------------------- |
| Số dòng dữ liệu (không tính header) | 6 |
| Dòng thiếu owner | 1 |
| Dòng hours không hợp lệ | 1 |
| Số task_id bị lặp (distinct) | 1 (T02) |

## 3. Chi tiết lỗi dữ liệu

| Line | Cột | Loại lỗi | Task ID | Mô tả |
| ------ | -------- | -------- | --------- | --------- |
| 5 | hours | invalid_hours | T04 | hours 'abc' khong phai so huu han khong am. |
| 6 | task_id | duplicate_id | T02 | task_id T02 da xuat hien o line 3. |
| 7 | owner | missing_owner | T05 | owner trong. |

## 4. Đánh giá và khuyến nghị

- **Đánh giá**: Dữ liệu có một số lỗi chất lượng cần khắc phục. Với ngưỡng 9.0 giờ, không có cá nhân nào vượt ngưỡng (Lan đạt đúng 9.0 giờ, Minh đạt 3.0 giờ).
- **Khuyến nghị**: Cần chuẩn hóa lại file CSV (sửa định dạng giờ của task T04, xử lý trùng lặp task_id T02, bổ sung owner cho T05) để đảm bảo tính chính xác của dữ liệu phân bổ công việc.
