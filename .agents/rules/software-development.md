# Quy trình phát triển phần mềm

Áp dụng quy trình tương xứng với rủi ro: thay đổi nhỏ cần kiểm tra gọn; thay đổi rủi ro cao hoặc ảnh hưởng nhiều thành phần cần yêu cầu, thiết kế, test, kế hoạch triển khai và bàn giao rõ ràng.

## Giai đoạn 1 — Hiểu vấn đề

- Tóm tắt vấn đề và kết quả mong muốn.
- Tìm memory, code và tài liệu hiện có trước khi đề xuất giải pháp.
- Xác định người dùng/actor, hành vi hiện tại, hành vi mong muốn, ràng buộc và tiêu chí chấp nhận.
- Đánh dấu điều chưa biết; không tự suy diễn quy tắc nghiệp vụ.

## Giai đoạn 2 — Lập kế hoạch

- Kiểm tra module, contract, luồng dữ liệu, test, migration và thành phần tiêu thụ bị ảnh hưởng.
- Chọn cách triển khai nhỏ nhất nhưng nhất quán.
- Chia công việc rủi ro cao thành các bước dễ review; liệt kê file/module dự kiến thay đổi.
- Xem xét tương thích, quyền truy cập, luồng lỗi, khả năng quan sát, rollback và tác động vận hành.

## Giai đoạn 3 — Thiết kế khi cần

- Ghi lại thay đổi API/schema/event và ranh giới trách nhiệm.
- Nêu các phương án quan trọng và lý do chọn phương án cuối cùng.
- Dùng ADR cho quyết định có ảnh hưởng kiến trúc lâu dài.
- Liên kết thiết kế với file nguồn và tiêu chí chấp nhận.

## Giai đoạn 4 — Triển khai

- Tuân theo pattern hiện có của project, trừ khi chính pattern đó là nguyên nhân đã xác nhận.
- Giữ phạm vi thay đổi rõ ràng; tránh refactor không liên quan.
- Bổ sung/cập nhật test cùng với thay đổi hành vi.
- Với thay đổi dữ liệu, xác định migration, tương thích, backfill và rollback khi phù hợp.

## Giai đoạn 5 — Kiểm chứng

- Chạy các kiểm tra tự động phù hợp nhất: unit, integration, e2e, lint, type check, build, kiểm tra migration hoặc kịch bản thủ công có thể tái hiện.
- Kiểm tra tiêu chí chấp nhận và các đường lỗi/edge case quan trọng, không chỉ happy path.
- Báo rõ lệnh/kết quả, kiểm tra bị bỏ qua, giả định và rủi ro còn lại.

## Giai đoạn 6 — Review và phát hành

- Review diff về tính đúng đắn, nguy cơ regression, bảo mật, logging, tương thích và secret vô tình bị thêm.
- Cập nhật tài liệu/config/migration/release notes khi cần.
- Với thay đổi triển khai rủi ro cao, nêu rollout, tín hiệu sức khỏe hệ thống và điều kiện rollback.

## Giai đoạn 7 — Đúc kết và bàn giao

- Tạo/cập nhật memory lâu dài trong `memory/entries/` khi đáp ứng memory policy.
- Cập nhật hoặc thay thế entry cũ để tránh phân mảnh kiến thức.
- Bàn giao ngắn gọn: hành vi đã đổi, khu vực/file liên quan, kết quả kiểm chứng, giới hạn và memory đã cập nhật.

## Chọn template tối thiểu

| Loại công việc | Template đề xuất |
|---|---|
| Bug nhỏ | Điều tra bug + test liên quan; memory nếu có bài học tái sử dụng |
| Feature | Đặc tả feature + kế hoạch triển khai + kế hoạch test |
| Refactor/ảnh hưởng nhiều thành phần | Kế hoạch + thiết kế kỹ thuật + kế hoạch test |
| Quyết định kiến trúc | ADR, thêm thiết kế kỹ thuật nếu cần |
| Release/migration rủi ro cao | Kế hoạch + kế hoạch test + checklist release |
| Incident production | Postmortem sau khi đã giảm thiểu/ổn định |
| Kết thúc phiên khi task chưa xong | Bàn giao công việc |

## Quy ước đầu ra: Chat ngắn gọn vs File Deliverable (Template)

Phân định nghiêm ngặt giữa hai kênh đầu ra để tránh làm loãng ngữ cảnh hội thoại:

1. **Kênh File Deliverable (bắt buộc khi dùng template):**
   - Mọi báo cáo hoặc tài liệu dựa trên template (`feature-spec.md`, `technical-design.md`, `implementation-plan.md`, `test-plan.md`, `bug-investigation.md`, `code-review.md`, `security-review.md`, `release-checklist.md`, `adr.md`, `incident-postmortem.md`, `handoff.md`, `retrospective.md`) **bắt buộc phải được ghi thành file Markdown (`.md`)**.
   - **Vị trí lưu trữ chuẩn theo `rules/deliverables-and-reporting.md`:**
     - Tài liệu dài hạn của dự án: Lưu trong repo (`docs/adr/`, `docs/specs/`, `.agents/memory/entries/`).
     - Báo cáo review, audit, điều tra bug, postmortem, handoff: Mặc định lưu ngoài worktree tại `~/.agents/outputs/<project-name>/reports/YYYY-MM-DD-<loại>-<chủ-đề>-<rev>.md` để tránh làm bẩn `git status` (trừ khi dự án quy định thư mục riêng trong `project.md`). Tuyệt đối không xả file rác ra root repository (`./report.md`, `./review.md`).
   - File deliverable chứa toàn bộ nội dung chi tiết, các mục theo template, bảng biểu, mã finding định danh `F-xx`, đường dẫn file code + số dòng, bằng chứng lệnh chạy và log liên quan.
2. **Kênh Chat (chỉ báo cáo tóm tắt):**
   - Tin nhắn chat đóng vai trò thông báo tóm tắt (Executive Summary) cho người dùng.
   - Nội dung chat chỉ gồm:
     - Tóm tắt kết quả chính trong 3–5 gạch đầu dòng.
     - Các blocker, rủi ro hoặc findings quan trọng nhất (nếu có).
     - **Đường dẫn đầy đủ** đến file deliverable đã ghi để người dùng kiểm tra chi tiết.
   - **Tuyệt đối không** copy/paste toàn bộ nội dung báo cáo hoặc in nguyên khung template dài vào cửa sổ chat.
