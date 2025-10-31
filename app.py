import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI
from PIL import Image
import pytesseract

# =================== CẤU HÌNH ===================
st.set_page_config(page_title="AI LỚP HỌC TOÁN 5.0 - PHIÊN BẢN 3.1", layout="wide")
st.title("🧠 AI LỚP HỌC TOÁN 5.0 – PHIÊN BẢN 3.1")
st.caption("Học thật – Chấm thật – Hiểu thật – 5.0")

menu = st.sidebar.radio("🧩 Chọn chức năng:", 
                        ["Chấm bài tự luận", "Chấm bài từ ảnh", "Tạo đề & Soạn bài", "Bảng điểm", "Giới thiệu"])

openai_api_key = st.text_input("🔑 Nhập OpenAI API Key:", type="password")

# =================== CHẤM BÀI TỰ LUẬN ===================
if menu == "Chấm bài tự luận":
    st.header("✏️ Chấm bài tự luận Toán")
    de_bai = st.text_area("📘 Đề bài:")
    bai_lam = st.text_area("📗 Bài làm của học sinh:")
    ten_hs = st.text_input("📛 Tên học sinh:")

    if st.button("🚀 Bắt đầu chấm"):
        if not openai_api_key:
            st.warning("⚠️ Vui lòng nhập OpenAI API Key!")
        elif not bai_lam.strip():
            st.warning("⚠️ Hãy nhập bài làm trước khi chấm!")
        else:
            with st.spinner("⏳ Đang chấm bài..."):
                client = OpenAI(api_key=openai_api_key)
                prompt = f"Hãy chấm bài toán sau, cho điểm (0-10) và nhận xét ngắn gọn:\nĐề bài: {de_bai}\nBài làm: {bai_lam}"
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                )
                ket_qua = response.choices[0].message.content
                st.success("✅ Kết quả chấm:")
                st.write(ket_qua)

                try:
                    df_new = pd.DataFrame([{
                        "Tên học sinh": ten_hs,
                        "Đề bài": de_bai,
                        "Bài làm": bai_lam,
                        "Kết quả": ket_qua,
                        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    }])
                    try:
                        df_old = pd.read_excel("diem_ai.xlsx")
                        df_new = pd.concat([df_old, df_new], ignore_index=True)
                    except FileNotFoundError:
                        pass
                    df_new.to_excel("diem_ai.xlsx", index=False)
                    st.info("📂 Kết quả đã được lưu vào file diem_ai.xlsx")
                except Exception as e:
                    st.error(f"Lỗi khi lưu file Excel: {e}")

# =================== TẠO ĐỀ & SOẠN BÀI ===================
elif menu == "Tạo đề & Soạn bài":
    st.header("⚡ Tạo đề và Soạn bài Toán bằng AI")
    chu_de = st.text_input("📘 Chủ đề:")
    muc_do = st.selectbox("🎯 Mức độ đề:", ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"])
    so_luong = st.slider("📄 Số lượng câu hỏi:", 1, 10, 5)

    if st.button("✨ Tạo đề"):
        if not openai_api_key:
            st.warning("⚠️ Vui lòng nhập OpenAI API Key!")
        else:
            with st.spinner("🧠 Đang tạo đề..."):
                client = OpenAI(api_key=openai_api_key)
                prompt = f"Hãy tạo {so_luong} câu hỏi Toán chủ đề {chu_de}, mức độ {muc_do}, có đáp án ngắn."
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                )
                de_tao = response.choices[0].message.content
                st.success("✅ Đề đã tạo xong:")
                st.write(de_tao)

# =================== BẢNG ĐIỂM ===================
elif menu == "Bảng điểm":
    st.header("📊 Bảng điểm tổng hợp")
    try:
        df = pd.read_excel("diem_ai.xlsx")
        st.dataframe(df)
        st.download_button("⬇️ Tải về file Excel", df.to_csv(index=False).encode('utf-8'), "diem_ai.csv")
    except:
        st.warning("⚠️ Chưa có dữ liệu điểm nào!")

# =================== GIỚI THIỆU ===================
else:
    st.markdown("""
    ### 🧠 GIỚI THIỆU PHIÊN BẢN 3.1
    - ✅ Chấm bài tự luận bằng GPT
    - ✅ Tự động ghi nhận xét và lưu file Excel
    - ✅ Tạo đề và soạn bài theo 4 cấp độ
    - ✅ Bảng điểm tổng hợp trực quan
    - ✅ Hỗ trợ toàn diện cho giáo viên Toán 5.0
    """)
import streamlit as st
import openai
import tempfile

def voice_to_text():
    st.subheader("🎤 Nhập bằng giọng nói")

    audio = st.audio_input("Giữ nút micro và đọc đề bài hoặc bài làm:")

    if audio is not None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(audio.read())
        temp_file.seek(0)

        if st.button("⏳ Chuyển giọng nói thành văn bản"):
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=open(temp_file.name, "rb")
            )
            voice_text = transcript.text
            st.success("✅ Đã nhận dạng giọng nói")
            st.text_area("Nội dung chuyển đổi:", voice_text, height=150)
            st.session_state['voice_input'] = voice_text
            return voice_text

    return None
# --------------------------------------------
# XỬ LÝ DỮ LIỆU BÀI LÀM HỌC SINH (Gõ / Giọng nói / Ảnh OCR)
# --------------------------------------------

# Biến kết quả (phòng trường hợp chưa có dữ liệu)
student_answer = ""

# Nếu thầy vừa chuyển giọng nói thành text phía trên:
try:
    voice_text = voice_to_text()
except NameError:
    voice_text = None

if voice_text:
    student_answer = voice_text

# Chọn phương thức nhập
mode = st.radio(
    "🛠️ Chọn phương thức nhập:",
    ["✍️ Gõ văn bản", "🎤 Giọng nói", "🖼️ Ảnh"]
)

# === Gõ văn bản ===
if mode == "✍️ Gõ văn bản":
    student_answer = st.text_area("✏️ Bài làm học sinh:", "", height=160)

# === Giọng nói ===
elif mode == "🎤 Giọng nói":
    # Nếu chưa có voice_text ở trên thì gọi lại
    if not voice_text:
        student_answer = voice_to_text()
    else:
        student_answer = voice_text

# === Ảnh OCR ===
elif mode == "🖼️ Ảnh":
    uploaded_file = st.file_uploader(
        "📤 Tải ảnh bài làm học sinh", type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file)
            st.image(img, caption="📎 Ảnh bài làm", use_column_width=True)

            with st.spinner("🔍 Đang nhận dạng chữ viết từ ảnh..."):
                # Tesseract với ngôn ngữ Việt + Anh (cải thiện độ chính xác)
                student_answer = pytesseract.image_to_string(
                    img, lang="eng+vie"
                ).strip()

            st.write("📄 **Văn bản OCR trích xuất:**")
            st.text_area("📄 Kết quả OCR", student_answer, height=160)

        except Exception as e:
            st.error(f"⚠️ Không nhận dạng được ảnh: {e}")
            student_answer = ""

# Hiển thị vùng tổng hợp nếu đã có kết quả ở bất kỳ cách nhập nào
if student_answer:
    st.markdown("### ✅ Bài làm (tổng hợp)")
    st.text_area("📦 Nội dung", student_answer, height=200, key="answer_final")

# (Tùy chọn) Lưu vào session_state để dùng tiếp ở bước chấm điểm
st.session_state["student_answer"] = student_answer
