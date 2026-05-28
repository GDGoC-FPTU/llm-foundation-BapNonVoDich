# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Với temperature thấp, câu trả lời thường ngắn gọn, chính xác và nhất quán. Khi temperature tăng, phản hồi trở nên sáng tạo hơn, ít lặp lại và có thể bao gồm các chi tiết bất ngờ hoặc khác biệt. Ở mức cao nhất, model có xu hướng ngẫu nhiên hơn và có thể tạo ra nội dung ít chắc chắn hơn.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ chọn temperature thấp, khoảng 0.2–0.4, để đảm bảo câu trả lời nhất quán, rõ ràng và ít sai lệch. Với hỗ trợ khách hàng, ưu tiên là tính chính xác và an toàn hơn là tính sáng tạo.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Với giá hiện tại, GPT-4o có chi phí tổng cộng khoảng 25 USD cho 1 triệu token, trong khi GPT-4o-mini chỉ khoảng 0.75 USD cho 1 triệu token. Do đó GPT-4o đắt hơn GPT-4o-mini khoảng 30–35 lần cho cùng workload.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o xứng đáng khi cần chất lượng cao, hiểu ngữ cảnh sâu và xử lý yêu cầu phức tạp như phân tích văn bản chuyên sâu, tạo nội dung sáng tạo chất lượng cao hoặc trả lời câu hỏi pháp lý/ tài chính. GPT-4o-mini là lựa chọn tốt hơn khi cần phục vụ nhiều người dùng với chi phí thấp, ví dụ chatbot cơ bản, truy vấn thông tin đơn giản hoặc nhiệm vụ tự động hoá nội dung không yêu cầu đầu ra quá tinh tế.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất khi người dùng tương tác trực tiếp với chatbot và cần phản hồi ngay tức thì, đặc biệt với câu trả lời dài hoặc khi cảm nhận độ trễ rất quan trọng. Non-streaming phù hợp hơn cho các tác vụ batch, xử lý offline hoặc khi cần toàn bộ kết quả hoàn chỉnh trước khi hiển thị, như tạo báo cáo tự động hoặc kiểm tra dữ liệu nội bộ.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
