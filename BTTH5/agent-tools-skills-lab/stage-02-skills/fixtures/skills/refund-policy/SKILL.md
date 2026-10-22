---
name: refund-policy
description: Tra cuu chinh sach hoan tien dung phien ban theo ngay mua, ngay yeu cau hoan va trang thai kich hoat. Dung khi nguoi dung hoi co du dieu kien hoan tien hay khong.
---

# Refund policy

Dung skill nay khi cau hoi lien quan den hoan tien, doi tra, ngay mua, ngay yeu cau hoan, phi hoan tien hoac san pham da/chua kich hoat.

## Quy trinh

1. Neu thieu mot trong ba thong tin: ngay mua, ngay yeu cau hoan, trang thai kich hoat, hay hoi lai truoc khi ket luan.
2. Dung `list_files` voi `data/policies` de tim tai lieu chinh sach hien co. Khong gia dinh ten file.
3. Doc cac file chinh sach bang `read_file`. Chon chinh sach theo ngay mua, khong theo ngay yeu cau hoan.
4. Tinh so ngay da qua bang chenh lech ngay lich giua ngay yeu cau hoan va ngay mua. Bang dung gioi han van du dieu kien ve thoi gian.
5. Neu san pham da kich hoat, ket luan khong du dieu kien theo chinh sach.
6. Doc `skills/refund-policy/references/answer-template.md` truoc khi tra loi.

Khong dung ngay hien tai cua may. Khong dung Bash hay script trong stage nay.
