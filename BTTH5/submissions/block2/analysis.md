# Phân tích kết quả `csv-quality`

## Thay đổi và bằng chứng

- `skills/csv-quality/SKILL.md` hướng dẫn không tự chọn ngưỡng khi người dùng chưa cung cấp; lỗi thực thi phải được báo rõ và không được ghi báo cáo thành công khi script không phân tích được.
- `skills/csv-quality/references/report-template.md` yêu cầu trình bày ngưỡng, giờ theo owner, người quá tải, các dòng bị loại, và chi tiết lỗi dữ liệu.
- Script trong `skills/csv-quality/scripts/check_csv.py` đã có logic ghi nhận `task_id` lần đầu trước khi quyết định cộng giờ; chỉ dòng không có lỗi mới được cộng vào `hours_by_owner`. Script workspace, fixture, và submission được đối chiếu để bảo đảm cùng nội dung.
- Thêm `data/workload-edge.csv` và fixture đồng bộ. Kiểm thử `test_edge_case_first_occurrence_invalid_hours` đọc CSV fixture này thay vì dựng dữ liệu inline; kiểm thử cũng có trong `tests/test_check_csv.py` của submission.
- `results/workload-8h.json`, `results/workload-9h.json`, và `results/workload-edge-max0.json` là stdout JSON được lưu lại từ các lần gọi trực tiếp script, đều exit code 0.

## Kết quả

### Ngưỡng 8 giờ

Nguồn: `data/workload.csv`; exit code 0. Tổng giờ hợp lệ là Lan 9.0, Minh 3.0. Lan vượt ngưỡng. Các dòng 5, 6, 7 lần lượt bị loại do `invalid_hours`, `duplicate_id`, và `missing_owner`.

Agent đã tạo `reports/workload.md`. Trace [20261007-122757_3ecf6f40_turn01_913fcb26.jsonl](./traces/20261007-122757_3ecf6f40_turn01_913fcb26.jsonl): dòng 1 là yêu cầu; dòng 12 gọi script với `--max-hours 8`; dòng 13 ghi nhận exit code 0; dòng 17 ghi báo cáo; dòng 20 kết thúc lượt.

### Ngưỡng 9 giờ

Nguồn: `data/workload.csv`; exit code 0. Tổng giờ vẫn là Lan 9.0, Minh 3.0. Không ai vượt ngưỡng vì điều kiện là tổng giờ **lớn hơn** ngưỡng; Lan đạt đúng 9.0. Các dòng bị loại giống trường hợp ngưỡng 8.

Agent đã tạo `reports/workload-9h.md`. Trace [20261007-123001_3ecf6f40_turn02_91c6989d.jsonl](./traces/20261007-123001_3ecf6f40_turn02_91c6989d.jsonl): dòng 1 là yêu cầu; dòng 4 gọi script với `--max-hours 9`; dòng 5 ghi nhận exit code 0; dòng 9 ghi báo cáo; dòng 12 kết thúc lượt.

### Thiếu ngưỡng

Yêu cầu trong trace không cung cấp ngưỡng. Agent đọc skill nhưng không gọi script và không ghi báo cáo; không tự áp dụng một ngưỡng mặc định. Trace [20261007-123113_3ecf6f40_turn03_37df04ee.jsonl]: dòng 1 là yêu cầu; dòng 4–5 ghi lần đọc skill; dòng 8 kết thúc lượt. Không có sự kiện `bash` hoặc `write_file` trong lượt này.

### File không tồn tại

Yêu cầu kiểm tra `data/khong-ton-tai.csv` với ngưỡng 8. Script trả exit code 1, stdout rỗng, stderr báo không đọc được file. Agent không tạo báo cáo thành công. Trace [20261007-123154_3ecf6f40_turn04_756c6a30.jsonl]: dòng 1 là yêu cầu; dòng 4 gọi script; dòng 5 ghi nhận exit code 1 và lỗi file không tồn tại; dòng 8 kết thúc lượt.

### Trường hợp đặc biệt: ID đầu tiên có giờ không hợp lệ

Đầu vào `data/workload-edge.csv`:

```csv
task_id,owner,hours
E01,Lan,abc
E01,Lan,5
E02,Minh,0
```

Chạy với ngưỡng 0; exit code 0. Dòng 2 bị loại do `invalid_hours` nhưng ID E01 vẫn được ghi nhận lần đầu. Dòng 3 bị loại do `duplicate_id`; 5 giờ của Lan không được cộng. Tổng giờ là `{"Minh": 0.0}`, và `overloaded_owners` rỗng vì 0 không lớn hơn ngưỡng 0. Kết quả đầy đủ ở `results/workload-edge-max0.json`.

## Kiểm tra bí mật

Không đưa `.env`, API key, hay credential vào submission. Các trace được giữ theo bản ghi sẵn có; nội dung bằng chứng được trích trong tài liệu này chỉ gồm yêu cầu, lệnh, trạng thái, kết quả script và đường dẫn báo cáo.
