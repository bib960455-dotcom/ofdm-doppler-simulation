import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mô phỏng Doppler & OFDM", layout="wide")
st.title("📡 MÔ PHỎNG VÀ ĐÁNH GIÁ ẢNH HƯỞNG CỦA DOPPLER ĐẾN HỆ THỐNG OFDM")
st.markdown("Đề tài: **Đánh giá ảnh hưởng của Doppler đến OFDM trong môi trường di động tốc độ cao**")

st.sidebar.header("🎛️ Bảng điều khiển tham số")
max_speed = st.sidebar.slider("Tốc độ tối đa khảo sát (km/h)", min_value=100, max_value=1000, value=500, step=50)
v_kmh = np.arange(0, max_speed + 1, 25)
v_ms = v_kmh * 1000 / 3600

fc_options = st.sidebar.multiselect("Chọn tần số sóng mang ($f_c$ GHz):", options=[1.0, 2.0, 3.5, 5.0], default=[2.0, 3.5])
fc_list = [fc * 1e9 for fc in fc_options]

scs_options = st.sidebar.multiselect("Chọn khoảng cách sóng mang con (SCS kHz):", options=[15, 30, 60, 120], default=[15, 30, 60])
scs_list = [scs * 1e3 for scs in scs_options]

N = st.sidebar.selectbox("Kích thước FFT ($N$ subcarriers):", options=[64, 128, 256], index=1)
snr_db = st.sidebar.slider("Tỷ lệ SNR cố định (dB):", min_value=0, max_value=40, value=20)
num_symbols = st.sidebar.slider("Số ký tự OFDM mô phỏng:", min_value=10, max_value=100, value=20, step=10)

def qpsk_mod(bits):
    mapping = {(0, 0): 1 + 1j, (0, 1): -1 + 1j, (1, 1): -1 - 1j, (1, 0): 1 - 1j}
    symbols = np.zeros(len(bits) // 2, dtype=complex)
    for i in range(0, len(bits), 2):
        symbols[i//2] = mapping[(bits[i], bits[i+1])] / np.sqrt(2)
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

c = 3e8

if not fc_list or not scs_list:
    st.warning("⚠️ Vui lòng chọn ít nhất một Tần số sóng mang và một loại SCS ở thanh bên trái!")
else:
    with st.spinner("⏳ Đang tính toán mô phỏng hệ thống OFDM... Vui lòng đợi trong giây lát!"):
        BER_results = np.zeros((len(fc_list), len(scs_list), len(v_kmh)))
        ICI_results = np.zeros((len(fc_list), len(scs_list), len(v_kmh)))

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
                        
                        signal_power = np.mean(np.abs(rx_time_faded)**2)
                        noise_power = signal_power / (10**(snr_db / 10))
                        noise = np.sqrt(noise_power / 2) * (np.random.randn(N) + 1j * np.random.randn(N))
                        rx_time_noisy = rx_time_faded + noise
                        
                        rx_mod = np.fft.fft(rx_time_noisy) / np.sqrt(N)
                        ici_power = np.mean(np.abs(rx_mod - tx_mod)**2)
                        ici_power_accum += ici_power
                        
                        rx_bits = qpsk_demod(rx_mod)
                        error_count += np.sum(tx_bits != rx_bits)
                        total_bits += len(tx_bits)
                    
                    BER_results[f_idx, s_idx, v_idx] = error_count / total_bits
                    ICI_results[f_idx, s_idx, v_idx] = ici_power_accum / num_symbols

    st.success("✅ Mô phỏng hoàn tất!")
    tab1, tab2 = st.tabs(["📊 Biểu đồ BER & ICI", "📋 Bảng số liệu chi tiết"])

    with tab1:
        for f_idx, fc in enumerate(fc_list):
            st.subheader(f"📌 Đánh giá tại Tần số sóng mang f_c = {fc/1e9} GHz")
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            for s_idx, scs in enumerate(scs_list):
                axes[0].plot(v_kmh, BER_results[f_idx, s_idx, :], marker='o', linewidth=2, label=f'SCS = {int(scs/1e3)} kHz')
            axes[0].grid(True, linestyle='--', alpha=0.7)
            axes[0].set_xlabel('Vận tốc (km/h)', fontweight='bold')
            axes[0].set_ylabel('Bit Error Rate (BER)', fontweight='bold')
            axes[0].set_title('Tỷ lệ lỗi bit (BER) theo tốc độ')
            axes[0].set_yscale('log')
            axes[0].set_ylim(1e-4, 1.0)
            axes[0].legend()

            for s_idx, scs in enumerate(scs_list):
                axes[1].plot(v_kmh, ICI_results[f_idx, s_idx, :], marker='s', linewidth=2, linestyle='-.', label=f'SCS = {int(scs/1e3)} kHz')
            axes[1].grid(True, linestyle='--', alpha=0.7)
            axes[1].set_xlabel('Vận tốc (km/h)', fontweight='bold')
            axes[1].set_ylabel('Công suất nhiễu ICI', fontweight='bold')
            axes[1].set_title('Nhiễu liên sóng mang (ICI) theo tốc độ')
            axes[1].legend()

            plt.tight_layout()
            st.pyplot(fig)

    with tab2:
        st.subheader("📁 Dữ liệu số liệu mô phỏng thô")
        summary_data = []
        for f_idx, fc in enumerate(fc_list):
            for s_idx, scs in enumerate(scs_list):
                for v_idx, v_val in enumerate(v_kmh):
                    v_m = v_val * 1000 / 3600
                    fd_val = (v_m * fc) / c
                    summary_data.append({
                        "Tần số (GHz)": fc/1e9,
                        "SCS (kHz)": scs/1e3,
                        "Tốc độ (km/h)": v_val,
                        "Doppler Shift (Hz)": round(fd_val, 2),
                        "ICI Power": round(ICI_results[f_idx, s_idx, v_idx], 5),
                        "BER": round(BER_results[f_idx, s_idx, v_idx], 5)
                    })
        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True)
