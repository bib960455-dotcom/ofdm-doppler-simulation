<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mô phỏng & Bảng Điều khiển OFDM (OFDM Simulator Dashboard)</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Font Awesome Icons CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Font: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Custom styling for sleek custom sliders */
        input[type=range] {
            accent-color: #2563eb;
        }
    </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen flex flex-col">

    <!-- Header Navigation -->
    <header class="bg-slate-800/80 backdrop-blur border-b border-slate-700/60 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="p-2 bg-blue-600 rounded-lg shadow-lg shadow-blue-500/30">
                    <i class="fa-solid fa-wave-square text-white text-xl"></i>
                </div>
                <div>
                    <h1 class="text-lg font-bold text-white tracking-wide">Mô Phỏng Tín Hiệu OFDM</h1>
                    <p class="text-xs text-slate-400">Trực quan hóa Dạng sóng & Tính toán Chỉ tiêu Hiệu năng 5G NR</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
                    Sẵn sàng Mô phỏng
                </span>
            </div>
        </div>
    </header>

    <!-- Main Dashboard Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- LEFT PANEL: CONTROL PARAMETERS -->
        <section class="lg:col-span-4 bg-slate-800 border border-slate-700/60 rounded-xl p-5 shadow-xl flex flex-col space-y-5">
            <div class="border-b border-slate-700/60 pb-3 flex justify-between items-center">
                <h2 class="text-base font-semibold text-slate-100 flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-blue-400"></i> Thông Số Đầu Vào
                </h2>
                <button id="resetBtn" class="text-xs text-slate-400 hover:text-blue-400 transition-colors">
<i class="fa-solid fa-rotate-left mr-1"></i> Mặc định
                </button>
            </div>

            <!-- Parameter 1: SCS -->
            <div class="space-y-1.5">
                <label for="scsSelect" class="text-xs font-medium text-slate-300 flex justify-between">
                    <span>Khoảng cách sóng mang (SCS)</span>
                    <span class="text-blue-400 font-mono" id="scsVal">15 kHz</span>
                </label>
                <select id="scsSelect" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500 transition-colors">
                    <option value="15" selected>15 kHz (SCS mặc định LTE / 5G FR1)</option>
                    <option value="30">30 kHz (SCS 5G NR FR1)</option>
                    <option value="60">60 kHz (SCS 5G NR High Speed)</option>
                </select>
            </div>

            <!-- Parameter 2: Resource Blocks (n_rb) -->
            <div class="space-y-1.5">
                <div class="flex justify-between text-xs font-medium text-slate-300">
                    <label for="nrbInput">Số Resource Blocks (n_rb)</label>
                    <span class="text-blue-400 font-mono" id="nrbVal">10 RB</span>
                </div>
                <input type="range" id="nrbInput" min="1" max="50" value="10" class="w-full h-2 bg-slate-900 rounded-lg appearance-none cursor-pointer">
                <div class="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>1 RB (12 SCs)</span>
                    <span>50 RB (600 SCs)</span>
                </div>
            </div>

            <!-- Parameter 3: Modulation Scheme -->
            <div class="space-y-1.5">
                <label for="modSelect" class="text-xs font-medium text-slate-300 flex justify-between">
                    <span>Bậc Điều Chế</span>
                    <span class="text-blue-400 font-mono" id="modVal">QPSK</span>
                </label>
                <select id="modSelect" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500 transition-colors">
                    <option value="QPSK" selected>QPSK (2 bits/symbol)</option>
                    <option value="16-QAM">16-QAM (4 bits/symbol)</option>
                </select>
            </div>

            <!-- Parameter 4: Cyclic Prefix (CP) -->
            <div class="space-y-1.5">
                <label for="cpSelect" class="text-xs font-medium text-slate-300 flex justify-between">
                    <span>Loại Tiền Tố Vòng (CP)</span>
                    <span class="text-blue-400 font-mono" id="cpVal">Normal (~7%)</span>
                </label>
<select id="cpSelect" class="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-blue-500 transition-colors">
                    <option value="Normal" selected>Normal CP (N_cp ~ 7% N_fft)</option>
                    <option value="Extended">Extended CP (N_cp = 25% N_fft)</option>
                </select>
            </div>

            <!-- Parameter 5: SNR (dB) -->
            <div class="space-y-1.5">
                <div class="flex justify-between text-xs font-medium text-slate-300">
                    <label for="snrInput">Tỷ số SNR Kênh Kênh Truyền (dB)</label>
                    <span class="text-blue-400 font-mono" id="snrVal">20 dB</span>
                </div>
                <input type="range" id="snrInput" min="0" max="40" value="20" step="1" class="w-full h-2 bg-slate-900 rounded-lg appearance-none cursor-pointer">
                <div class="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>0 dB (Nhiễu lớn)</span>
                    <span>40 dB (Kênh tốt)</span>
                </div>
            </div>

            <!-- Parameter 6: Samples to Plot -->
            <div class="space-y-1.5">
                <div class="flex justify-between text-xs font-medium text-slate-300">
                    <label for="samplesInput">Số Mẫu Hiển Thị Trên Đồ Thị</label>
                    <span class="text-blue-400 font-mono" id="samplesVal">40 mẫu</span>
                </div>
                <input type="range" id="samplesInput" min="10" max="200" value="40" step="5" class="w-full h-2 bg-slate-900 rounded-lg appearance-none cursor-pointer">
                <div class="flex justify-between text-[10px] text-slate-500 font-mono">
                    <span>10 mẫu (Zoom gần)</span>
                    <span>200 mẫu (Toàn cảnh)</span>
                </div>
            </div>

            <div class="pt-2 border-t border-slate-700/60">
                <div class="bg-blue-950/40 border border-blue-800/40 rounded-lg p-3 text-xs text-slate-300 flex items-start gap-2.5">
                    <i class="fa-solid fa-circle-info text-blue-400 mt-0.5"></i>
                    <span>Tất cả thông số được tính toán thời gian thực ngay khi bạn tương tác với các thanh trượt và menu.</span>
                </div>
            </div>
        </section>

        <!-- RIGHT PANEL: VISUALIZATION & METRICS -->
        <section class="lg:col-span-8 flex flex-col space-y-6">

            <!-- Summary Metric Cards -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
                <div class="bg-slate-800 border border-slate-700/60 rounded-xl p-3 shadow-md flex flex-col justify-between">
                    <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Số Sóng Mang ($N_{fft}$)</span>
<span id="metricNfft" class="text-xl font-bold text-blue-400 font-mono mt-1">120</span>
                    <span class="text-[10px] text-slate-500 mt-1">10 RB × 12 subcarriers</span>
                </div>

                <div class="bg-slate-800 border border-slate-700/60 rounded-xl p-3 shadow-md flex flex-col justify-between">
                    <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Băng Thông</span>
                    <span id="metricBw" class="text-xl font-bold text-emerald-400 font-mono mt-1">1.80 MHz</span>
                    <span class="text-[10px] text-slate-500 mt-1">$N_{fft} \times SCS$</span>
                </div>

                <div class="bg-slate-800 border border-slate-700/60 rounded-xl p-3 shadow-md flex flex-col justify-between">
                    <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Tỷ Lệ Lỗi Bit (BER)</span>
                    <span id="metricBer" class="text-xl font-bold text-amber-400 font-mono mt-1">0.00e+0</span>
                    <span class="text-[10px] text-slate-500 mt-1">Simulated AWGN</span>
                </div>

                <div class="bg-slate-800 border border-slate-700/60 rounded-xl p-3 shadow-md flex flex-col justify-between">
                    <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Thông Lượng Thô (R)</span>
                    <span id="metricThroughput" class="text-xl font-bold text-purple-400 font-mono mt-1">3.36 Mbps</span>
                    <span class="text-[10px] text-slate-500 mt-1">Truyền dẫn thực tế</span>
                </div>

                <div class="col-span-2 sm:col-span-1 bg-slate-800 border border-slate-700/60 rounded-xl p-3 shadow-md flex flex-col justify-between">
                    <span class="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Hiệu Suất Phổ</span>
                    <span id="metricSpecEff" class="text-xl font-bold text-cyan-400 font-mono mt-1">1.87 bit/s/Hz</span>
                    <span class="text-[10px] text-slate-500 mt-1">R / Bandwidth</span>
                </div>
            </div>

            <!-- Waveform Chart Box -->
            <div class="bg-slate-800 border border-slate-700/60 rounded-xl p-5 shadow-xl flex flex-col flex-1 min-h-[360px]">
                <div class="flex flex-col sm:flex-row justify-between sm:items-center border-b border-slate-700/60 pb-3 gap-2">
                    <div>
                        <h2 class="text-base font-semibold text-slate-100 flex items-center gap-2">
                            <i class="fa-solid fa-chart-line text-blue-400"></i> Dạng Sóng OFDM Miền Thời Gian
                        </h2>
                        <p class="text-xs text-slate-400">Thành phần Phần thực (Real) và Phần ảo (Imaginary) của tín hiệu sau IFFT + CP</p>
                    </div>
                    <div class="flex items-center space-x-3 text-xs font-medium">
<span class="flex items-center text-blue-400">
                            <span class="w-3 h-3 rounded-full bg-blue-500 border border-white inline-block mr-1.5"></span> Phần thực (Real)
                        </span>
                        <span class="flex items-center text-red-400">
                            <span class="w-3 h-3 rounded-full bg-red-500 border border-white inline-block mr-1.5"></span> Phần ảo (Imag)
                        </span>
                    </div>
                </div>

                <!-- Canvas Container -->
                <div class="relative flex-1 w-full mt-4 min-h-[280px]">
                    <canvas id="ofdmChart"></canvas>
                </div>
            </div>

            <!-- Detailed Breakdown Table -->
            <div class="bg-slate-800 border border-slate-700/60 rounded-xl p-5 shadow-xl">
                <h3 class="text-sm font-semibold text-slate-200 mb-3 flex items-center gap-2">
                    <i class="fa-solid fa-list-check text-blue-400"></i> Chi Tiết Thông Số Kỹ Thuật Hệ Thống
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300">
                        <thead class="bg-slate-900/60 uppercase text-[10px] text-slate-400 font-semibold border-b border-slate-700">
                            <tr>
                                <th class="px-3 py-2">Thông Số</th>
                                <th class="px-3 py-2">Ký Hiệu / Công Thức</th>
                                <th class="px-3 py-2 font-mono">Giá Trị Tính Toán</th>
                                <th class="px-3 py-2">Đơn Vị</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-700/50 font-mono">
                            <tr class="hover:bg-slate-700/30">
                                <td class="px-3 py-2 font-sans font-medium text-slate-200">Thời gian Symbol hữu ích</td>
                                <td class="px-3 py-2 text-slate-400">Tu = 1000 / SCS</td>
                                <td id="tableTu" class="px-3 py-2 text-blue-400">66.67</td>
                                <td class="px-3 py-2 font-sans text-slate-400">µs</td>
                            </tr>
                            <tr class="hover:bg-slate-700/30">
                                <td class="px-3 py-2 font-sans font-medium text-slate-200">Độ dài Tiền tố vòng (CP)</td>
                                <td id="tableCpFormula" class="px-3 py-2 text-slate-400">N_cp (7% N_fft)</td>
                                <td id="tableNcp" class="px-3 py-2 text-blue-400">8 mẫu (4.67 µs)</td>
                                <td class="px-3 py-2 font-sans text-slate-400">mẫu / µs</td>
                            </tr>
                            <tr class="hover:bg-slate-700/30">
<td class="px-3 py-2 font-sans font-medium text-slate-200">Tổng thời gian 1 Symbol OFDM</td>
                                <td class="px-3 py-2 text-slate-400">T_total = Tu + Tcp</td>
                                <td id="tableTtotal" class="px-3 py-2 text-blue-400">71.33</td>
                                <td class="px-3 py-2 font-sans text-slate-400">µs</td>
                            </tr>
                            <tr class="hover:bg-slate-700/30">
                                <td class="px-3 py-2 font-sans font-medium text-slate-200">Số bit trên mỗi ký hiệu điều chế</td>
                                <td class="px-3 py-2 text-slate-400">μ (QPSK=2, 16QAM=4)</td>
                                <td id="tableMu" class="px-3 py-2 text-blue-400">2</td>
                                <td class="px-3 py-2 font-sans text-slate-400">bits/symbol</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </section>
    </main>

    <!-- Footer -->
    <footer class="bg-slate-950 border-t border-slate-800 py-3 text-center text-xs text-slate-500">
        <p>© 2026 OFDM Simulator Dashboard • Thiết kế trực quan cho Học tập và Báo cáo Đồ án</p>
    </footer>

    <!-- LOGIC SIMULATION & CHART rendering script -->
    <script>
        // DOM Elements
        const scsSelect = document.getElementById('scsSelect');
        const nrbInput = document.getElementById('nrbInput');
        const modSelect = document.getElementById('modSelect');
        const cpSelect = document.getElementById('cpSelect');
        const snrInput = document.getElementById('snrInput');
        const samplesInput = document.getElementById('samplesInput');
        const resetBtn = document.getElementById('resetBtn');

        // Value Displays
        const scsVal = document.getElementById('scsVal');
        const nrbVal = document.getElementById('nrbVal');
        const modVal = document.getElementById('modVal');
        const cpVal = document.getElementById('cpVal');
        const snrVal = document.getElementById('snrVal');
        const samplesVal = document.getElementById('samplesVal');

        // Metric Displays
        const metricNfft = document.getElementById('metricNfft');
        const metricBw = document.getElementById('metricBw');
        const metricBer = document.getElementById('metricBer');
        const metricThroughput = document.getElementById('metricThroughput');
        const metricSpecEff = document.getElementById('metricSpecEff');

        // Table Displays
        const tableTu = document.getElementById('tableTu');
        const tableCpFormula = document.getElementById('tableCpFormula');
        const tableNcp = document.getElementById('tableNcp');
        const tableTtotal = document.getElementById('tableTtotal');
        const tableMu = document.getElementById('tableMu');

        // Chart setup
        let ofdmChart = null;
function initChart() {
            const ctx = document.getElementById('ofdmChart').getContext('2d');
            ofdmChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        {
                            label: 'Phần thực (Real)',
                            data: [],
                            borderColor: '#3b82f6', // blue-500
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            borderWidth: 1.8,
                            pointStyle: 'circle',
                            pointRadius: 3,
                            pointHoverRadius: 5,
                            pointBackgroundColor: '#3b82f6',
                            tension: 0.2
                        },
                        {
                            label: 'Phần ảo (Imaginary)',
                            data: [],
                            borderColor: '#ef4444', // red-500
                            backgroundColor: 'rgba(239, 68, 68, 0.1)',
                            borderWidth: 1.8,
                            borderDash: [5, 4],
                            pointStyle: 'crossRot',
                            pointRadius: 4,
                            pointHoverRadius: 6,
                            pointBackgroundColor: '#ef4444',
                            tension: 0.2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 300
                    },
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Chỉ số mẫu (Sample Index)',
                                color: '#94a3b8',
                                font: { size: 11, family: 'Inter' }
                            },
                            grid: {
                                color: 'rgba(51, 65, 85, 0.4)'
                            },
                            ticks: {
                                color: '#94a3b8',
                                font: { size: 10 }
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Biên độ (Amplitude)',
                                color: '#94a3b8',
                                font: { size: 11, family: 'Inter' }
                            },
                            grid: {
                                color: 'rgba(51, 65, 85, 0.4)'
                            },
ticks: {
                                color: '#94a3b8',
                                font: { size: 10 }
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: '#0f172a',
                            titleColor: '#f8fafc',
                            bodyColor: '#cbd5e1',
                            borderColor: '#334155',
                            borderWidth: 1,
                            padding: 10,
                            displayColors: true
                        }
                    }
                }
            });
        }

        // QPSK & 16-QAM constellation mapping
        function mapSymbol(b1, b2, mod) {
            if (mod === 'QPSK') {
                const re = b1 === 0 ? -1 : 1;
                const im = b2 === 0 ? -1 : 1;
                return { re: re / Math.SQRT2, im: im / Math.SQRT2 };
            } else {
                // 16-QAM dummy mapping
                const levels = [-3, -1, 1, 3];
                const re = levels[b1 % 4];
                const im = levels[b2 % 4];
                return { re: re / Math.sqrt(10), im: im / Math.sqrt(10) };
            }
        }

        // Fast Fourier Transform (Cooley-Tukey IDFT simplified for OFDM generation)
        function computeIFFT(realIn, imagIn) {
            const N = realIn.length;
            const realOut = new Float64Array(N);
            const imagOut = new Float64Array(N);

            for (let k = 0; k < N; k++) {
                let sumRe = 0;
                let sumIm = 0;
                for (let n = 0; n < N; n++) {
                    const angle = (2 * Math.PI * k * n) / N;
                    const cosA = Math.cos(angle);
                    const sinA = Math.sin(angle);
                    sumRe += realIn[n] * cosA - imagIn[n] * sinA;
                    sumIm += realIn[n] * sinA + imagIn[n] * cosA;
                }
                realOut[k] = sumRe / Math.sqrt(N);
                imagOut[k] = sumIm / Math.sqrt(N);
            }
            return { real: realOut, imag: imagOut };
        }

        // Main Simulation Engine
        function runSimulation() {
            // Get Parameters
            const scs = parseFloat(scsSelect.value); // kHz
            const n_rb = parseInt(nrbInput.value);
            const modulation = modSelect.value;
            const cpType = cpSelect.value;
            const snr_db = parseFloat(snrInput.value);
            const numPlotSamples = parseInt(samplesInput.value);

            // Update Text Displays
            scsVal.innerText = `${scs} kHz`;
            nrbVal.innerText = `${n_rb} RB`;
            modVal.innerText = modulation;
            cpVal.innerText = cpType === 'Normal' ? 'Normal (~7%)' : 'Extended (25%)';
snrVal.innerText = `${snr_db} dB`;
            samplesVal.innerText = `${numPlotSamples} mẫu`;

            // Calculated Parameters
            const mu = modulation === 'QPSK' ? 2 : 4;
            const n_fft = n_rb * 12; // Total subcarriers
            const t_u = 1000.0 / scs; // microseconds

            let cpRatio = cpType === 'Normal' ? 0.07 : 0.25;
            let n_cp = Math.max(1, Math.round(n_fft * cpRatio));
            let t_cp = t_u * cpRatio;

            // Generate Symbol Data
            const symReal = new Float64Array(n_fft);
            const symImag = new Float64Array(n_fft);

            // Pseudorandom symbol constellation generation
            let seed = 42;
            function pseudoRandom() {
                seed = (seed * 9301 + 49297) % 233280;
                return seed / 233280;
            }

            for (let i = 0; i < n_fft; i++) {
                const b1 = pseudoRandom() > 0.5 ? 1 : 0;
                const b2 = pseudoRandom() > 0.5 ? 1 : 0;
                const sym = mapSymbol(b1, b2, modulation);
                symReal[i] = sym.re;
                symImag[i] = sym.im;
            }

            // Perform IFFT to transform to Time Domain
            const timeSignal = computeIFFT(symReal, symImag);

            // Add Cyclic Prefix (CP)
            const totalSamples = n_fft + n_cp;
            const ofdmReal = new Float64Array(totalSamples);
            const ofdmImag = new Float64Array(totalSamples);

            // Copy CP
            for (let i = 0; i < n_cp; i++) {
                ofdmReal[i] = timeSignal.real[n_fft - n_cp + i];
                ofdmImag[i] = timeSignal.imag[n_fft - n_cp + i];
            }
            // Copy main signal
            for (let i = 0; i < n_fft; i++) {
                ofdmReal[n_cp + i] = timeSignal.real[i];
                ofdmImag[n_cp + i] = timeSignal.imag[i];
            }

            // Repeat pattern to satisfy plot samples if necessary
            const labels = [];
            const plotReal = [];
            const plotImag = [];

            for (let i = 0; i < numPlotSamples; i++) {
                labels.push(i);
                const sampleIdx = i % totalSamples;
                plotReal.push(ofdmReal[sampleIdx]);
                plotImag.push(ofdmImag[sampleIdx]);
            }

            // Update Chart Data
            if (ofdmChart) {
                ofdmChart.data.labels = labels;
                ofdmChart.data.datasets[0].data = plotReal;
                ofdmChart.data.datasets[1].data = plotImag;
                ofdmChart.update();
            }

            // Calculate Metrics
            const bandwidth_mhz = (n_fft * scs) / 1000.0;
            const t_total = t_u + t_cp; // us
            const r_raw_mbps = (n_fft * mu) / (t_total * 1e-3); // Mbps
            const spec_efficiency = r_raw_mbps / bandwidth_mhz;

            // Theoretical BER Approximation under AWGN
            const snr_lin = Math.pow(10, snr_db / 10.0);
let ber = 0.0;
            if (modulation === 'QPSK') {
                // QPSK BER = Q(sqrt(SNR))
                const arg = Math.sqrt(snr_lin);
                ber = 0.5 * erfc(arg / Math.SQRT2);
            } else {
                // 16-QAM BER approximation = 0.75 * Q(sqrt(0.2 * SNR))
                const arg = Math.sqrt(0.2 * snr_lin);
                ber = 0.75 * 0.5 * erfc(arg / Math.SQRT2);
            }

            // Update Metric Cards
            metricNfft.innerText = n_fft;
            metricBw.innerText = `${bandwidth_mhz.toFixed(2)} MHz`;
            metricBer.innerText = ber === 0 ? "0.00e+0" : ber.toExponential(2);
            metricThroughput.innerText = `${r_raw_mbps.toFixed(2)} Mbps`;
            metricSpecEff.innerText = `${spec_efficiency.toFixed(2)} bit/s/Hz`;

            // Update Breakdown Table
            tableTu.innerText = t_u.toFixed(2);
            tableCpFormula.innerText = cpType === 'Normal' ? `N_cp (7% N_fft)` : `N_cp (25% N_fft)`;
            tableNcp.innerText = `${n_cp} mẫu (${t_cp.toFixed(2)} µs)`;
            tableTtotal.innerText = t_total.toFixed(2);
            tableMu.innerText = `${mu} (${modulation})`;
        }

        // Complementary Error Function (erfc) approximation for BER calculation
        function erfc(x) {
            if (x < 0) return 2 - erfc(-x);
            const a1 =  0.254829592;
            const a2 = -0.284496736;
            const a3 =  1.421413741;
            const a4 = -1.453152027;
            const a5 =  1.061405429;
            const p  =  0.3275911;

            const t = 1.0 / (1.0 + p * x);
            const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
            return 1.0 - y;
        }

        // Reset inputs to default
        function resetDefaults() {
            scsSelect.value = "15";
            nrbInput.value = "10";
            modSelect.value = "QPSK";
            cpSelect.value = "Normal";
            snrInput.value = "20";
            samplesInput.value = "40";
            runSimulation();
        }

        // Event Listeners
        [scsSelect, nrbInput, modSelect, cpSelect, snrInput, samplesInput].forEach(elem => {
            elem.addEventListener('input', runSimulation);
            elem.addEventListener('change', runSimulation);
        });

        resetBtn.addEventListener('click', resetDefaults);

        // Initialize App on Load
        window.addEventListener('DOMContentLoaded', () => {
            initChart();
            runSimulation();
        });
    </script>
</body>
</html>
