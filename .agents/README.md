# `.agents/` — nguồn chuẩn

Thư mục này chứa workflow, quy tắc, điểm mở rộng, script, template và memory lâu dài của repository.

- `AGENTS.md`: hợp đồng làm việc cơ bản cho agent.
- `rules/`: triết lý kỹ thuật (The Zen of GitHub tại `engineering-philosophy.md`), quy chuẩn phát triển phần mềm, chính sách memory, an toàn bảo mật, ngôn ngữ và chuẩn xuất bản báo cáo (`deliverables-and-reporting.md`); tùy chỉnh `project.md` cho từng repository.
- `skills/`: năng lực theo từng loại tác vụ, được đăng ký với agent đang sử dụng.
- `mcp/`: hướng dẫn cấu hình MCP và quyền truy cập.
- `tools/`: công cụ hỗ trợ có hành vi xác định.
- `scripts/`: script tự động hóa khởi tạo toàn cục (`init-global.sh`), dự án (`init-project.sh`), kiểm tra (`doctor.sh`) và tìm kiếm memory (`search-memory.sh`).
- `template/`: template Markdown có thể tái sử dụng cho các giai đoạn kỹ thuật.
- `memory/`: knowledge base có thể tìm kiếm và quản lý bằng version control.
- `outputs/`: lưu trữ báo cáo, artifacts và test results ngoài worktree theo chuẩn `~/.agents/outputs/<project>/`.

Không mặc định rằng công cụ sẽ tự phát hiện mọi thư mục. Hãy đăng ký skill/MCP hoặc cấu hình adapter cho file chỉ dẫn theo cơ chế riêng của agent đó.
