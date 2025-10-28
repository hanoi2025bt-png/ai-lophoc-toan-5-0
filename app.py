import streamlit as st
import pandas as pd
import openai
import pytesseract
from PIL import Image
import io
import base64

# --- Cấu hình giao diện ---
st.set_page_config(page_title="AI LỚP HỌC TOÁN 5.0 – PHIÊN BẢN 3.0", page_icon="🧠", layout="centered")
st.title("🧠 AI LỚP HỌC TOÁN 5.0 – PHIÊN BẢN 3.0")
st.subheader("Học thật – Chấm thật – Hiểu thật – 5.0")

# --- Sidebar chức năng ---
st.sidebar.header("📚 Chọn chức năng:")
option = st.sidebar.radio("", ["Chấm bài tự luận", "Chấm bài từ ảnh", "Tạo đề & Soạn bài", "Bảng điểm", "Giới thiệu"])

# --- Nhập API key ---
api_key = st.text_input("🔑 Nhập OpenAI API Key:", type="password")
if not api_key:
    st.warning("⚠️ Vui lòng nhập API key để tiếp tục.")
    st.stop()

openai.api_key = api_key

# --- 1. CHẤM BÀI TỰ LUẬN ---
if option == "Chấm bài tự luận":
    st.header("✏️ Chấm bài tự luận Toán")

    de_bai = st.text_area("📘 Đề bài:")
    bai_lam = st.text_area("📄 Bài làm của học sinh:")
    ten_hs = st.text_input("👩‍🎓 Tên học sinh:")

    if st.button("🚀 Bắt đầu chấm"):
        with st.spinner("Đang chấm bài..."):
            prompt = f"Hãy chấm bài toán sau và cho điểm từ 0–10, có nhận xét rõ ràng:\nĐề: {de_bai}\nBài làm: {bai_lam}"
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )
            ket_qua = response.choices[0].message.content
            st.success("✅ Kết quả chấm:")
            st.write(ket_qua)

            # Lưu điểm vào Excel
            try:
                diem = [s for s in ket_qua.split() if s.replace(".", "").isdigit()]
                diem = float(diem[0]) if diem else None
                data = pd.DataFrame([[ten_hs, de_bai, bai_lam, ket_qua, diem]], 
                                    columns=["Tên HS", "Đề bài", "Bài làm", "Nhận xét", "Điểm"])
                data.to_excel("diem_ai.xlsx", index=False, engine="openpyxl")
            except Exception as e:
                st.error(f"Lỗi khi lưu điểm: {e}")

# --- 2. CHẤM BÀI TỪ ẢNH ---
elif option == "Chấm bài từ ảnh":
    st.header("📷 Chấm bài từ file ảnh")
    uploaded_file = st.file_uploader("Tải ảnh bài làm học sinh:", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh bài làm học sinh", use_container_width=True)
        text = pytesseract.image_to_string(image, lang="eng+vie")
        st.text_area("📝 Văn bản OCR nhận diện được:", text)

        de_bai = st.text_area("📘 Đề bài gốc:")
        if st.button("🚀 Chấm ảnh này"):
            with st.spinner("Đang chấm bài từ ảnh..."):
                prompt = f"Chấm bài toán sau (OCR từ ảnh), cho điểm 0–10 và nhận xét:\nĐề: {de_bai}\nBài làm: {text}"
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                st.success("✅ Kết quả chấm:")
                st.write(response.choices[0].message.content)

# --- 3. TẠO ĐỀ & SOẠN BÀI ---
elif option == "Tạo đề & Soạn bài":
    st.header("🧩 Tạo đề Toán – Soạn bài giảng tự động")
    chu_de = st.text_input("Nhập chủ đề (VD: Bất phương trình bậc nhất hai ẩn, Định lý sin, Vectơ...)")
    so_de = st.slider("Số lượng đề cần tạo:", 1, 10, 5)
    if st.button("⚡ Tạo đề"):
        with st.spinner("Đang tạo đề và soạn bài..."):
            prompt = f"Hãy tạo {so_de} bài toán chủ đề {chu_de} kèm đáp án và gợi ý lời giải chi tiết, ngắn gọn, dễ hiểu cho học sinh lớp 10."
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            st.success("📘 Bộ đề được tạo:")
            st.write(response.choices[0].message.content)

# --- 4. BẢNG ĐIỂM ---
elif option == "Bảng điểm":
    st.header("📊 Bảng điểm AI")
    try:
        data = pd.read_excel("diem_ai.xlsx")
        st.dataframe(data)
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Tải về file điểm (.csv)", csv, "diem_ai.csv", "text/csv")
    except:
        st.info("Chưa có dữ liệu chấm bài nào được lưu.")

# --- 5. GIỚI THIỆU ---
else:
    st.markdown("""
    ### 💡 Giới thiệu
    **AI LỚP HỌC TOÁN 5.0 – PHIÊN BẢN 3.0**  
    👉 Phát triển bởi Thầy Quân & Trợ lý AI Mực Tím.  
    - Chấm bài tự luận, trắc nghiệm, file ảnh  
    - Tạo đề, soạn bài, lưu bảng điểm  
    - Dành riêng cho giáo viên Toán Việt Nam thời đại 5.0.  
    """)
