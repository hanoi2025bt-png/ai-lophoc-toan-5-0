import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# ==================== CẤU HÌNH ====================
st.set_page_config(page_title="AI LỚP HỌC TOÁN 5.0 – PHIÊN BẢN 2.0", layout="wide")
st.title("🧠 AI LỚP HỌC TOÁN 5.0 – PHIÊN BẢN 2.0")
st.caption("Học thật – Chấm thật – Hiểu thật – 5.0")

# ==================== MENU CHÍNH ====================
menu = st.sidebar.radio("📚 Chọn chức năng:", ["Chấm bài tự luận", "Bảng điểm", "Giới thiệu"])

# ==================== CHẤM BÀI ====================
if menu == "Chấm bài tự luận":
    st.header("✏️ Chấm bài tự luận Toán")
    openai_api_key = st.text_input("🔑 Nhập OpenAI API Key:", type="password")
    de_bai = st.text_area("📘 Đề bài:", height=80)
    bai_lam = st.text_area("📗 Bài làm của học sinh:", height=80)
    ten_hs = st.text_input("👩‍🎓 Tên học sinh:")

    if st.button("🚀 Bắt đầu chấm"):
        if not openai_api_key:
            st.warning("⚠️ Vui lòng nhập OpenAI API Key!")
        elif not bai_lam.strip():
            st.warning("⚠️ Vui lòng nhập bài làm trước khi chấm!")
        else:
            with st.spinner("🤖 Đang chấm bài..."):
                try:
                    client = OpenAI(api_key=openai_api_key)

                    prompt = (
                        f"Hãy chấm bài toán sau, cho điểm (0–10) và viết 1 nhận xét ngắn, rõ ràng:"
                        f"\nĐề: {de_bai}\nBài làm: {bai_lam}"
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4,
                    )
                    ket_qua = response.choices[0].message.content

                    st.success("✅ Kết quả chấm:")
                    st.write(ket_qua)

                    # Ghi điểm vào file
                    try:
                        df_old = pd.read_excel("diem_ai.xlsx")
                    except FileNotFoundError:
                        df_old = pd.DataFrame(columns=["Thời gian", "Học sinh", "Đề", "Bài làm", "Kết quả"])

                    new_data = pd.DataFrame(
                        [[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ten_hs, de_bai, bai_lam, ket_qua]],
                        columns=["Thời gian", "Học sinh", "Đề", "Bài làm", "Kết quả"]
                    )

                    df_new = pd.concat([df_old, new_data], ignore_index=True)
                    df_new.to_excel("diem_ai.xlsx", index=False)
                    st.info("💾 Kết quả đã được lưu vào file diem_ai.xlsx")

                except Exception as e:
                    st.error(f"❌ Lỗi: {e}")

# ==================== BẢNG ĐIỂM ====================
elif menu == "Bảng điểm":
    st.header("📊 Bảng điểm tổng hợp")
    try:
        df = pd.read_excel("diem_ai.xlsx")
        st.dataframe(df)
        st.download_button("⬇️ Tải về file Excel", df.to_csv(index=False).encode('utf-8'), "diem_ai.csv")
    except FileNotFoundError:
        st.warning("⚠️ Chưa có dữ liệu điểm nào!")

# ==================== GIỚI THIỆU ====================
else:
    st.markdown("""
    ## 🌟 GIỚI THIỆU PHIÊN BẢN 2.0
    - ✅ Chấm bài tự luận Toán bằng GPT-4o-mini  
    - ✅ Tự động gợi ý nhận xét, lưu kết quả  
    - ✅ Bảng điểm tổng hợp, tải file Excel  
    - ✅ Hoạt động ổn định, không lỗi API  
    """)
