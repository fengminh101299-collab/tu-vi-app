import streamlit as st
import os
from google import genai
from PIL import Image

st.set_page_config(page_title="App Tử Vi Cao Cấp - Thực Chiến", layout="centered")

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"
KNOWLEDGE_FILE = "knowledge_base.txt"

def load_knowledge_base():
    if os.path.exists(KNOWLEDGE_FILE):
        try:
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return f"\n\n[KHO KINH NGHIỆM & BÀI HỌC THỰC CHUYẾN ĐÃ TÍCH LŨY]:\n{content}\n"
        except Exception:
            pass
    return ""

SYSTEM_PROMPT_SINGLE = """
Bạn là một Đại sư Tử Vi Đẩu Số Nam Phái Việt Nam am hiểu tường tận lý số thực chiến và THẤU HIỂU TÂM LÝ CON NGUỜI.

YÊU CẦU NGUYÊN TẮC & VĂN PHONG:
1. ĐỌC VỊ TÂM LÝ ĐA CHUYỀN:
   - Không nhìn từ ngữ theo nghĩa đen thô ráp. Phải đọc thấu ngữ cảnh thực tế.
   - Các từ như "rén", "sợ", "ngại" không chỉ là hoảng sợ, mà thường là: NỂ PHỤC, NỂ UY, NỂ ÂN TÌNH, SỢ MẤT LÒNG TIN, hoặc TỰ GIÁC GIỮ RANH GIỚI với người cửa trên.
   - Văn phong sắc sảo, thực tế, phũ đúng trọng tâm nhưng TINH TẾ và TRÚNG TÂM LÝ.

2. VẬN DỤNG KINH NGHIỆM ĐÃ TÍCH LŨY:
   - Hãy bám sát kho kinh nghiệm thực chiến đã được đúc kết tự động ở các ca trước để phân tích ngày càng sắc bén.

3. LUẬN ĐẦY ĐỦ CÁC SAO & 12 CUNG CHIẾM BÀN:
   - Phân tích đầy đủ Chính tinh, Phụ tinh, Cát/Hung tinh, Tuần/Triệt, Tứ Hóa.
   - Trình bày 4 mục: Sao tọa thủ -> Ý nghĩa thực tế -> Điểm mạnh -> Điểm yếu & Bí kíp Hóa giải thực chiến.
""" + load_knowledge_base()

SYSTEM_PROMPT_MULTI_BASE = """
Bạn là một Đại sư Tử Vi Đẩu Số Nam Phái Việt Nam am hiểu tường tận lý số thực chiến và THẤU HIỂU TÂM LÝ CON NGUỜI.
Dưới đây là các BÀN SỐ TỬ VI được gửi lên kèm theo yêu cầu từ người dùng.

YÊU CẦU ĐỌC VỊ & LUẬN GIẢI:
1. ĐỌC THẤU BẢN CHẤT MỐI QUAN HỆ:
   - Phân tích đúng vị thế thực tế (Anh em/Sếp - Nhân viên/Duyên nợ/Đối tác).
   - Phân biệt rõ sự "RÉN" do bị o ép KHÁC HOÀN TOÀN với "RÉN" do NỂ PHỤC, SỢ LÀM PHẬT Ý ÂN NHÂN, hay SỢ RÚT LẠI SỰ CHỐNG LƯƠNG.
   - Vạch rõ "Vạch ranh giới đỏ" để tránh đổ vỡ mối quan hệ.

2. CẤU TRÚC BÁO CÁO:
   - Phân tích tương quan Mệnh - Cục - Tinh đẩu các lá số.
   - Bóc tách thực trạng (Thực tế, phũ nhưng chuẩn tâm lý, áp dụng tri thức va vấp đã đúc kết).
   - Đưa ví dụ tình huống va vấp đời sống thực tế.
   - Phương án Hóa giải xung khắc & Ứng xử thông minh.
""" + load_knowledge_base()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

st.title("🔮 App Tử Vi Cao Cấp - Nam Phái Thực Chiến")

uploaded_files = st.file_uploader("📁 Chọn ảnh Lá số Tử Vi (Tối đa 10 lá)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

col1, col2 = st.columns([3, 2])
with col2:
    if st.button("🧠 Lưu kinh nghiệm ca này vào Bộ Não AI"):
        if st.session_state.messages:
            with st.spinner("AI đang tự chắt lọc bài học mới..."):
                full_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                prompt = f"Từ cuộc trò chuyện Tử Vi này:\n{full_chat}\nHãy rút ra 1-3 câu kinh nghiệm thực chiến/tâm lý thực tế mới (nếu có). Nếu không có thì chỉ ghi NONE."
                res = client.models.generate_content(model=MODEL_NAME, contents=prompt)
                if res.text and "NONE" not in res.text:
                    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
                        f.write(f"\n- {res.text.strip()}\n")
                    st.success("✅ Đã tích lũy bài học mới!")
                else:
                    st.info("Chưa phát hiện kinh nghiệm mới.")
        else:
            st.warning("Chưa có nội dung để lưu!")

if uploaded_files and st.session_state.chat_session is None:
    st.session_state.chat_session = client.chats.create(model=MODEL_NAME)
    img1 = Image.open(uploaded_files[0])
    with st.spinner("⚡ AI đang tự động phân tích & đọc vị Lá số 1..."):
        response = st.session_state.chat_session.send_message([img1, SYSTEM_PROMPT_SINGLE])
        st.session_state.messages.append({"role": "assistant", "content": response.text})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**❓ Bạn:** {msg['content']}")
    else:
        st.markdown(f"**🔮 AI Luận Giải:**\n{msg['content']}")

if prompt := st.chat_input("Nhập câu lệnh / câu hỏi của bạn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("⚡ AI đang xử lý..."):
        if uploaded_files and len(uploaded_files) > 1 and len(st.session_state.messages) == 2:
            imgs = [Image.open(f) for f in uploaded_files]
            response = st.session_state.chat_session.send_message(imgs + [SYSTEM_PROMPT_MULTI_BASE, f"Yêu cầu: {prompt}"])
        else:
            response = st.session_state.chat_session.send_message(prompt)
            
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()
