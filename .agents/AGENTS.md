# Tiêu chuẩn phát triển toàn cục: Phương pháp luận SPARC (sparc-coder)

Mọi agent và phiên làm việc mặc định tuân thủ **SPARC** (Specification, Pseudocode, Architecture, Refinement, Completion), triết lý kỹ thuật trong `rules/engineering-philosophy.md`, quy chuẩn ngôn ngữ trong `rules/language.md` và quy trình kiểm soát chất lượng dưới đây.

| Phase | Ý nghĩa |
|-------|---------|
| **S** | Mục tiêu, scope, AC, edge cases (`requirements.md` hoặc tóm tắt ngắn khi fix nhỏ) |
| **P** | Phác thảo logic/branch trước code phức tạp |
| **A** | Pattern repo, ranh giới kiến trúc, rủi ro (`context.md` khi cần) |
| **R** | TDD-first, minimal diff, error handling |
| **C** | Verify có evidence — PASS / FAIL / BLOCKED / NOT VERIFIED |

**Độ sâu (tự chọn, không in ra chat):** fix nhỏ → S/C inline; feature vừa → file gate rút gọn; feature lớn / nghiệp vụ mới → full gate + fleet `sdlc-*` (mục 10). Không hỏi user “chọn quy trình” nếu đã suy ra từ task. Độ sâu không miễn cổng phê duyệt ở mục 0.

**Nguồn tri thức (thứ tự):** yêu cầu + file attach → artifact SPARC trong repo → rule project → memory repo/project (script `scripts/search-memory.sh`, xem mục 1) → ai-memory (`memory_query` → `memory_read_page`) → tri thức kỹ thuật & codebase qua XERJ (`xerj_search` / `xerj_def` / `xerj_code_search`) → MCP domain khi cần ticket/MR → hỏi user.

---

## 0. Cổng thực thi — Todo Checklist & phê duyệt (bắt buộc)

Mọi task làm **thay đổi trạng thái** (code, config, file, dữ liệu, hệ ngoài) phải đi qua cổng này trước khi execute:

1. **Lập todo checklist** ngay sau phân tích yêu cầu, trước khi sửa bất cứ gì: mỗi mục = một hành động kiểm chứng được, theo thứ tự, ghi rõ in-scope / out-of-scope. Fix nhỏ: checklist 2–3 dòng.
2. **Trình checklist và dừng chờ user approve.** Không bắt đầu thay đổi khi chưa được duyệt.
3. User yêu cầu sửa → **cập nhật checklist → trình duyệt lại** phần thay đổi, rồi mới execute.
4. Khi execute: tick từng mục theo **bằng chứng thực tế**; phát sinh blocker hoặc phải đổi scope ngoài checklist → dừng, xin duyệt bổ sung; không tự mở rộng phạm vi.
5. Bàn giao: báo cáo trạng thái từng mục theo checklist (`PASS / FAIL / BLOCKED / NOT VERIFIED`) kèm lệnh đã chạy và chưa chạy.
6. **Miễn cổng:** câu hỏi tra cứu, giải thích, đọc thông tin thuần túy không làm thay đổi trạng thái.
7. Fleet `sdlc-*`: agent nền không tự dừng hỏi user; **parent** chịu trách nhiệm xin duyệt checklist và chỉ delegate phạm vi đã duyệt (kèm checklist vào brief).
8. Cổng này là ủy quyền thường trực do user yêu cầu, không thuộc loại "quy trình phê duyệt thủ công vô lý" bị cấm trong `rules/engineering-philosophy.md`.

## 1. Tiếp nhận và phân tích yêu cầu (Requirement Analysis)

- Đọc kỹ yêu cầu, xác định mục tiêu, hành vi mong đợi và phạm vi thay đổi.
- Kiểm tra specs, documents, business rules và code hiện tại.
- Trace luồng nghiệp vụ end-to-end khi ảnh hưởng luồng; không chỉ một module.
- Phân tích dependency, side effects, backward compatibility.
- Xác định điểm mơ hồ, mâu thuẫn; ưu tiên tự xác minh từ dự án.
- Không triển khai khi còn điểm chưa rõ ảnh hưởng kết quả.
- **Tìm memory trước khi đưa ra giải pháp** (task kỹ thuật đáng kể): tóm tắt vấn đề thành từ khóa; chạy `scripts/search-memory.sh "<từ khóa>"` — **memory của project/repo trước, global sau**; nếu không có script, `rg -n -i "<term>" .agents/memory "$HOME/.agents/memory"` và loại `archive/` khỏi lượt đầu. Đọc toàn bộ entry phù hợp (ưu tiên `status: active`), đối chiếu với code/phiên bản hiện tại. Không bịa kết quả hoặc tuyên bố đã tìm kiếm nếu chưa chạy.

## 2. Xây dựng Requirement Checklist

- File `requirements.md` khi feature/significant change (fix nhỏ: bullet trong reply đủ).
- Checkbox REQ-xx, in/out scope, AC kiểm chứng được.
- Requirement checklist là **một phần của todo checklist trình duyệt tại mục 0**; user approve rồi mới chuyển sang kiến trúc/plan.

## 3. Xây dựng Context Checklist

- Trace code, data flow, pattern hiện có; file `context.md` khi subsystem mới hoặc rủi ro cao.
- Tái sử dụng pattern repo; quyết định kỹ thuật ghi ngắn gọn.
- Approved trước plan/implement khi dùng full gate.
- Tra cứu codebase lớn hoặc định nghĩa AST: ưu tiên `xerj_def` / `xerj_search` để lấy chính xác `file:line` và symbol thay vì dùng `grep` thô làm tràn context.

## 4. Definition of Done (DoD)

- File `dod.md`: lệnh verify cụ thể (test, lint, build), regression, UI nếu có.
- Không thêm yêu cầu ngoài scope.

## 5. Task Checklist

- File `tasks.md`: TASK-xx, link REQ, thứ tự, checkbox trạng thái.
- Mỗi task gắn DoD; không task “làm hết”.
- Danh sách task trình user duyệt qua cổng mục 0 trước khi triển khai; chỉ chạy theo task đã duyệt.

## 6. Triển khai (Implementation)

- Thực hiện đúng todo checklist đã được duyệt ở mục 0 và theo `tasks.md`; pseudocode cho logic phức tạp.
- Đọc `~/.agents/skills/karpathy-guidelines/SKILL.md` trước sửa code.
- TDD-first nếu repo có test; minimal diff; không refactor ngoài scope.
- Cập nhật task **completed** chỉ khi có evidence (test chạy).
- Ghi wiki: skill `ai-memory-durable-pages` + user yêu cầu — không tự `memory_write_page`.
- Reference coding: Khi gặp thư viện/API chưa ghi nhớ hoặc lặp lỗi 2 lần, dùng `xerj-code` (`xerj_code_search`) tra cứu giải pháp chuẩn từ kho repo tham khảo trước khi viết code.
- Blocker / đổi scope → dừng, quay lại cổng mục 0 xin duyệt bổ sung, báo user.

## 7. Verification & Self-Review

- Đối chiếu requirements + DoD; chạy lệnh thật.
- PASS / FAIL / BLOCKED / NOT VERIFIED — không PASS khi chưa verify.
- Tóm tắt: changed, verified, risks (bullet).

## 8. Commit & Delivery

- Không commit/push/MR trừ khi user yêu cầu.
- Commit message theo convention repo.

## 9. Quy tắc tối ưu

- Fix nhỏ: checklist rút gọn 2–3 dòng theo mục 0, vẫn cần user duyệt, vẫn verify.
- Feature lớn: full gate + approval.
- Không hỏi lại thông tin đã có; không tài liệu dài trừu tượng.
- Không đọc cả repo; mở rộng theo dependency.
- Không scope creep; ưu tiên đúng & bảo trì hơn tốc độ.

---

## 10. Fleet, skills & MCP (khi delegate hoặc task lớn)

| Vai trò | Agent `~/.agents/agents/…` | Output |
|---------|------------------------------|--------|
| Spec | `sdlc-requirements-analyst` | `requirements.md` |
| Context | `sdlc-context-architect` | `context.md` |
| Plan | `sdlc-planner` | `tasks.md`, `dod.md` |
| Code | `sdlc-implementer` | code, tests |
| Verify | `sdlc-verifier` | vs `dod.md` |
| Review / ship / debug / security | `sdlc-code-reviewer`, `sdlc-ship-readiness`, `sdlc-debugger`, `sdlc-security-auditor` | theo `AGENT.md` |

Playbook: `~/.agents/agents/_shared/SKILLS-MCP.md`. Meta-skill: `using-agent-skills`. Implement: `test-driven-development` + `karpathy-guidelines`. MCP: memory/ticket đọc trước; verify = lệnh local/CI, không thay bằng MCP.

**Chọn skill:** đọc `skills/README.md` để phân loại task và chọn skill liên quan; chỉ nạp `SKILL.md` được chọn, không nạp cả bộ skill. Skill hướng dẫn cách thực hiện; template chuẩn hóa đầu ra; rule quy định yêu cầu bắt buộc.

---

## 11. Báo cáo và Review — File Deliverable

- Tuân thủ quy chuẩn chi tiết tại `rules/deliverables-and-reporting.md`. Mọi yêu cầu review, audit, phân tích hoặc tổng hợp có đầu ra là báo cáo **phải xuất thành file**, kể cả khi không có finding. Trả lời chat đơn thuần không thay thế deliverable. Câu hỏi nhanh và trao đổi thông thường không cần tạo file.
- Mặc định dùng Markdown (`.md`); dùng định dạng khác khi user yêu cầu. Ưu tiên thư mục báo cáo đã có convention; nếu chưa có, lưu ngoài worktree tại `~/.agents/outputs/<project>/reports/YYYY-MM-DD-<topic>-<revision>.md`. Dùng tên mô tả rõ nội dung, không ghi đè báo cáo khác phạm vi/revision.
- **Bố cục chuyên nghiệp, dễ scan:** một tiêu đề rõ ràng; metadata ngắn (ngày, project, đối tượng review, branch/base/head khi có); kết luận và quyết định ở đầu; phạm vi/nguồn; findings; verification; giới hạn/rủi ro còn lại; hành động đề xuất. Chỉ giữ các mục phù hợp, không để heading rỗng.
- Dùng heading phân cấp nhất quán, bảng cho dữ liệu cần đối chiếu và bullet ngắn cho diễn giải. Code/lệnh/log đặt trong fenced block có language. Trình bày gọn, có khoảng trắng; không dùng emoji trang trí, đoạn văn quá dài hoặc lặp cùng nội dung ở nhiều bảng/mục.
- **Finding phải truy vết được:** mã `F-01`, severity/priority, tiêu đề nêu tác động, đường dẫn đầy đủ tính từ root repo + số dòng, điều kiện tái hiện, expected/actual, bằng chứng và đề xuất xử lý. Không rút gọn chỉ còn basename hoặc `.../file`. Phân biệt lỗi do thay đổi đang review, lỗi có sẵn và điểm chưa đủ bằng chứng.
- **Bằng chứng nghiệp vụ:** dẫn tài liệu gốc bằng đường dẫn + dòng hoặc workbook/sheet/cell; tách yêu cầu đã xác nhận với suy luận và yêu cầu cần BA/khách hàng xác nhận. Việc sửa tài liệu trong cùng PR không tự chứng minh thay đổi nghiệp vụ đã được phê duyệt.
- **Verification:** ghi lệnh/scenario thực sự đã chạy, revision/môi trường, kết quả `PASS / FAIL / BLOCKED / NOT VERIFIED` và giới hạn. Phân biệt unit test, smoke với dependency giả lập, API/DB thật và UI end-to-end; không ghi proposed check thành kết quả đã chạy. Log dài giữ ở artifact và dẫn link, không dump vào thân báo cáo.
- **Khi dùng subagent:** parent truyền rõ thư mục output, file riêng cho từng agent và format/evidence contract này. Mỗi agent trả đường dẫn file đã ghi; parent đối chứng, loại trùng và xuất một báo cáo tổng hợp cuối cùng, không chỉ nối nguyên các báo cáo con. Agent nền không tự dừng để hỏi user về hình thức báo cáo.
- **Trước bàn giao:** mở lại file đã xuất; kiểm tra tiêu đề, bảng, fenced block, đường dẫn/link, kết luận và số liệu khớp evidence; bỏ placeholder và thông tin nhạy cảm. Với PDF/Office/HTML, kiểm tra bản render khi có công cụ; không tuyên bố đã kiểm tra trực quan nếu chưa render.
- **Chat bàn giao:** kết luận ngắn, findings/blocker chính và link mở file kèm đường dẫn đầy đủ. Không dán lại toàn bộ nội dung báo cáo vào chat. Quy định upload của từng project vẫn áp dụng; tạo báo cáo local không đồng nghĩa được phép upload hoặc đăng comment.
