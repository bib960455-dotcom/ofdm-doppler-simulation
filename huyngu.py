import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# --- CẤU HÌNH GIAO DIỆN WEB ---
st.set_page_config(
    page_title="Mô phỏng Doppler & OFDM", 
    page_icon="📡", 
    layout="wide"
)

st.title("📡 MÔ PHỎNG VÀ ĐÁNH GIÁ ẢNH HƯỞNG CỦA DOPPLER ĐẾN HỆ THỐNG OFDM")
st.markdown("Đề tài: **Đánh giá ảnh hưởng của Doppler đến OFDM trong môi trường di động tốc độ cao**")
st.markdown("---")

# --- THANH ĐIỀU CHỈNH THÔNG SỐ (SIDEBAR) ---
st.sidebar.header("🎛️ Bảng điều khiển tham số")

max_speed = st.sidebar.slider("Tốc độ tối đa khảo sát (km/h)", min_value=100, max_value=1000, value=500, step=50)
v_kmh = np.arange(0, max_speed + 1, 25)
v_ms = v_kmh * 1000 / 3600

fc_options = st.sidebar.multiselect(
    "Chọn tần số sóng mang ($f_c$ GHz):",
    options=[1.0, 2.0, 3.5, 5.0],
    default=[2.0, 3.5]
)
fc_list = [fc * 1e9 for fc in fc_options]

scs_options = st.sidebar.multiselect(
    "Chọn khoảng cách sóng mang con (SCS kHz):",
    options=[15, 30, 60, 120],
    default=[15, 30, 60]
)
scs_list = [scs * 1e3 for scs in scs_options]

N = st.sidebar.selectbox("Kích thước FFT ($N$ subcarriers):", options=[64, 128, 256], index=1)
snr_db = st.sidebar.slider("Tỷ lệ SNR cố định (dB):", min_value=0, max_value=40, value=20)
num_symbols = st.sidebar.slider("Số ký tự OFDM mô phỏng:", min_value=10, max_value=50, value=20, step=10)

c = 3e8

# Hàm điều chế QPSK
def qpsk_mod(bits):
    mapping = {(0, 0): 1 + 1j, (0, 1): -1 + 1j, (1, 1): -1 - 1j, (1, 0): 1 - 1j}
    symbols = np.zeros(len(bits) // 2, dtype=complex)
    for i in range(0, len(bits), 2):
        symbols[i // 2] = mapping[(bits[i], bits[i + 1])] / np.sqrt(2)
    return symbols

def qpsk_demod(symbols):
    bits = []
    for sym in symbols:
        real_part = np.real(sym) >= 0
        imag_part = np.imag(sym) >= 0
        if real_part and imag_part: bits.extend([0, 0])
        elif not real_part and imag_part: bits.extend([0, 1])
        elif not real_part and not imag_part: bits.extend([1, 1])
        else: bits.extend([1, 0])
    return np.array(bits)

if not fc_list or not scs_list:
    st.warning("⚠️ Vui lòng chọn ít nhất một Tần số sóng mang và một loại SCS ở thanh bên trái để bắt đầu mô phỏng!")
else:
    my_bar = st.progress(0, text="⏳ Đang tiến hành mô phỏng hệ thống, vui lòng đợi...")

    BER_results = np.zeros((len(fc_list), len(scs_list), len(v_kmh)))
    ICI_results = np.zeros((len(fc_list), len(scs_list), len(v_kmh)))

    total_steps = len(fc_list) * len(scs_list)
    current_step = 0

    for f_idx, fc in enumerate(fc_list):
        for s_idx, scs in enumerate(scs_list):
            for v_idx, v in enumerate(v_ms):
                fd = (v * fc) / c
                error_count = 0
                total_bits = 0
                ici_power_accum = 0

                for _ in range(num_symbols):
                    tx_bits = np.random.randint(0, 2, N * 2)
                    tx_mod = qpsk_mod(tx_bits)
                    
                    tx_time = np.fft.ifft(tx_mod) * np.sqrt(N)
                    
                    t = np.arange(N) / (N * scs)
                    doppler_phase = np.exp(1j * 2 * np.pi * fd * t * np.cos(np.pi / 4))
                    rx_time_faded = tx_time * doppler_phase
                    
                    signal_power = np.mean(np.abs(rx_time_faded) ** 2)
                    noise_power = signal_power / (10 ** (snr_db / 10))
                    noise = np.sqrt(noise_power / 2) * (np.random.randn(N) + 1j * np.random.randn(N))
                    rx_time_noisy = rx_time_faded + noise
                    
                    rx_mod = np.fft.fft(rx_time_noisy) / np.sqrt(N)
                    
                    ici_power = np.mean(np.abs(rx_mod - tx_mod) ** 2)
                    ici_power_accum += ici_power
                    
                    rx_bits = qpsk_demod(rx_mod)
                    error_count += np.sum(tx_bits != rx_bits)
                    total_bits += len(tx_bits)
                
                BER_results[f_idx, s_idx, v_idx] = error_count / total_bits
                ICI_results[f_idx, s_idx, v_idx] = ici_power_accum / num_symbols

            current_step += 1
            my_bar.progress(int((current_step / total_steps) * 100), text=f"Đang xử lý cấu hình {current_step}/{total_steps}...")

    my_bar.empty()
    st.success("✅ Mô phỏng hoàn tất thành công!")

    # --- TỔNG HỢP DỮ LIỆU ĐÁNH GIÁ CHUNG ---
    eval_list = []
    for f_idx, fc in enumerate(fc_list):
        for s_idx, scs in enumerate(scs_list):
            for v_idx, v_val in enumerate(v_kmh):
                v_m = v_val * 1000 / 3600
                fd_val = (v_m * fc) / c if v_m > 0 else 1e-6
                tc_val = 0.423 / fd_val if fd_val > 0 else float('inf')
                
                ber_val = BER_results[f_idx, s_idx, v_idx]
                ici_val = ICI_results[f_idx, s_idx, v_idx]
                
                if ber_val < 0.01:
                    eval_status = "Tốt"
                elif ber_val < 0.1:
                    eval_status = "Trung bình"
                else:
                    eval_status = "Suy hao nặng"

                eval_list.append({
                    "Tần số fc (GHz)": fc / 1e9,
                    "SCS (kHz)": int(scs / 1e3),
                    "Tốc độ (km/h)": v_val,
                    "BER": ber_val,
                    "ICI Power": ici_val,
                    "Coherence Time (ms)": tc_val * 1000,
                    "Trạng thái": eval_status
                })
    df_eval = pd.DataFrame(eval_list)

    # --- DÒNG ĐÁNH GIÁ DỮ LIỆU TỔNG QUAN (EXECUTIVE SUMMARY NÂNG CẤP) ---
    st.markdown("### 📌 Đánh giá Dữ liệu Tổng quan & Phân tích Chuyên sâu Hệ thống")
    
    total_cases = len(df_eval)
    good_cases = len(df_eval[df_eval["Trạng thái"] == "Tốt"])
    med_cases = len(df_eval[df_eval["Trạng thái"] == "Trung bình"])
    bad_cases = len(df_eval[df_eval["Trạng thái"] == "Suy hao nặng"])
    avg_ber = df_eval["BER"].mean()
    max_ber = df_eval["BER"].max()
    max_ici = df_eval["ICI Power"].max()
    min_tc = df_eval["Coherence Time (ms)"].min()
    
    # Hiển thị thẻ chỉ số trực quan
    col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
    col_sum1.metric("📊 Tổng cấu hình khảo sát", f"{total_cases} trường hợp")
    col_sum2.metric("🟢 Tỷ lệ Đạt (Tốt)", f"{round((good_cases/total_cases)*100, 1)}%")
    col_sum3.metric("🔴 Tỷ lệ Suy hao nặng", f"{round((bad_cases/total_cases)*100, 1)}%")
    col_sum4.metric("⏱️ Thời gian đồng kết ($T_c$ min)", f"{round(min_tc, 2)} ms")

    # Hiển thị thêm chỉ số chi tiết phụ
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    sub_col1.metric("📉 Tỷ lệ lỗi bit trung bình (Avg BER)", f"{format(avg_ber, '.4f')}")
    sub_col2.metric("📈 Tỷ lệ lỗi bit lớn nhất (Max BER)", f"{format(max_ber, '.4f')}")
    sub_col3.metric("⚡ Công suất nhiễu ICI cực đại", f"{format(max_ici, '.4f')}")

    # Nhận định tóm tắt chi tiết bằng văn bản
    st.markdown("---")
    st.markdown("#### 🔍 Giải thích Cơ chế Vật lý & Đánh giá Tác động:")
    
    detailed_explanation = f"""
    1. **Mối quan hệ giữa Vận tốc và Dịch chuyển Doppler ($f_d$):** Khi phương tiện di chuyển ở tốc độ cao (đặc biệt từ $300$ km/h trở lên) trong các dải tần số cao ($3.5$ GHz - $5.0$ GHz), tần số dịch chuyển Doppler tăng mạnh. Điều này làm thay đổi pha tín hiệu liên tục trong một ký tự OFDM.
    2. **Nguyên nhân gây nhiễu liên sóng mang (ICI - Inter-Carrier Interference):** 
       - Trực giao giữa các sóng mang con phụ thuộc hoàn toàn vào khoảng cách sóng mang con (**SCS**). 
       - Khi sử dụng SCS nhỏ ($15$ kHz), độ dịch Doppler dễ vượt quá giới hạn an toàn (thường ngưỡng Doppler vượt quá $5\% - 10\%$ SCS sẽ gây ra ICI nghiêm trọng). 
       - Ngược lại, việc lựa chọn **SCS lớn hơn ($60$ kHz hoặc $120$ kHz)** giúp nới rộng khoảng cách giữa các sóng mang, từ đó triệt tiêu bớt ảnh hưởng của ICI.
    3. **Thời gian đồng kết kênh truyền ($T_c$):** Với thời gian đồng kết tối thiểu đo được là **{round(min_tc, 2)} ms**, kênh truyền thay đổi cực kỳ nhanh chóng so với độ dài ký tự OFDM truyền thống, dẫn đến hiện tượng suy giảm biên độ sâu và sàn lỗi (*BER floor*).
    """
    st.info(detailed_explanation)

    if bad_cases / total_cases > 0.5:
        summary_comment = "⚠️ **Kết luận tổng quan:** Hệ thống chịu ảnh hưởng cực kỳ nghiêm trọng bởi hiệu ứng Doppler ở dải vận tốc cao. **Khuyến nghị bắt buộc:** Phải tăng khoảng cách sóng mang con (SCS) lên mức cao hơn hoặc ứng dụng các thuật toán cân bằng kênh (Equalization) và ước lượng kênh chuyên sâu nhằm triệt tiêu nhiễu ICI."
    elif bad_cases / total_cases > 0.2:
        summary_comment = "⚡ **Kết luận tổng quan:** Hệ thống vận hành ổn định ở tốc độ thấp đến trung bình, tuy nhiên xuất hiện suy hao rõ rệt khi phương tiện đạt vận tốc lớn ở các băng tần cao. Cần cân nhắc cấu hình linh hoạt tùy theo kịch bản triển khai thực tế."
    else:
        summary_comment = "✅ **Kết luận tổng quan:** Cấu hình hệ thống hiện tại có khả năng chống chịu tốt với hiệu ứng Doppler trong dải thông số đã chọn, giữ cho tỷ lệ lỗi bit (BER) nằm trong ngưỡng kiểm soát."
    
    st.warning(summary_comment)
    st.markdown("---")

    # --- HIỂN THỊ CÁC TAB GIAO DIỆN ---
    tab1, tab2, tab3 = st.tabs([
        "📊 Biểu đồ Phân tích (BER & ICI)", 
        "📋 Dữ liệu Số liệu Thô", 
        "📑 Đánh giá Chuyên Sâu (Theo 5 Tiêu Chí)"
    ])

    with tab1:
        st.subheader("📈 Đồ thị trực quan hóa ảnh hưởng của hiệu ứng Doppler")
        for f_idx, fc in enumerate(fc_list):
            st.markdown(f"#### 🔹 Tần số sóng mang: $f_c$ = {fc / 1e9} GHz")
            
            fig, axes = plt.subplots(1, 2, figsize=(16, 5))
            
            for s_idx, scs in enumerate(scs_list):
                axes[0].plot(v_kmh, BER_results[f_idx, s_idx, :], marker='o', linewidth=2, label=f'SCS = {int(scs / 1e3)} kHz')
            axes[0].grid(True, linestyle='--', alpha=0.7)
            axes[0].set_xlabel('Vận tốc di chuyển (km/h)', fontweight='bold')
            axes[0].set_ylabel('Bit Error Rate (BER)', fontweight='bold')
            axes[0].set_title('Tỷ lệ lỗi bit (BER) theo vận tốc', fontsize=12, fontweight='bold')
            axes[0].set_yscale('log')
            axes[0].set_ylim(1e-4, 1.0)
            axes[0].legend()

            for s_idx, scs in enumerate(scs_list):
                axes[1].plot(v_kmh, ICI_results[f_idx, s_idx, :], marker='s', linewidth=2, linestyle='-.', label=f'SCS = {int(scs / 1e3)} kHz')
            axes[1].grid(True, linestyle='--', alpha=0.7)
            axes[1].set_xlabel('Vận tốc di chuyển (km/h)', fontweight='bold')
            axes[1].set_ylabel('Công suất nhiễu ICI', fontweight='bold')
            axes[1].set_title('Nhiễu liên sóng mang (ICI) theo vận tốc', fontsize=12, fontweight='bold')
            axes[1].legend()

            plt.tight_layout()
            st.pyplot(fig)
            st.markdown("---")

    with tab2:
        st.subheader("📁 Bảng dữ liệu mô phỏng thô")
        summary_data = []
        for f_idx, fc in enumerate(fc_list):
            for s_idx, scs in enumerate(scs_list):
                for v_idx, v_val in enumerate(v_kmh):
                    v_m = v_val * 1000 / 3600
                    fd_val = (v_m * fc) / c
                    summary_data.append({
                        "Tần số (GHz)": fc / 1e9,
                        "SCS (kHz)": scs / 1e3,
                        "Tốc độ (km/h)": v_val,
                        "Doppler Shift (Hz)": round(fd_val, 2),
                        "ICI Power": round(ICI_results[f_idx, s_idx, v_idx], 5),
                        "BER": round(BER_results[f_idx, s_idx, v_idx], 5)
                    })
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True)

    with tab3:
        st.subheader("📑 Bảng Đánh Giá Chuyên Sâu Theo 5 Tiêu Chí Kỹ Thuật")
        st.markdown("Bảng chi tiết phân tích từng tiêu chí kỹ thuật ứng với các cấu hình sóng mang, khoảng cách sóng mang con (SCS) và tốc độ di chuyển:")
        
        eval_display_list = []
        for row in eval_list:
            eval_display_list.append({
                "Tần số fc (GHz)": row["Tần số fc (GHz)"],
                "SCS (kHz)": row["SCS (kHz)"],
                "Tốc độ (km/h)": row["Tốc độ (km/h)"],
                "1. BER": round(row["BER"], 5),
                "2. ICI Power": round(row["ICI Power"], 5),
                "3. Coherence Time (ms)": round(row["Coherence Time (ms)"], 2),
                "4. Ảnh hưởng SCS": "Ít nhạy hơn (Kháng ICI tốt)" if row["SCS (kHz)"] >= 60 else "Nhạy cảm cao (Dễ mất trực giao)",
                "5. Ảnh hưởng fc": "Suy hao lớn (Dịch Doppler rộng)" if row["Tần số fc (GHz)"] >= 3.5 else "Ổn định hơn (D Doppler nhỏ)",
                "Trạng thái": "🟢 Tốt" if row["Trạng thái"]=="Tốt" else ("🟡 Trung bình" if row["Trạng thái"]=="Trung bình" else "🔴 Suy hao nặng")
            })
            
        df_eval_display = pd.DataFrame(eval_display_list)
        st.dataframe(df_eval_display, use_container_width=True)

        csv_eval = df_eval_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tải xuống Bảng Đánh Giá Chi Tiết (CSV)",
            data=csv_eval,
            file_name='bao_cao_danh_gia_doppler_ofdm.csv',
            mime='text/csv',
        )
