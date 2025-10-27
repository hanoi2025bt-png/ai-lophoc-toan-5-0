import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Lớp học Toán 5.0 - THPT Ba Vì", page_icon="🧮", layout="wide")

st.title("🧠 AI LỚP HỌC TOÁN 5.0 – TRƯỜNG THPT BA VÌ")
st.caption("“Học thật – Chấm thật – Hiểu thật – 5.0”")

# Sidebar cấu hình
st.sidebar.header("⚙️ Cấu hình")
api_key = st.sidebar.text_input("🔑 Nhập OpenAI API key", type="password")
mathpix_key = st.sidebar.text_input("📸 Nhập Mathpix API key (nếu có)", type="password")
model_name = st.sidebar.selectbox("🧩 Mô hình GPT", ["gpt-4o", "gpt-4o-mini"])

if not api_key:
    st.warning("⚠️ Vui lòng nhập OpenAI API key trước khi sử dụng!")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🧮 Chấm bài", "📘 Soạn bài", "🧩 Ra đề", "📷 OCR Ảnh Toán"])

# ---------------------- TAB 1: CHẤM BÀI ----------------------
with tab1:
    st.subheader("✏️ Chấm bài tự luận Toán")
    de_bai = st.text_area("Đề bài", "Giải phương trình 2x + 3 = 7")
    loi_giai_mau = st.text_area("Lời giải mẫu", "2x + 3 = 7 ⇒ 2x = 4 ⇒ x = 2")
    bai_lam_hs = st.text_area("Bài làm của học sinh", "")
    if st.button("🧾 Chấm điểm và nhận xét"):
        if bai_lam_hs.strip():
            with st.spinner("Đang chấm..."):
                url = "https://api.openai.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": "Bạn là giáo viên Toán giỏi, chấm bài và đưa ra nhận xét chi tiết."},
                        {"role": "user", "content": f"Đề bài: {de_bai}\nLời giải mẫu: {loi_giai_mau}\nBài làm học sinh: {bai_lam_hs}"}
                    ]
                }
                response = requests.post(url, headers=headers, json=payload)
                data = response.json()
                if "choices" in data:
                    st.success("✅ Đã chấm xong!")
                    st.write(data["choices"][0]["message"]["content"])
                elif "error" in data:
                    st.error(f"🚫 Lỗi API: {data['error'].get('message', 'Không rõ lỗi')}")
                else:
                    st.error("⚠️ Kết quả không hợp lệ. Kiểm tra lại API key hoặc model.")

# ---------------------- TAB 2: SOẠN BÀI ----------------------
with tab2:
    st.subheader("📘 Soạn giáo án 10 slide")
    chu_de = st.text_input("Tên chương hoặc bài học", "Bất phương trình bậc nhất 2 ẩn - Toán 10 Cánh Diều")
    thoi_luong = st.number_input("⏱️ Thời lượng (phút)", 15, 90, 45)
    if st.button("🪄 Soạn giáo án 10 slide"):
        with st.spinner("Đang soạn giáo án..."):
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "Bạn là chuyên gia sư phạm, hãy soạn giáo án Toán học sinh THPT dễ hiểu, chia thành 10 slide ngắn gọn."},
                    {"role": "user", "content": f"Soạn giáo án cho bài: {chu_de}, thời lượng {thoi_luong} phút."}
                ]
            }
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            if "choices" in data:
                st.success("✅ Hoàn tất soạn bài!")
                st.write(data["choices"][0]["message"]["content"])
            elif "error" in data:
                st.error(f"🚫 Lỗi API: {data['error'].get('message', 'Không rõ lỗi')}")
            else:
                st.error("⚠️ Không nhận được phản hồi hợp lệ.")

# ---------------------- TAB 3: RA ĐỀ ----------------------
with tab3:
    st.subheader("🧩 Tạo đề trắc nghiệm Toán")
    chuong = st.text_input("Tên chương hoặc chủ đề", "Bất phương trình bậc nhất 2 ẩn - Toán 10 Cánh Diều")
    so_cau = st.slider("Số câu hỏi", 1, 20, 10)
    if st.button("🎯 Tạo đề và đáp án"):
        with st.spinner("Đang tạo đề..."):
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "Bạn là giáo viên Toán, hãy ra đề trắc nghiệm có đáp án rõ ràng, đúng chương trình THPT Việt Nam."},
                    {"role": "user", "content": f"Hãy tạo {so_cau} câu hỏi trắc nghiệm Toán về chủ đề: {chuong}. Ghi rõ đáp án."}
                ]
            }
            response = requests.post(url, headers=headers, json=payload)
            data = response.json()
            if "choices" in data:
                st.success("✅ Đề và đáp án đã sẵn sàng!")
                st.write(data["choices"][0]["message"]["content"])
            elif "error" in data:
                st.error(f"🚫 Lỗi API: {data['error'].get('message', 'Không rõ lỗi')}")
            else:
                st.error("⚠️ Không nhận được phản hồi hợp lệ.")

# ---------------------- TAB 4: OCR ẢNH TOÁN ----------------------
with tab4:
    st.subheader("📷 Nhận dạng công thức Toán học từ ảnh (OCR Mathpix)")
    uploaded = st.file_uploader("📸 Chọn ảnh...", type=["png", "jpg", "jpeg"])
    if uploaded:
        if not mathpix_key:
            st.warning("⚠️ Cần nhập Mathpix API key để dùng OCR.")
        else:
            image_bytes = uploaded.read()
            url = "https://api.mathpix.com/v3/text"
            headers = {
                "app_id": "demo",
                "app_key": mathpix_key,
                "Content-type": "application/json"
            }
            data = {
                "src": "data:image/jpg;base64," + image_bytes.decode("latin1"),
                "formats": ["text", "data"]
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Nhận dạng thành công!")
                st.write(result.get("text", "Không có kết quả nhận dạng."))
            else:
                st.error("🚫 Lỗi khi xử lý OCR. Vui lòng thử lại.")
