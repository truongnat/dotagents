# Quy chuẩn xuất bản báo cáo và quản lý deliverable

Mọi tác vụ phân tích, review, audit, điều tra lỗi, lập kế hoạch hoặc bàn giao đều phải tuân thủ cấu trúc lưu trữ và quy ước xuất bản dưới đây. Tuyệt đối không tạo file báo cáo rải rác, không rõ nguồn gốc trong repository.

---

## 1. Phân loại tài liệu: Trong Repo (In-Tree) vs Ngoài Repo (Out-of-Tree)

Không phải mọi tài liệu do Agent tạo ra đều được lưu trong git repository. Phải phân định rõ:

| Nhóm | Loại tài liệu | Vị trí lưu trữ | Quản lý Git |
|---|---|---|---|
| **In-Tree (Tài liệu dự án)** | ADR, đặc tả nghiệp vụ (`feature-spec`), tài liệu kiến trúc dài hạn, memory dự án | `docs/adr/`, `docs/specs/`, `.agents/memory/entries/` | Commit cùng mã nguồn trong PR/MR |
| **Out-of-Tree (Báo cáo & Artifacts)** | Báo cáo review diff/PR, audit bảo mật, điều tra lỗi, bằng chứng test, log chạy máy, handoff phiên | `~/.agents/outputs/<project-name>/` | **Không commit vào git** (trừ khi dự án có quy định thư mục báo cáo riêng) |

---

## 2. Cấu trúc lưu trữ chuẩn cho Báo cáo (Out-of-Tree)

Khi tạo báo cáo, đánh giá hoặc artifact không thuộc tài liệu mã nguồn dài hạn, vị trí lưu trữ mặc định là:
`~/.agents/outputs/<project-name>/` (hoặc thư mục riêng được định nghĩa trong `project.md`).

```text
~/.agents/outputs/<project-name>/
├── reports/         # Toàn bộ báo cáo Markdown (code review, security audit, bug investigation, postmortem)
├── artifacts/       # Bằng chứng nhị phân (ảnh chụp UI/screenshot, PDF, Excel matrix, file xuất)
├── testresults/     # Log kiểm thử, benchmark, kết quả test chạy tự động, execution trace
└── notes/           # Ghi chép kỹ thuật nháp, phân tích dữ liệu tạm thời trong phiên
```

> **Nguyên tắc an toàn:** Tuyệt đối không xả file báo cáo tạm, ảnh chụp màn hình, file excel test ra thư mục gốc repository (`./report.md`, `./review.md`, `./evidence.png`). Việc này làm bẩn `git status`, dễ gây commit nhầm file rác vào lịch sử git và gây xung đột khi merge nhánh.

---

## 3. Quy ước đặt tên file báo cáo (Naming Convention)

Tên file báo cáo bắt buộc phải theo cấu trúc định danh sau:

```text
YYYY-MM-DD-<loại-báo-cáo>-<chủ-đề>-<phiên-bản/mã-task>.md
```

Trong đó:
- `YYYY-MM-DD`: Ngày lập báo cáo theo chuẩn ISO (ví dụ: `2026-10-26`).
- `<loại-báo-cáo>`: Loại công việc theo template:
  - `code-review` (Review mã nguồn, PR, MR)
  - `security-review` (Đánh giá an toàn, bảo mật)
  - `bug-investigation` (Điều tra nguyên nhân gốc của bug)
  - `feature-spec` (Đặc tả tính năng)
  - `test-plan` (Kế hoạch kiểm thử)
  - `release-checklist` (Checklist phát hành)
  - `incident-postmortem` (Tổng kết sự cố)
  - `handoff` (Bàn giao công việc giữa các phiên/agent)
- `<chủ-đề>`: Tên ngắn gọn mô tả tính năng hoặc phạm vi (dùng kebab-case, ví dụ: `auth-jwt-refresh`, `export-excel-boundary`).
- `<phiên-bản/mã-task>`: Số hiệu PR/MR, revision hoặc ticket ID (ví dụ: `mr381`, `pr12-rev1`, `issue240`).

### Ví dụ hợp lệ:
- `~/.agents/outputs/my-app/reports/2026-10-26-code-review-mr381-rev01.md`
- `~/.agents/outputs/my-app/reports/2026-10-26-bug-investigation-token-refresh-loop.md`
- `~/.agents/outputs/my-app/artifacts/2026-10-26-ui-test-evidence-login.png`

### CẤM đặt tên:
- `report.md`, `review.md`, `output.md`, `test.md`, `result.md`, `final.md` (dễ bị ghi đè, vô nghĩa khi tra cứu lịch sử).

---

## 4. Tiêu chuẩn nội dung của File Báo cáo (Deliverable)

Mọi file báo cáo Markdown khi xuất ra phải đáp ứng các tiêu chuẩn sau:

1. **Metadata Header:** Đặt ở đầu file:
   - Ngày tạo, tên dự án, đối tượng báo cáo (MR/PR/branch/commit).
   - Tác giả (Agent / Reviewer).
2. **Executive Summary (Kết luận ở đầu):**
   - Đưa ngay kết luận chính lên đầu file: `PASS`, `FAIL`, `BLOCKED` hoặc `APPROVED / REQUEST_CHANGES`.
   - Tóm tắt tác động và rủi ro trong một bảng hoặc đoạn ngắn (để người đọc nắm được ngay mà không cần đọc hết file).
3. **Tính truy vết của Findings (Traceability):**
   - Mọi lỗi/phát hiện phải gắn mã định danh: `F-01`, `F-02`...
   - Mức độ nghiêm trọng: `Critical`, `High`, `Medium`, `Low`, `Suggestion`.
   - **Đường dẫn file chính xác kèm số dòng**: `src/auth/token.ts:45-52` (không viết tắt `.../token.ts`).
   - Bằng chứng thực tế: Đoạn mã lỗi, log thực thi, kết quả test thực tế (không suy diễn).
4. **Bằng chứng kiểm chứng (Verification):**
   - Ghi rõ lệnh thực tế đã chạy, môi trường test, và kết quả kiểm chứng.
   - Phân biệt rõ giữa: Lệnh ĐÃ CHẠY (verified) với Kiểm tra ĐỀ XUẤT (chưa chạy).

---

## 5. Quy ước giao tiếp trong Chat

Sau khi ghi file deliverable thành công, tin nhắn chat của Agent phải tuân thủ:

- **Ngắn gọn, súc tích (Executive Summary):**
  - Tóm tắt kết luận và hành vi chính trong 3–5 bullet points.
  - Nêu ngay các blocker hoặc rủi ro nghiêm trọng (nếu có).
  - **Dẫn đường dẫn đầy đủ** đến file báo cáo để người dùng bấm vào xem:
    ```markdown
    📄 **Báo cáo chi tiết:** `~/.agents/outputs/<project-name>/reports/YYYY-MM-DD-<topic>-<rev>.md`
    ```
- **TUYỆT ĐỐI KHÔNG:**
  - Không dán toàn bộ nội dung file báo cáo vào chat.
  - Không paste log kiểm thử dài hàng trăm dòng vào chat (hãy ghi vào `testresults/` hoặc file artifact tương ứng).
  - Không in lại toàn bộ khung bảng biểu template vào chat.
