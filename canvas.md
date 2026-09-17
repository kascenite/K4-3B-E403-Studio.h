# Canvas 7 dòng — CP1 · Studio.h

1. **Track + đề:** B2 · Trợ lý Discord — nhắc LabCoach các câu hỏi học viên chưa được trả lời.
2. **Job executor:** LabCoach, hàng ngày lúc rảnh, đang lướt Discord để kiểm tra còn câu hỏi học viên nào chưa có người trả lời.
3. **Pain:** LabCoach phải tự lướt và tìm từng câu hỏi chưa được trả lời, việc này lặp lại mỗi ngày nên dễ sót tin và mất thời gian theo kịp kênh.
4. **Bằng chứng đầu:**
   - *Chuẩn B — mining `data/discord-pack/k4_messages.csv`:* tin người (`is_bot=False`) có dấu `?` = **107**; không có tin nào `reply_to` trỏ vào = **23/107 (21%)**. *Cách đếm:* lọc câu có `?`, đối chiếu tập `reply_to`. *Mã minh hoạ:* `M88027` (hỏi gia hạn Lab2, không reply), `M42852` (hỏi cú pháp daily standup, không reply), `M60122` (standup làm ở đâu / làm thế nào, không reply).
   - *Phỏng vấn LabCoach:* anh Tài, Tiến Minh — xác nhận phải thường xuyên lướt Discord để tìm câu chưa trả lời. *(n = 2; log nguyên văn bổ sung trong repo.)*
   - *Baseline bản tin bot `k4_daily_reports.md`:* 2/4 bản cắt cụt giữa câu; nhiều dòng ghi “Đã có phản hồi, chưa xác nhận đã xử lý” — không dùng được để biết câu nào còn tồn.
5. **Lát cắt:** Một LabCoach lúc rảnh · cần biết câu hỏi học viên nào còn chưa được trả lời · AI quyết định tin nào là câu hỏi còn tồn và cần nhắc · LabCoach nhận danh sách ngắn kèm link tin, đỡ phải lướt tay và hạn chế bỏ sót.
6. **AI tự làm đến đâu:** *Tự:* quét tin Discord, phát hiện câu hỏi chưa có trả lời, nhắc LabCoach kèm link. *Không tự:* trả lời học viên, không suy diễn nội dung hay chốt đáp án. *Lý do (cost-of-error):* trả lời thay LabCoach thì thông tin sai đến học viên (deadline/điểm) — đắt; sót câu hỏi thì LabCoach chịu, nên máy chỉ nhắc, người mới trả lời. **Willing users (ngoài nhóm):** anh Tài (LabCoach), Tiến Minh (LabCoach). *(cần chốt thêm 1 người nếu làm R6.)*
7. **Phân công:** Lương Sỹ Khánh — Discord integration + phát hiện tin · Văn Quốc Dũng — quản lý + QA · Nguyễn Đức Thịnh — backend/web + notification · Đào Quang Thái Anh — AI logic + LangGraph workflow.

Sau khi chốt, copy vào `spec.md` §1–§2.
