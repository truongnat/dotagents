---
name: self-learning-loop
description: "Tự động phân tích, đúc kết bài học kỹ thuật sau mỗi turn/task gặp lỗi lặp lại, sửa sai hoặc giải pháp mới; sinh và tinh chỉnh skill để tích lũy tri thức cho các phiên tiếp theo."
---
# Vòng lặp Tự học và Đúc kết Kỹ năng (Self-Learning Loop)

## Khi nào dùng
- Khi gặp lỗi hoặc thử nghiệm lệnh thất bại $\ge 2$ lần trước khi tìm được cách khắc phục thành công.
- Khi người dùng phản hồi chỉnh sửa sai sót hoặc đưa ra hướng dẫn/quy ước nghiệp vụ mới.
- Sau khi hoàn thành một bài toán kỹ thuật phức tạp, giải quyết được root cause khó hoặc quy trình chưa từng có trong kho skill.
- Khi người dùng yêu cầu rõ ràng: "hãy đúc kết lại thành skill", "/learn", hoặc "lưu quy trình này để lần sau dùng".

## Không dùng khi
- Các tương tác thông thường, tra cứu tài liệu đơn giản hoặc câu hỏi giải thích không tạo ra tri thức tái sử dụng.
- Vấn đề chỉ mang tính nhất thời, cục bộ một lần (one-off scratch) không có khả năng lặp lại.
- Chưa xác minh được giải pháp trong thực tế (không đúc kết các giả thuyết chưa được kiểm chứng).

## Quy trình
1. **Thu thập tín hiệu (Signal Capture):**
   - Xác định: (a) Triệu chứng/Lỗi ban đầu, (b) Nguyên nhân cốt lõi (Root Cause), (c) Hành động/cú pháp chính xác mang lại kết quả thành công, (d) Điều kiện áp dụng.
2. **Kiểm tra trùng lặp & Khởi tạo draft:**
   - Chạy script kiểm tra và tạo draft vào thư mục staging:
     ```bash
     python3 .agents/scripts/skill-distiller.py \
       --name "<ten-skill-kebab-case>" \
       --description "<Mô tả ngắn gọn mục đích và trigger>" \
       --trigger "<Điều kiện kích hoạt 1>" \
       --anti-trigger "<Trường hợp không dùng>" \
       --step "<Bước 1>" \
       --step "<Bước 2>" \
       --rule "<Quy tắc an toàn>" \
       --gotcha "<Bẫy thường gặp>" \
       --code "<Lệnh hoặc đoạn code mẫu>"
     ```
   - Nếu script phát hiện trùng lặp cao với skill sẵn có: mở skill cũ và cập nhật thêm gotcha/edge case thay vì tạo skill trùng lặp.
3. **Kiểm định chất lượng draft (Verification):**
   - Chạy kiểm tra dry-run với script promote:
     ```bash
     python3 .agents/scripts/promote-skill.py <ten-skill-kebab-case> --dry-run
     ```
4. **Phê duyệt & Chuyển vào kho chính thức (Promotion):**
   - Trình tóm tắt skill mới cho người dùng (hoặc chuyển vào kho chính thức nếu đã được ủy quyền):
     ```bash
     python3 .agents/scripts/promote-skill.py <ten-skill-kebab-case>
     ```
   - Chạy kiểm tra tính toàn vẹn của danh mục:
     ```bash
     .agents/scripts/validate-skills.sh .agents/skills
     ```

## Quy tắc
- **Chất lượng hơn số lượng:** Không tạo skill rác cho các tác vụ cơ bản đã có trong tài liệu tiêu chuẩn.
- **Bắt buộc kiểm chứng:** Chỉ đúc kết giải pháp khi đã có bằng chứng chạy thật (test pass, exit code 0).
- **Tuân thủ quy chuẩn naming:** Tên skill phải là kebab-case, trùng tên thư mục chứa file `SKILL.md`.
- **Cơ chế Staging an toàn:** Mọi skill mới sinh ra phải đi qua `.agents/skills/.staging/` trước khi promote.

## Điều kiện hoàn tất
- Draft skill được tạo thành công, vượt qua kiểm định `validate-draft-skill` và `validate-skills.sh`.
- Báo cáo rõ ràng đường dẫn file skill đã tạo hoặc cập nhật.

## Template/tham chiếu liên quan
- `.agents/template/skill/SKILL.md`
- `.agents/scripts/skill-distiller.py`
- `.agents/scripts/promote-skill.py`
- `.agents/scripts/validate-skills.sh`
