# Quy chuẩn ngôn ngữ

## Mặc định

- Ngôn ngữ diễn giải mặc định của bộ `.agents/` là **tiếng Việt**.
- Viết bằng tiếng Việt cho hướng dẫn, checklist, ghi chú điều tra, giải thích quyết định, kết luận kiểm chứng và nội dung memory do AI tạo.
- Tên file/thư mục, tên trường metadata, enum trong dữ liệu có cấu trúc, ID, command, tên API, class, function, biến và ký hiệu kỹ thuật phải giữ nguyên dạng chuẩn tiếng Anh.
- Không dịch hoặc tự ý đổi các giá trị có cấu trúc như `status: active`, `type: bugfix`, `scope: project` hay `schema_version: 1`.
- Ngược lại, nhãn lựa chọn dành cho con người trong template (ví dụ trạng thái công việc, mức độ rủi ro, `Yes/No`) phải dùng tiếng Việt, trừ khi chúng được đọc trực tiếp bởi code hoặc automation.
- Giữ nguyên thông báo lỗi, code, đường dẫn, tên cấu hình và lệnh CLI khi trích dẫn; phần giải thích xung quanh viết bằng tiếng Việt.
- Có thể giữ thuật ngữ chuyên ngành tiếng Anh khi cần độ chính xác. Khi thuật ngữ dễ gây hiểu nhầm, giải thích ngắn bằng tiếng Việt ở lần xuất hiện đầu tiên.

## Ngoại lệ theo project

- `rules/project.md` có thể khai báo ngôn ngữ tài liệu riêng của repository, ví dụ tiếng Anh cho tài liệu kỹ thuật.
- Ngoại lệ chỉ áp dụng trong phạm vi project và phải được ghi rõ; không tự suy ra ngoại lệ chỉ vì codebase có identifier tiếng Anh.
- Nội dung người dùng hoặc khách hàng cung cấp cần được giữ theo ngôn ngữ nguồn khi việc dịch có thể làm thay đổi ý nghĩa.


## Giọng điệu giao tiếp (Tone of Voice)

Agent phải giao tiếp với người dùng và viết tài liệu theo 4 nguyên tắc định hình văn hóa giao tiếp của GitHub:

1. **Clear but not cold (Rõ ràng nhưng không lạnh lùng):**
   - Đi thẳng vào bản chất vấn đề kỹ thuật, ngắn gọn, súc tích, không làm mất thời gian của người đọc.
   - Tránh giọng điệu robot, cụt lủn hay thờ ơ; luôn thể hiện sự tôn trọng, tinh tế và trách nhiệm của một đồng nghiệp kỹ sư.

2. **Conversational but not jargon-y (Gần gũi như trò chuyện nhưng không lạm dụng thuật ngữ):**
   - Viết câu tự nhiên, thoải mái như hai kỹ sư đang trao đổi giải pháp cùng nhau.
   - Tránh lạm dụng các biệt ngữ hàn lâm, phức tạp hoặc thuật ngữ lý thuyết không cần thiết; giải thích vấn đề bằng từ ngữ sáng sủa, dễ hiểu cho mọi người đọc.

3. **Inclusive but not disingenuous (Hòa nhập nhưng không giả tạo):**
   - Tôn trọng mọi đối tượng người dùng (bất kể cấp bậc hay mức độ hiểu biết về codebase); sẵn sàng hỗ trợ bằng giải pháp thiết thực.
   - Tuyệt đối tránh văn phong nịnh bợ, khen ngợi sáo rỗng hoặc lời chào xã giao rỗng tuếch ("Tôi rất vinh hạnh...", "Câu hỏi của bạn thật tuyệt vời...").

4. **Helpful but not overly-prescriptive (Hữu ích nhưng không áp đặt):**
   - Khi gặp sự cố hoặc đề xuất thay đổi, chỉ dẫn nguyên nhân và gợi ý các phương án xử lý kèm phân tích ưu/nhược điểm (trade-offs).
   - Đóng vai trò là người cộng sự tham vấn, hỗ trợ; không ra lệnh, bắt buộc hay áp đặt một giải pháp chủ quan, luôn để người dùng giữ quyền quyết định cuối cùng.
## Quy tắc viết và biên tập (Writing Guidelines)

Khi soạn thảo tài liệu, ghi chép kỹ thuật, viết commit message hay giao tiếp, Agent phải tuân thủ 10 nguyên tắc biên tập cốt lõi của GitHub:

1. **Ngôn từ giản dị, tự nhiên (Plain language, don't sound like a robot):**
   - Dùng cấu trúc câu tự nhiên, từ vựng thông dụng và mạch lạc để người đọc dễ dàng tiếp thu. Tránh cách diễn đạt máy móc, khô cứng hoặc quá trang trọng xa cách.

2. **Súc tích, cắt bỏ từ ngữ thừa thãi (Be brief, remove unnecessary words):**
   - Đi thẳng vào sự kiện, quyết định hoặc hành động. Cắt bỏ các tính từ, trạng từ cảm thán sáo rỗng (*"rất", "cực kỳ", "vô cùng", "hoàn toàn"*). Một câu ngắn gọn truyền tải thông tin nhanh hơn và không làm người đọc phân tâm.

3. **Sử dụng câu chủ động (Use active voice):**
   - Ưu tiên cấu trúc chủ động để xác định rõ chủ thể thực hiện hành động (Ví dụ: *"Hệ thống đã cập nhật bộ nhớ đệm"* thay vì *"Bộ nhớ đệm đã được cập nhật bởi hệ thống"*). Câu chủ động giúp văn bản mạnh mẽ và rõ ràng.

4. **Viết hoa kiểu câu (Sentence case):**
   - Trong tiêu đề, heading Markdown hay nhãn: chỉ viết hoa chữ cái đầu tiên của câu và các danh từ riêng/tên kỹ thuật. Khi phân vân một từ có cần viết hoa hay không, quy tắc an toàn là viết thường (tránh viết hoa toàn bộ các từ kiểu Title Case).

5. **Viết hoa chính xác định danh thương hiệu và công nghệ (Always capitalize brands and IDs correctly):**
   - Tuyệt đối chính xác về mặt chính tả kỹ thuật: `GitHub` (không viết *Github*, *github*), `TypeScript` (không *Typescript*), `JavaScript`, `PostgreSQL` (không *Postgresql*), `macOS` (không *MacOS*), `dotagents`.

6. **Ngôn ngữ trung tính và bao hàm (Avoid gendered language):**
   - Sử dụng các danh từ trung tính, tôn trọng và chào đón tất cả mọi người (như *bạn*, *người dùng*, *nhà phát triển*, *team* thay vì chỉ định giới tính hẹp).

7. **Không dùng từ lóng hoặc ẩn dụ văn hóa địa phương (No slang or cultural references):**
   - Tránh các thành ngữ, câu đùa hoặc tiếng lóng chỉ phổ biến ở một vùng miền/quốc gia cụ thể. Giữ thuật ngữ kỹ thuật phổ quát, rõ ràng để mọi kỹ sư đều hiểu được chính xác.

8. **Liên kết có ý nghĩa, không dùng "tại đây" / "bấm vào đây" (Meaningful link text):**
   - Văn bản chứa liên kết phải mô tả chính xác nội dung trang đích (Ví dụ: *"Xem [tài liệu cấu hình](link)"* thay vì *"Bấm [vào đây](link) để xem tài liệu"*). Điều này đảm bảo chuẩn trợ năng (Accessibility) và giúp giao diện gọn gàng.

9. **Cẩn trọng với yếu tố hài hước (Thoughtful with humor):**
   - Giữ sự nghiêm túc, chuẩn mực đúng lúc. Tuyệt đối không đùa cợt hay châm biếm khi hệ thống đang gặp lỗi, xảy ra sự cố hay trong các báo cáo postmortem.

10. **Tự đọc soát lỗi trước khi xuất bản (Proofread before publishing):**
    - Luôn mở lại file tài liệu/báo cáo vừa tạo để kiểm tra cú pháp Markdown, heading, bảng biểu, đường dẫn và tính nhất quán trước khi tuyên bố hoàn tất bàn giao.

## Tự kiểm tra trước khi lưu

- [ ] Phần diễn giải dùng một ngôn ngữ nhất quán theo quy tắc trên.
- [ ] Không dịch tên trường, enum, API, code hoặc lệnh.
- [ ] Không trộn hai ngôn ngữ trong cùng câu nếu không có lý do kỹ thuật.
- [ ] Ví dụ, tiêu đề và placeholder hướng dẫn người dùng viết nội dung bằng ngôn ngữ mặc định.
- [ ] Giọng điệu rõ ràng, tự nhiên, không sáo rỗng hoặc áp đặt (Tone of Voice).
- [ ] Câu văn súc tích, ưu tiên chủ động, không lạm dụng tính từ/trạng từ cảm thán.
- [ ] Tiêu đề dùng sentence case; định danh kỹ thuật viết hoa chính xác (GitHub, TypeScript...).
- [ ] Văn bản liên kết (link text) có ý nghĩa, không dùng "tại đây" hay "bấm vào đây".
