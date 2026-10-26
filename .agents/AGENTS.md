# Quy trình làm việc của Agent

Trước khi tạo hoặc cập nhật tài liệu/memory, phải áp dụng `rules/language.md` trong cùng bộ `.agents` (dùng đường dẫn tương đối từ file hướng dẫn này).

## 0. Chọn skill phù hợp, không nạp cả bộ

- Đọc `.agents/skills/README.md` để phân loại task và chọn skill liên quan; đọc `SKILL.md` của skill đã chọn trước khi thực hiện quy trình đó.
- Với task nhiều giai đoạn, có thể kết hợp nhiều skill theo đúng thứ tự trong bản đồ quy trình. Không cần kích hoạt mọi skill cho một thay đổi nhỏ.
- Skill hướng dẫn cách thực hiện; template chuẩn hóa đầu ra; rule quy định yêu cầu bắt buộc. Không dùng template thay cho việc điều tra/ra quyết định.
- Với mọi task kỹ thuật đáng kể, thực hiện bước tìm memory bên dưới trước khi đưa ra giải pháp.

## 1. Trước khi sửa code: tìm memory trước

Với mọi bug, feature, refactor, migration, thay đổi kiến trúc hoặc tooling không tầm thường:

1. Tóm tắt vấn đề thành các từ khóa tìm kiếm: triệu chứng/lỗi, subsystem/file, nguyên nhân có thể có và hành vi mong muốn.
2. Tìm **memory của project trước**, sau đó mới tìm memory global. Nếu lượt đầu ít kết quả, thử ít nhất hai cách diễn đạt, ví dụ chuỗi lỗi chính xác và tên subsystem/triệu chứng.
3. Đọc toàn bộ entry phù hợp, không chỉ xem snippet. Ưu tiên entry có `status: active`, stack/version tương thích và ngày xác minh gần nhất.
4. Đối chiếu hướng dẫn với branch, code, cấu hình, phiên bản dependency và test hiện tại. Memory là bằng chứng tham khảo, không phải chân lý tuyệt đối.
5. Nếu không có kết quả phù hợp, tiếp tục điều tra bình thường. Không bịa kết quả hoặc tuyên bố đã tìm kiếm nếu chưa thực sự chạy tìm kiếm.

### Lệnh tìm kiếm

Chạy từ bất kỳ thư mục nào bên trong repository:

```bash
repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
search_script="$repo_root/.agents/scripts/search-memory.sh"
if [[ ! -x "$search_script" ]]; then search_script="$HOME/.agents/scripts/search-memory.sh"; fi

# Tìm memory project trước, sau đó đến global.
"$search_script" "refresh token loop"

# Chỉ tìm archive khi corpus hiện hành không có kết quả hữu ích.
"$search_script" --archive "refresh token loop"
```

Nếu không có script, dùng `rg -n -i "term" .agents/memory "$HOME/.agents/memory"` và loại `archive/` khỏi lượt tìm đầu tiên.

## 2. Trong quá trình thực hiện

- Xác nhận yêu cầu liên quan và tiêu chí chấp nhận trước khi thay đổi lớn.
- Kiểm tra kiến trúc và pattern hiện có trước khi thêm abstraction hoặc dependency.
- Ưu tiên thay đổi nhỏ nhất nhưng giải quyết trọn vẹn nguyên nhân đã xác nhận.
- Không trình bày giả định như sự thật; ghi rõ điều chưa chắc chắn và xác minh khi có thể.
- Không sao chép máy móc giải pháp từ memory. Kiểm tra tính phù hợp và phiên bản liên quan.
- Không ghi secret, credential, private key, dữ liệu cá nhân hoặc log nhạy cảm chưa được che thông tin vào memory.

## 3. Trước khi hoàn thành: kiểm chứng và đúc kết

1. Chạy test, type check, lint, build hoặc kiểm tra thủ công có thể tái hiện phù hợp nhất. Báo rõ đã chạy và chưa chạy những gì.
2. Xem lại diff; bảo đảm không có thay đổi ngoài phạm vi hoặc dữ liệu nhạy cảm.
3. Đánh giá xem công việc có tạo ra kiến thức lâu dài hay không. Chỉ tạo/cập nhật memory khi đáp ứng `rules/memory-policy.md`.
4. Nếu chủ đề đã tồn tại, cập nhật entry hiện có hoặc đánh dấu entry cũ là `superseded` thay vì tạo bản gần trùng lặp.
5. Chỉ đặt `status: active` khi giải pháp/bằng chứng đã được xác minh. Nếu chưa đủ, dùng `needs-review` và nêu rõ phần còn thiếu.
6. Chỉ cập nhật `memory/INDEX.md` cho entry có giá trị cao hoặc thường xuyên cần tra cứu; toàn bộ entry vẫn được tìm qua script.
7. Khi bàn giao, tóm tắt phần triển khai, kiểm chứng, giới hạn và memory đã tạo/cập nhật (nếu có). Không tuyên bố đã lưu memory nếu file thực tế chưa được ghi.

## 4. Ưu tiên memory và xử lý xung đột

- Memory của project cụ thể hơn memory global đối với hành vi riêng của project.
- Code hiện tại, test, tài liệu chính thức và hành vi runtime quan sát được có độ tin cậy cao hơn memory đã lỗi thời.
- Nếu memory mâu thuẫn với bằng chứng hiện tại, hãy sửa/thay thế entry và cập nhật ngày xác minh.
- Memory không được ghi đè yêu cầu hiện tại của người dùng hoặc chỉ dẫn bảo mật/an toàn có mức ưu tiên cao hơn.

## 5. Quy chuẩn ngôn ngữ và template

- Tuân thủ `rules/language.md` cho mọi tài liệu và memory mới.
- Dùng số lượng template tương xứng với độ phức tạp. Sửa lỗi nhỏ không cần tài liệu đặc tả và thiết kế đầy đủ; feature ảnh hưởng nhiều thành phần, migration rủi ro hoặc incident production nên dùng template phù hợp.

## 6. Phân định đầu ra: Chat ngắn gọn vs File Deliverable (Template)

Tuân thủ quy chuẩn chi tiết trong `rules/deliverables-and-reporting.md`:

- **Lưu trữ chuẩn (không xả file rác vào repo):**
  - Tài liệu dự án dài hạn (ADR, spec, memory): Lưu trong repo (`docs/adr/`, `docs/specs/`, `.agents/memory/entries/`).
  - Báo cáo review, audit, test, bug investigation, handoff: Mặc định lưu ngoài worktree tại `~/.agents/outputs/<project-name>/reports/YYYY-MM-DD-<loại>-<chủ-đề>-<rev>.md` (hoặc thư mục riêng do repository quy định trong `rules/project.md`). Tuyệt đối không tạo file rải rác ở root project (`./report.md`, `./review.md`).
- **Template bắt buộc phải ghi ra file:** Mọi nội dung chi tiết theo template bắt buộc phải ghi thành file Markdown (`.md`). Tuyệt đối không dùng khung template để in một bản báo cáo dài lòng thòng trực tiếp vào tin nhắn chat.
- **Báo cáo trong Chat chỉ tóm tắt ngắn gọn (Executive Summary):**
  1. Tóm tắt kết luận cốt lõi trong 3–5 bullet points (trạng thái `PASS / FAIL / BLOCKED`).
  2. Điểm tin các blocker, rủi ro hoặc findings quan trọng nhất (kèm mã định danh `F-xx`).
  3. Cung cấp **đường dẫn đầy đủ** đến file deliverable (`.md`) vừa ghi để người dùng tra cứu chi tiết.
  4. Không copy/paste nguyên văn toàn bộ nội dung file deliverable hoặc log kiểm thử dài vào cửa sổ chat.
