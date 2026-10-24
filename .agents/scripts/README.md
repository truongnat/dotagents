# Script hỗ trợ

Bộ công cụ vận hành và kiểm tra tính toàn vẹn của dotagents framework:

### 1. Kiểm tra sức khỏe & Xác thực
- `doctor.sh` — Kiểm tra toàn diện hệ thống: thư mục cốt lõi, quyền thực thi, tính hợp lệ của skills, schema của memory và unit tests.
- `validate-skills.sh` — Kiểm tra cơ bản YAML frontmatter, kebab-case và sự trùng khớp giữa `name` với tên thư mục skill.
- `validate-memory.py` — Xác thực các memory entry theo đúng 15 trường frontmatter bắt buộc, enum hợp lệ (`type`, `scope`, `status`, `confidence`) và định dạng ngày ISO theo `memory-policy.md`.
- `test-validate-memory.py` — Unit test cho `validate-memory.py`.
- `test-init-project.sh` — Integration test cho `init-project.sh`.

### 2. Tìm kiếm Memory
- `search-memory.sh` (hoặc `search-memory.py`) — Tìm kiếm tri thức theo thứ tự project → global:
  - Hỗ trợ smart-case và ripgrep (tự động fallback sang Python search nếu máy chưa có `rg`).
  - Hỗ trợ cờ `--archive` để tìm trong kho lưu trữ cũ.
  - Hỗ trợ lọc theo metadata: `--type`, `--status`, `--confidence`, `--tag`.
  - Hỗ trợ cờ `--summary` để in danh sách thẻ tóm tắt nhanh.

### 3. Khởi tạo dự án mới
- `init-project.sh <target-dir>` — Khởi tạo cấu trúc `.agents/` và `AGENTS.md` sang repository đích một cách an toàn (mặc định không ghi đè các file tùy biến như `project.md` hay `AGENTS.md` trừ khi có cờ `--force`).
