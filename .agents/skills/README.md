# Skills — năng lực theo tác vụ

Skill mô tả **cách thực hiện một loại công việc**; template mô tả **đầu ra cần tạo**; rule nêu **điều bắt buộc**. Không trộn ba vai trò này và không nạp tất cả skill cho mỗi task.

## Skill điều phối

- `software-lifecycle/SKILL.md` — phân loại task, chọn skill/template, kiểm tra cổng chất lượng.

## Bản đồ vòng đời phần mềm

| Giai đoạn/tình huống | Skill chính | Template có thể dùng |
|---|---|---|
| Làm rõ feature | `requirements-discovery` | `feature-spec.md` |
| Thiết kế/API/data/kiến trúc | `solution-design` | `technical-design.md`, `adr.md`, `implementation-plan.md` |
| Viết hoặc sửa code | `implementation` | `implementation-plan.md` khi cần |
| Điều tra bug | `bug-investigation` | `bug-investigation.md` |
| Refactor giữ nguyên hành vi | `refactoring` | `test-plan.md` khi cần |
| Test và kiểm chứng | `testing-validation` | `test-plan.md` |
| Review diff | `code-review` | `code-review.md` |
| Auth, dữ liệu nhạy cảm, trust boundary | `security-review` | `security-review.md` |
| Release/deploy/migration | `release-deployment` | `release-checklist.md` |
| Sự cố đang ảnh hưởng dịch vụ | `incident-response` | `incident-postmortem.md` sau khi ổn định |
| Tìm/cập nhật/đúc kết memory | `memory-curation` | `memory-entry.md`, `memory-evaluation.md` |
| Bàn giao hoặc tổng kết | `handoff-retrospective` | `handoff.md`, `retrospective.md` |

## Chuỗi quy trình mẫu

- **Bug:** `memory-curation` (tìm trước) → `bug-investigation` → `testing-validation` → `code-review` → `memory-curation` (đúc kết nếu hữu ích).
- **Feature:** `memory-curation` (tìm trước) → `requirements-discovery` → `solution-design` nếu cần → `implementation` → `testing-validation` → `security-review` nếu có rủi ro → `code-review` → `memory-curation`.
- **Refactor:** `memory-curation` (tìm trước) → `refactoring` → `testing-validation` → `code-review`.
- **Release:** `release-deployment` → sau sự cố thì `incident-response` → `handoff-retrospective`/`memory-curation` khi có bài học.

## Quy ước viết skill

- Mỗi skill là một thư mục chứa `SKILL.md` có YAML frontmatter gồm `name` và `description`; `name` phải trùng tên thư mục và dùng kebab-case.
- Nội dung diễn giải viết bằng tiếng Việt theo `rules/language.md`; giữ nguyên tên kỹ thuật và field có cấu trúc.
- Mỗi skill nêu: khi nào dùng, khi nào không dùng, quy trình, quy tắc, điều kiện hoàn tất và template/tham chiếu liên quan.
- Nêu trigger đủ cụ thể để agent có thể chọn skill từ phần mô tả mà không phải nạp nội dung toàn bộ.
- Giữ skill tập trung; nội dung dài hoặc chuyên sâu nên tách thành `references/` thay vì phình `SKILL.md`.

## Lưu ý về tương thích

Có thư mục `skills/` không đồng nghĩa mọi coding agent sẽ tự động phát hiện skill. Agent cần hỗ trợ định dạng Agent Skills và được cấu hình đúng thư mục. Một số công cụ đòi thư mục skills riêng; khi đó dùng adapter hoặc symlink được kiểm tra, nhưng vẫn giữ `.agents/skills/` làm nguồn chuẩn trong repository này.
