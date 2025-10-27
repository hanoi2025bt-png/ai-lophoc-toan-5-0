import streamlit as st
import requests
import json

# ---------- Cấu hình trang ----------
st.set_page_config(page_title="AI Lớp học Toán 5.0 – Trường THPT Ba Vì", layout="wide")

st.title("🧮 AI LỚP HỌC TOÁN 5.0 – TRƯỜNG THPT BA VÌ")
st.caption("“Học thật – Chấm thật – Hiểu thật – 5.0”")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Cấu hình")
    api_key = st.text_input("🔑 Nhập OpenAI API key", type="password")
    mathpix_key = st.text_input("📷 Nhập Mathpix API key (nếu có)", type="password")
    model = st.selectbox("Mô hình GPT", ["gpt-4o-mini", "gpt-4o", "gpt-5"])
    st.info("Nhập key rồi chọn tab bên phải để sử dụng!")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["📝 Chấm bài", "📘 Soạn bài", "🧪 Ra đề", "📷 Upload ảnh (OCR)"])

# ---------- TAB 1: Chấm bài ----------
with tab1:
    st.subheader("🧮 Chấm bài tự luận Toán")
    problem = st.text_area("Đề bài", "Giải phương trình 2x + 3 = 7")
    expected = st.text_area("Lời giải mẫu", "2x + 3 = 7 ⇒ 2x = 4 ⇒ x = 2")
    student = st.text_area("Bài làm của học sinh", "2x + 3 = 7 ⇒ 2x = 10 ⇒ x = 5")
    max_score = st.slider("Điểm tối đa", 1, 10, 10)
    if st.button("Chấm điểm và nhận xét", type="primary"):
        if not api_key:
            st.error("❌ Vui lòng nhập OpenAI API key.")
        else:
            st.write("⏳ Đang chấm bài...")
            headers = {"Authorization": f"Bearer {api_key}"}
            prompt = f"""
Bạn là giáo viên Toán. Hãy chấm bài tự luận dưới đây:
Đề: {problem}
Lời giải mẫu: {expected}
Bài làm học sinh: {student}
Hãy phân tích, chỉ ra lỗi sai, cho điểm (thang {max_score}), và nhận xét thân thiện.
"""
            body = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "Bạn là giáo viên Toán cấp THPT Việt Nam."},
                    {"role": "user", "content": prompt}
                ]
            }
            resp = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, json=body)
            data = resp.json()
            if "choices" in data:
                st.success("✅ Hoàn tất chấm bài!")
                st.write(data["choices"][0]["message"]["content"])
            else:
                st.error("Lỗi khi gọi API. Kiểm tra lại key hoặc kết nối mạng.")

# ---------- TAB 2: Soạn bài ----------
with tab2:
    st.subheader("📘 Soạn bài giảng Toán (10 slide)")
    topic = st.text_input("Chủ đề", "Bất phương trình bậc nhất hai ẩn")
    goal = st.text_area("Mục tiêu học tập", "- Hiểu khái niệm\n- Xác định miền nghiệm")
    book = st.selectbox("Bộ sách", ["Cánh Diều", "Kết Nối Tri Thức", "Chân Trời Sáng Tạo"])
    duration = st.number_input("Thời lượng (phút)", 15, 90, 45)
    if st.button("Soạn giáo án 10 slide", type="primary"):
        if not api_key:
            st.error("❌ Vui lòng nhập OpenAI API key.")
        else:
            st.write("🧠 Đang soạn bài giảng...")
            headers = {"Authorization": f"Bearer {api_key}"}
            prompt = f"Soạn bài giảng Toán 10 gồm 10 slide. Chủ đề: {topic}. Bộ sách: {book}. Mục tiêu: {goal}. Thời lượng: {duration} phút."
            body = {"model": model, "messages":[{"role":"user","content":prompt}]}
            resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
            data = resp.json()
            st.success("✅ Hoàn tất soạn bài!")
            st.write(data["choices"][0]["message"]["content"])

# ---------- TAB 3: Ra đề ----------
with tab3:
    st.subheader("🧪 Tạo đề trắc nghiệm Toán")
    chapter = st.text_input("Tên chương hoặc chủ đề", "Hàm số bậc nhất")
    num_qs = st.slider("Số câu hỏi", 5, 30, 10)
    if st.button("Tạo đề và đáp án", type="primary"):
        if not api_key:
            st.error("❌ Vui lòng nhập OpenAI API key.")
        else:
            headers = {"Authorization": f"Bearer {api_key}"}
            prompt = f"Tạo {num_qs} câu hỏi trắc nghiệm Toán lớp 10 chủ đề {chapter}, có 4 lựa chọn A–D và ghi rõ đáp án đúng."
            body = {"model": model, "messages":[{"role":"user","content":prompt}]}
            resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
            data = resp.json()
            st.success("✅ Đề và đáp án đã sẵn sàng!")
            st.write(data["choices"][0]["message"]["content"])

# ---------- TAB 4: OCR ----------
with tab4:
    st.subheader("📷 Nhận dạng công thức Toán học từ ảnh (OCR Mathpix)")
    uploaded = st.file_uploader("Chọn ảnh...", type=["png","jpg","jpeg"])
    if uploaded:
        if not mathpix_key:
            st.warning("⚠️ Nhập Mathpix API key để dùng OCR.")
        else:
            st.write("⏳ Đang xử lý OCR...")
            image_bytes = uploaded.read()
            url = "https://api.mathpix.com/v3/text"
            headers = {
                "app_id": "demo",
                "app_key": mathpix_key,
                "Content-type": "application/json"
            }
            data = {
                "src": f"data:image/jpeg;base64,{image_bytes.decode('latin1')}",
                "formats": ["text", "data", "latex_styled"]
            }
            resp = requests.post(url, headers=headers, json=data)
            st.success("✅ Kết quả OCR:")
            st.json(resp.json())
