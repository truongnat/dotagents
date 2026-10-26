# Template phát triển phần mềm

Chọn template theo mức độ rủi ro và giai đoạn công việc; không coi đây là giấy tờ bắt buộc cho mọi thay đổi. Skill tương ứng nằm trong `.agents/skills/` và hướng dẫn cách tạo/kiểm tra đầu ra.

| Template | Skill gợi ý | Dùng khi |
|---|---|---|
| `feature-spec.md` | `requirements-discovery` | Làm rõ vấn đề, phạm vi và tiêu chí nghiệm thu |
| `implementation-plan.md` | `solution-design`, `implementation` | Thay đổi cần chia bước và xác minh |
| `technical-design.md` | `solution-design` | Thiết kế nhiều thành phần hoặc luồng dữ liệu |
| `test-plan.md` | `testing-validation` | Rủi ro/case test cần được review trước |
| `bug-investigation.md` | `bug-investigation` | Tái hiện, giả thuyết, root cause và fix |
| `code-review.md` | `code-review` | Lưu review có nhiều findings |
| `security-review.md` | `security-review` | Thay đổi auth, dữ liệu nhạy cảm hoặc trust boundary |
| `release-checklist.md` | `release-deployment` | Chuẩn bị rollout, smoke test, rollback |
| `adr.md` | `solution-design` | Quyết định kiến trúc có ảnh hưởng dài hạn |
| `incident-postmortem.md` | `incident-response` | Tổng kết sau khi ổn định sự cố |
| `handoff.md` | `handoff-retrospective` | Chuyển phiên/agent hoặc bàn giao task |
| `retrospective.md` | `handoff-retrospective` | Rút bài học có action item cụ thể |
| `memory-evaluation.md` | `memory-curation` | Đo hiệu quả truy xuất/sử dụng memory |

Template trong `.agents/template/` là bản gốc. Khi khởi tạo tài liệu cho task, tuân theo quy chuẩn lưu trữ tại `../../rules/deliverables-and-reporting.md`:
- Tài liệu dự án dài hạn (ADR, feature-spec): lưu trong repo (`docs/adr/`, `docs/specs/`).
- Báo cáo review, audit, bug investigation, handoff: mặc định lưu tại `~/.agents/outputs/<project-name>/reports/YYYY-MM-DD-<loại>-<chủ-đề>-<rev>.md`. Không tạo file rác ở root project.

> **Phân định Chat và File:** Toàn bộ nội dung chi tiết theo template phải được xuất ra **file Markdown (`.md`)**. Không dán nguyên bản template vào chat; chat chỉ đưa kết luận ngắn gọn, blocker chính và đường dẫn file đã tạo.
