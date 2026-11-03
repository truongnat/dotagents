# Script hỗ trợ

Bộ công cụ vận hành và kiểm tra tính toàn vẹn của dotagents framework:

### 1. Kiểm tra sức khỏe & Xác thực
- `doctor.sh` — Kiểm tra toàn diện hệ thống: thư mục cốt lõi, quyền thực thi, tính hợp lệ của skills, schema của memory và unit tests.
- `validate-skills.sh` — Kiểm tra cơ bản YAML frontmatter, kebab-case và sự trùng khớp giữa `name` với tên thư mục skill.
- `validate-memory.py` — Xác thực các memory entry theo đúng 15 trường frontmatter bắt buộc, enum hợp lệ (`type`, `scope`, `status`, `confidence`) và định dạng ngày ISO theo `memory-policy.md`.
- `test-validate-memory.py` — Unit test cho `validate-memory.py`.
- `test-init-project.sh` — Integration test cho `init-project.sh`.
- `test-init-global.sh` — Integration test cho `init-global.sh`.

### 2. Tìm kiếm Memory
- `search-memory.sh` (hoặc `search-memory.py`) — Tìm kiếm tri thức theo thứ tự project → global:
  - Hỗ trợ smart-case và ripgrep (tự động fallback sang Python search nếu máy chưa có `rg`).
  - Hỗ trợ cờ `--archive` để tìm trong kho lưu trữ cũ.
  - Hỗ trợ lọc theo metadata: `--type`, `--status`, `--confidence`, `--tag`.
  - Hỗ trợ cờ `--summary` để in danh sách thẻ tóm tắt nhanh.

### 3. Tự học & Đúc kết Kỹ năng (Self-Learning Loop)
- `skill-distiller.py` — Phân tích bài học, kiểm tra trùng lặp (Jaccard similarity) và sinh draft `SKILL.md` chuẩn hóa vào thư mục staging (`.agents/skills/.staging/`).
- `promote-skill.py` — Kiểm tra tính đầy đủ, cú pháp và chuyển draft skill từ staging sang thư mục skills chính thức (project hoặc global).
- `test-skill-distiller.py` — Bộ unit test tự động cho quá trình trích xuất, đối chiếu trùng lặp và promote skill.

### 4. Khởi tạo & Cài đặt
- `init-global.sh [--force] [target-dir]` — Khởi tạo cấu trúc dotagents toàn cục (Global Framework) cho người dùng vào `~/.agents/` (hoặc thư mục đích nếu chỉ định), an toàn không ghi đè trừ khi có `--force`.
- `init-project.sh [--force] <target-dir>` — Khởi tạo cấu trúc `.agents/` và `AGENTS.md` sang repository đích một cách an toàn (mặc định không ghi đè các file tùy biến như `project.md` hay `AGENTS.md` trừ khi có cờ `--force`).
