# `.agents` — Bộ khung workflow và memory cho AI coding agent

Mục tiêu là biến memory thành **knowledge base có thể tìm kiếm, kiểm chứng, cập nhật và quản lý bằng version control**, thay vì ghi lại mọi thứ một cách tự động.

## 1. Nguyên tắc thiết kế

1. **Một nguồn chuẩn:** quản lý rule, skill, MCP, tool, script, template và memory trong `.agents/`.
2. **Tìm trước khi làm:** với task kỹ thuật đáng kể, tìm memory project trước rồi global; đọc entry phù hợp và xác minh còn đúng với code/dependency hiện tại.
3. **Chỉ lưu kiến thức có giá trị lâu dài:** ưu tiên root cause khó nhận biết, lỗi đã giải quyết, quyết định kiến trúc, workaround có điều kiện, lỗi có thể tái diễn hoặc quy trình đã kiểm chứng.
4. **Bằng chứng quan trọng hơn lời kể:** memory nêu rõ cách xác minh, phạm vi/phiên bản áp dụng và nguồn liên quan.
5. **Bắt đầu bằng Markdown + Git:** dùng `rg`/`grep` trước. Chỉ thêm vector search, database hoặc memory service khi benchmark chứng minh cách tìm hiện tại không đủ.
6. **Không lưu bí mật:** không đưa token, mật khẩu, private key, dữ liệu cá nhân hoặc log chứa thông tin nhạy cảm vào memory.
7. **Ngôn ngữ nhất quán:** nội dung diễn giải mặc định bằng tiếng Việt; định danh kỹ thuật và metadata có cấu trúc giữ nguyên tiếng Anh. Quy tắc chi tiết nằm trong `.agents/rules/language.md`.

## 2. Cấu trúc

```text
~/.agents/                         # Global: cách làm việc và kiến thức dùng lại được
├── AGENTS.md
├── skills/
├── rules/
├── mcp/
├── tools/
├── scripts/
├── template/
└── memory/
    ├── INDEX.md
    ├── entries/{bugfixes,decisions,patterns,workflows,environment}/
    └── archive/YYYY/

<repo>/
├── AGENTS.md                      # Entry point để agent đọc quy chuẩn
└── .agents/                       # Quy tắc, template, memory, tool riêng của project
    ├── AGENTS.md
    ├── rules/project.md
    └── memory/...
```

Trong bộ mẫu này, các file cấu hình tùy chỉnh nằm dưới `.agents/`; `AGENTS.md` ở root project là **entry point/adapter** để agent phát hiện và đọc các chỉ dẫn đó.

### Phân chia global và project

- **Global:** cách làm việc chung, pattern tái sử dụng qua nhiều repository, lỗi/cạm bẫy phổ quát.
- **Project:** kiến trúc repo, quy ước nghiệp vụ, quyết định riêng, bugfix phụ thuộc code/dependency, lệnh test/build/deploy riêng.
- Không tự động đưa memory của project lên global. Chỉ nâng cấp khi đã loại bỏ chi tiết nội bộ và xác nhận kiến thức có thể tái sử dụng.
- Rule cụ thể của project được ưu tiên trong phạm vi project, nhưng không được ghi đè yêu cầu bảo mật hoặc chỉ dẫn có mức ưu tiên cao hơn.

## 3. Cài đặt

### Global

1. Sao chép thư mục `.agents/` trong gói này vào `~/.agents/`.
2. Cấu hình agent để đọc `~/.agents/AGENTS.md` theo cơ chế global instruction riêng của công cụ. **Không phải agent nào cũng tự động đọc `~/.agents/`**; `.agents/` là quy ước lưu trữ, không phải cơ chế tự nạp dùng chung cho mọi công cụ.
3. Cấp quyền thực thi cho script: `chmod +x ~/.agents/scripts/search-memory.sh`.

### Mỗi project

1. Sao chép `.agents/` vào thư mục gốc repository.
2. Sao chép `AGENTS.md` trong gói này vào thư mục gốc repository.
3. Điền `.agents/rules/project.md`: stack, lệnh kiểm tra, kiến trúc và ràng buộc riêng.
4. Chạy `git status` để xác nhận chỉ commit file phù hợp. Không đưa credential hoặc dữ liệu nhạy cảm vào repo.

### Tích hợp công cụ khác

Nếu công cụ đang dùng không đọc `AGENTS.md`, hãy dùng file instruction/config riêng của công cụ làm adapter ngắn trỏ về cùng một nguồn `.agents/`. Tránh duy trì nhiều bộ quy tắc độc lập. Chỉ dùng symlink khi công cụ và hệ điều hành hỗ trợ ổn định.

## 4. Skills và template phối hợp với nhau

Bộ khung có các skill theo vòng đời: khám phá yêu cầu, thiết kế giải pháp, implement, điều tra bug, kiểm thử, code review, security review, release/deployment, incident response, refactor, memory curation và handoff/retrospective. Xem `.agents/skills/README.md` để chọn skill theo task.

- **Skill** hướng dẫn quy trình hành động, trigger và tiêu chí hoàn tất.
- **Template** định dạng tài liệu/đầu ra khi thực sự cần.
- **Rule** nêu ràng buộc cần áp dụng xuyên suốt.

Không nạp toàn bộ skill cùng lúc. Chọn skill phù hợp; task nhỏ dùng luồng rút gọn, task lớn/rủi ro cao đi qua các cổng kiểm chứng đầy đủ. Skills phải được agent hỗ trợ và cấu hình đúng thư mục mới tự động phát hiện; chỉ lưu file vào `.agents/skills/` chưa đảm bảo mọi công cụ đã nạp chúng.

## 5. Quy trình chuẩn

```text
Phân loại task
  → Tìm memory (project → global)
  → Đọc entry phù hợp và xác minh tính hiện hành
  → Điều tra / thiết kế / triển khai
  → Chạy kiểm chứng phù hợp
  → Cập nhật hoặc tạo memory nếu có kiến thức tái sử dụng
  → Review diff, kiểm tra trạng thái memory và bàn giao
```

Chi tiết nằm trong `.agents/AGENTS.md`, `.agents/rules/memory-policy.md` và `.agents/rules/software-development.md`.

## 6. Đo hiệu quả, không đánh giá bằng cảm giác

Tạo benchmark nhỏ gồm 10–20 câu hỏi/task đã từng gặp và xác định trước entry nào đáng lẽ cần tìm thấy. Đo:

- **Recall@5:** tỷ lệ case có memory đúng trong 5 kết quả đầu.
- **Precision@5:** tỷ lệ kết quả trong top 5 thực sự hữu ích.
- **Adoption rate:** tỷ lệ task liên quan mà agent áp dụng memory đúng.
- **Stale-memory rate:** tỷ lệ memory lỗi thời/mâu thuẫn với bằng chứng hiện tại khi được truy xuất.
- **Kết quả:** thời gian điều tra, tỷ lệ giải quyết thành công và mức độ tái diễn lỗi.

Dùng `.agents/template/software/memory-evaluation.md` để ghi kết quả. Chỉ nâng cấp search engine khi dữ liệu cho thấy `rg` + taxonomy + metadata không đủ đáp ứng.
