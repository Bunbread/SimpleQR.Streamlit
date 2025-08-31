import streamlit as st
import qrcode
from io import BytesIO

# ตั้งค่าเพจ Streamlit
st.set_page_config(page_title="ตัวสร้าง QR Code", page_icon="🔳")

st.title("ตัวสร้าง QR Code")

# กรอกข้อความหรือ URL
data = st.text_input("กรอกข้อความหรือ URL:")

# ตัวเลือกปรับแต่ง
col1, col2 = st.columns(2)
with col1:
    fill_color = st.color_picker("สีของ QR Code", "#000000")
with col2:
    back_color = st.color_picker("สีพื้นหลัง", "#FFFFFF")

col3, col4 = st.columns(2)
with col3:
    box_size = st.slider("ขนาดรูป", 1, 20, 10)
with col4:
    border = st.slider("ขอบ", 0, 10, 4)

col5, col6 = st.columns(2)
with col5:
    error_choice = st.selectbox(
        "ระดับความทนทานต่อข้อผิดพลาด",
        ["L (7%)", "M (15%)", "Q (25%)", "H (30%)"],
        index=1
    )
with col6:
    format_qr = st.selectbox(
        "รูปแบบไฟล์",
        ["PNG", "JPEG"]
    )

# แปลงค่าที่เลือกเป็น constant ของ qrcode
error_map = {
    "L (7%)": qrcode.constants.ERROR_CORRECT_L,
    "M (15%)": qrcode.constants.ERROR_CORRECT_M,
    "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
    "H (30%)": qrcode.constants.ERROR_CORRECT_H,
}

if data is not "":
    # สร้าง QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_map[error_choice],
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # สร้างภาพ QR Code
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    # แปลงภาพเป็น bytes สำหรับแสดงและดาวน์โหลด
    buf = BytesIO()
    img.save(buf, format=format_qr)
    byte_im = buf.getvalue()

    # แสดง QR Code ในแอป
    st.write("")
    st.image(byte_im, caption="QR Code ของคุณ")

    # ปุ่มดาวน์โหลด
    st.download_button(
        label="ดาวน์โหลด QR Code",
        data=byte_im,
        file_name=f"qrcode.{format_qr.lower()}",
        mime=f"image/{format_qr.lower()}"
    )
