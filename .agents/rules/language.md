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
## Tự kiểm tra trước khi lưu

- [ ] Phần diễn giải dùng một ngôn ngữ nhất quán theo quy tắc trên.
- [ ] Không dịch tên trường, enum, API, code hoặc lệnh.
- [ ] Không trộn hai ngôn ngữ trong cùng câu nếu không có lý do kỹ thuật.
- [ ] Ví dụ, tiêu đề và placeholder hướng dẫn người dùng viết nội dung bằng ngôn ngữ mặc định.
- [ ] Giọng điệu rõ ràng, tự nhiên, không sáo rỗng hoặc áp đặt (Tone of Voice).
