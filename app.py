import streamlit as st
import os
import asyncio
import yt_dlp
import whisper
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip

# Cấu hình giao diện chuẩn Dark Mode và chia tỷ lệ màn hình rộng
st.set_page_config(page_title="TikTok -> Faceless AI", layout="wide", initial_sidebar_state="collapsed")

# Thiết lập Mật khẩu bảo mật nội bộ cho Team
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]: return True
    st.title("🔐 Hệ thống nội bộ Team Faceless AI")
    pwd = st.text_input("Nhập mật khẩu sử dụng tool:", type="password")
    if st.button("Đăng nhập"):
        if pwd == "123456": # ĐỔI MẬT KHẨU CỦA BẠN TẠI ĐÂY
            st.session_state["password_correct"] = True
            st.rerun()
        else: st.error("Sai mật khẩu!")
    return False

if not check_password(): st.stop()

# Tối ưu CSS để giao diện đổi màu Tím / Đen huyền ảo y hệt ảnh demo
st.markdown("""
<style>
    .main { background-color: #0b0d13 !important; color: #e6edf3; }
    div[data-testid="stBlock"] { background-color: #121620; border-radius: 12px; padding: 20px; border: 1px solid #1f2635; margin-bottom: 15px; }
    h1, h2, h3, p, span, label { color: #ffffff !important; font-family: 'Segoe UI', sans-serif; }
    .stButton>button { background-color: #7952b3 !important; color: white !important; border-radius: 8px !important; border: none !important; font-weight: bold; width: 100%; height: 45px; }
    .stButton>button:hover { background-color: #613d96 !important; }
    .render-btn>div>button { background-color: #6f42c1 !important; }
    .download-btn>div>button { background-color: #198754 !important; }
    .stTextArea textarea { background-color: #090b11 !important; color: #00ffcc !important; border: 1px solid #283149 !important; font-size: 15px; }
    .step-done { color: #a370f7 !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# TIÊU ĐỀ CHÍNH
st.title("TikTok ➔ Faceless AI 🎬")
st.caption("Tái chế nội dung TikTok thành video ngắn chuyên nghiệp chỉ với 1–Click")
st.write("---")

# CHIA THÀNH 3 CỘT CHUẨN Y NHƯ ẢNH DEMO ĐỐI THỦ
col_left, col_center, col_right = st.columns([1, 1.3, 1])

# --- CỘT 1: CẤU HÌNH ĐẦU VÀO (BÊN TRÁI) ---
with col_left:
    st.markdown("### 📋 Quy Trình Tạo Video")
    st.markdown("<p class='step-done'>✓ Dán Link Video</p><p style='font-size:13px; color:#8b949e; margin-top:-15px; margin-left:20px;'>Nhập URL TikTok & chọn giọng đọc</p>", unsafe_allow_html=True)
    st.markdown("<p class='step-done'>✓ AI Phân Tích</p><p style='font-size:13px; color:#8b949e; margin-top:-15px; margin-left:20px;'>Tải âm thanh & Nhận dạng chữ</p>", unsafe_allow_html=True)
    st.markdown("<p class='step-done'>✓ Biên Tập Nội Dung</p><p style='font-size:13px; color:#8b949e; margin-top:-15px; margin-left:20px;'>Sửa đổi kịch bản, ảnh bìa & Outro</p>", unsafe_allow_html=True)
    st.markdown("<p class='step-done'>✓ Dựng Video</p><p style='font-size:13px; color:#8b949e; margin-top:-15px; margin-left:20px;'>Lồng tiếng, ghép nền phong cảnh</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8b949e;'>○ Tải Kết Quả</p><p style='font-size:13px; color:#8b949e; margin-top:-15px; margin-left:20px;'>Nhận file video chất lượng cao</p>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Cấu Hình Đầu Vào")
    channel_name = st.text_input("BUỚC 1 · KÊNH NỘI DUNG", value="Sim HH - Phong Thuỷ")
    tiktok_url = st.text_input("BƯỚC 2 · ĐƯỜNG DẪN VIDEO TIKTOK", placeholder="https://vt.tiktok.com/...")
    
    voice_option = st.selectbox(
        "GIỌNG ĐỌC THUYẾT MINH (AI)",
        options=["vi-VN-HoaiMyNeural (Nữ – Hoài My)", "vi-VN-NamMinhNeural (Nam – Nam Minh)"]
    )
    selected_voice = voice_option.split(" ")[0]
    
    btn_analyze = st.button("🚀 Phân Tích Video Đối Thủ")

# --- CỘT 2: BIÊN TẬP NỘI DUNG (Ở GIỮA) ---
with col_center:
    st.markdown("### 🛠️ Kịch bản & Thiết lập")
    
    # Khởi tạo session state để lưu trữ văn bản kịch bản
    if btn_analyze and tiktok_url:
        with st.spinner("📥 Đang cào dữ liệu và bóc băng chữ từ TikTok..."):
            try:
                ydl_opts = {'format': 'bestaudio', 'outtmpl': 'temp_audio', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([tiktok_url])
                
                model = whisper.load_model("base")
                result = model.transcribe("temp_audio.mp3", language="vi")
                st.session_state['script'] = result['text']
                st.success("🤖 AI đã bóc chữ thành công!")
            except Exception as e:
                st.error(f"Lỗi tải video: {e}. Vui lòng kiểm tra lại đường link!")

    if 'script' in st.session_state:
        st.markdown("**NỘI DUNG ĐĂNG TẢI ĐỀ XUẤT**")
        edited_script = st.text_area("Chỉnh sửa lại nội dung kịch bản tại đây để tránh quét bản quyền:", value=st.session_state['script'], height=280)
        
        st.write(f"🎙️ Giọng thuyết minh đang chọn: **{voice_option.split(' ')[1]}**")
        
        st.markdown("<div class='render-btn'>", unsafe_allow_html=True)
        btn_render = st.button("🔮 Dựng Lại Video (Render)")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("💡 Vui lòng dán link TikTok ở cột bên trái và nhấn nút 'Phân Tích Video Đối Thủ' để lấy kịch bản văn bản.")

# --- CỘT 3: XEM TRƯỚC & TẢI KẾT QUẢ (BÊN PHẢI) ---
with col_right:
    st.markdown("### 📺 Xem Trước Video")
    
    if 'script' in st.session_state and 'btn_render' in locals() and btn_render:
        with st.spinner("⚙️ Hệ thống đang tạo giọng đọc và trộn hình ảnh nền..."):
            try:
                # 1. Chuyển văn bản thành file âm thanh giọng Hoài My/Nam Minh
                async def generate_voice():
                    communicate = edge_tts.Communicate(edited_script, selected_voice)
                    await communicate.save("voice.mp3")
                asyncio.run(generate_voice())
                
                # 2. Kiểm tra file nền background.mp4 và xử lý trộn
                if os.path.exists("background.mp4"):
                    video_clip = VideoFileClip("background.mp4")
                    audio_clip = AudioFileClip("voice.mp3")
                    
                    # Giới hạn thời gian video khít với độ dài file nói mới tạo ra
                    final_video = video_clip.set_duration(audio_clip.duration).set_audio(audio_clip)
                    final_video.write_videofile("final_output.mp4", codec="libx264", audio_codec="aac", logger=None)
                    st.session_state['render_done'] = True
                else:
                    st.error("❌ Thiếu file 'background.mp4' trên hệ thống GitHub để làm video nền!")
            except Exception as e:
                st.error(f"Lỗi Render: {e}")

    # Hiển thị kết quả xem trực tuyến và nút tải xuống
    if 'render_done' in st.session_state:
        st.video("final_output.mp4")
        st.markdown("<p style='color:#198754; font-weight:bold;'>✓ Video của bạn đã dựng xong thành công!</p>", unsafe_allow_html=True)
        
        with open("final_output.mp4", "rb") as f:
            st.markdown("<div class='download-btn'>", unsafe_allow_html=True)
            st.download_button("📥 Tải Video Xuống (.MP4)", f, file_name="faceless_ai_success.mp4", mime="video/mp4")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color:#090b11; border: 2px dashed #283149; border-radius:10px; height:350px; display:flex; align-items:center; justify-content:center;">
            <p style="color:#57606a !important; text-align:center;">Video thành phẩm <br> sẽ hiển thị tại đây sau khi nhấn Render</p>
        </div>
        """, unsafe_allow_html=True)
