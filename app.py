from Assignment_1.DSP_Assignment_1 import addSignals, advance, delay, folding, multiplySignalByConst, subtractSignals
from Assignment_2.DSP_Assignment_2 import checkAliasing, analogSignal, discreteSignal
from Assignment_3.DSP_Assignment_3 import quantize_signal
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def parse_streamlit_file(uploaded_file):
    indices = []
    samples = []
    content = uploaded_file.getvalue().decode("utf-8").splitlines()
    for line in content[3:]:
        L = line.strip()
        if len(L.split()) == 2:
            V1, V2 = L.split()
            indices.append(int(V1))
            samples.append(float(V2))
    return indices, samples


def plot_signal(indices, samples, title, stem_color='rgba(31, 119, 180, 0.7)', marker_color="#50aff3"):
    fig = go.Figure()

    for x, y in zip(indices, samples):
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=y, line=dict(color=stem_color, width=2))

    fig.add_trace(go.Scatter(
        x=indices, y=samples, mode='markers', name=title,
        marker=dict(size=6, color=marker_color, line=dict(color=stem_color, width=1))
    ))
    
    is_small_data = len(indices) <= 30
    
    if is_small_data:
        for x in indices:
            fig.add_annotation(x=x, y=0, text=str(x), showarrow=False, yshift=-20, font=dict(color="black", size=14))
            
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(color="black", size=20)), 
        plot_bgcolor='white', paper_bgcolor='white',  
        xaxis=dict(
            title=dict(text="Time Index [n]", font=dict(color="black", size=18)), 
            showticklabels=not is_small_data, showline=not is_small_data, zeroline=False, gridcolor='lightgray'
        ), 
        yaxis=dict(
            title=dict(text="Amplitude", font=dict(color="black", size=18)), tickfont=dict(color="black", size=16), 
            showline=True, linewidth=2, linecolor='black', zeroline=True, zerolinewidth=2, zerolinecolor='black', gridcolor='lightgray'
        ),
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_analog_signal(t, samples, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t, y=samples, mode='lines', name=title, 
        line=dict(color="#5cebf0", width=3)
    ))
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(color="black", size=20)),
        plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(title=dict(text="Time (t)", font=dict(color="black", size=18)), tickfont=dict(color="black", size=18), showline=True, linewidth=2, linecolor='black', gridcolor='lightgray'),
        yaxis=dict(title=dict(text="Amplitude", font=dict(color="black", size=18)), tickfont=dict(color="black", size=18), showline=True, linewidth=2, linecolor='black', zeroline=True, zerolinewidth=2, zerolinecolor='black', gridcolor='lightgray'),
        height=400, margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)


def generate_output_file(indices, samples):
    content = "0\n0\n"
    content += f"{len(indices)}\n"
    for i, s in zip(indices, samples):
        content += f"{i} {s}\n"
    return content


def generate_quantization_output_file(encoded_vals, quantized_vals):
    """Outputs encoded stream and quantized reconstruction to match QuanTest1 spec."""
    content = "0\n0\n"
    content += f"{len(encoded_vals)}\n"
    for enc, q in zip(encoded_vals, quantized_vals):
        content += f"{enc} {q:.3f}\n"
    return content


st.set_page_config(
    page_title="DSP Tasks Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("📚 DSP Workstation Lab")
st.sidebar.divider()
st.sidebar.title("📝 Lab Tasks")

selected_task = st.sidebar.radio(
    "Choose Task:",
    [
        "📊 Task 1: Signal Processing", 
        "🚀 Task 2: Signal Sampling", 
        "⚛️ Task 3: Signal Quantization",
        "Task 4: "
    ],
    label_visibility="collapsed"
)

# ==============================================================================
# TASK 1: SIGNAL PROCESSING
# ==============================================================================
if "Task 1" in selected_task:
    st.title("Task 1: Signal Processing")
    st.caption("Perform fundamental discrete-time signal transformations on uploaded experimental time-series.")
    
    st.divider()
    st.markdown("## 📤 Signal Ingestion")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("#### **Upload Signal 1 (.txt)**")
            file1 = st.file_uploader("Format: index, value (.txt)", type=['txt'], key="file1")
            if file1 is not None:
                st.success(f"✅ {file1.name} - Uploaded & Parsed")
                
    with col2:
        with st.container(border=True):
            st.markdown("#### **Upload Signal 2 (.txt)**")
            file2 = st.file_uploader("Format: index, value (.txt)", type=['txt'], key="file2")
            if file2 is not None:
                st.success(f"✅ {file2.name} - Uploaded & Parsed")
                
    st.divider()
    st.markdown("## 💡 Operations")
    
    operation = st.radio(
        "Select Operation:",
        ["➕ Add", "➖ Subtract", "✖️ Multiply", "⏳ Delay", "⏩ Advance", "🔄 Folding"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    constant_value = None
    shift_value = None
    
    if operation == "✖️ Multiply":
        with st.container(border=True):
            st.markdown("#### ✖️ Multiplication Settings")
            constant_value = st.number_input("Enter the Constant Value:", value=1.0, step=0.5)
            
    elif operation in ["⏳ Delay", "⏩ Advance"]:
        with st.container(border=True):
            st.markdown("#### ⏱️ Shift Parameter Settings")
            shift_value = st.number_input(f"Enter Shift Amount (k) for {operation}:", value=1, step=1)

    st.divider()
    
    exec_col1, exec_col2 = st.columns([8, 2])
    with exec_col1:
        st.markdown(f"#### **Target Operation:** `{operation}`")
    with exec_col2:
        execute_btn = st.button("Display Result", type="primary", use_container_width=True)
        
    if execute_btn:
        if file1 is None:
            st.warning("⚠️ Please upload Signal 1 first!")
        else:
            ind1, samp1 = parse_streamlit_file(file1)
            res_ind, res_samp = [], []
            op_title = "Resulting Signal"
            
            if operation in ["➕ Add", "➖ Subtract"]:
                if file2 is None:
                    st.warning("⚠️ Please upload Signal 2 for this operation!")
                else:
                    ind2, samp2 = parse_streamlit_file(file2)
                    if operation == "➕ Add":
                        res_ind, res_samp = addSignals(ind1, samp1, ind2, samp2)
                        op_title = "Resulting Signal: y[n] = x1[n] + x2[n]"
                    else:
                        res_ind, res_samp = subtractSignals(ind1, samp1, ind2, samp2)
                        op_title = "Resulting Signal: y[n] = x1[n] - x2[n]"
                        
            elif operation == "✖️ Multiply":
                res_ind, res_samp = multiplySignalByConst(ind1, samp1, constant_value)
                op_title = f"Resulting Signal: y[n] = {constant_value} * x1[n]"
                
            elif operation == "⏳ Delay":
                res_ind, res_samp = delay(ind1, samp1, int(shift_value))
                op_title = f"Resulting Signal: y[n] = x1[n - {int(shift_value)}]"
                
            elif operation == "⏩ Advance":
                res_ind, res_samp = advance(ind1, samp1, int(shift_value))
                op_title = f"Resulting Signal: y[n] = x1[n + {int(shift_value)}]"
                
            elif operation == "🔄 Folding":
                res_ind, res_samp = folding(ind1, samp1)
                op_title = "Resulting Signal: y[n] = x1[-n]"

            if len(res_ind) > 0:
                with st.container(border=True):
                    st.success("✅ Computation Executed Successfully")
                    plot_signal(res_ind, res_samp, op_title)
                    
                    st.divider()
                    file_content = generate_output_file(res_ind, res_samp)
                    op_name = operation.split(' ')[1] 
                    
                    dl_col1, dl_col2 = st.columns([8, 2])
                    with dl_col2:
                        st.download_button(
                            label=f"📥 Download {op_name} Result (.txt)",
                            data=file_content,
                            file_name=f"{op_name}_result.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

# ==============================================================================
# TASK 2: SIGNAL SAMPLING
# ==============================================================================
elif "Task 2" in selected_task:
    st.title("🚀 Task 2: Signal Sampling")
    st.caption("Generate continuous and discrete sinusoidal signals based on Nyquist Theorem.")
    st.divider()

    st.markdown("## 🌊 Pick Wave Type")
    wave_type = st.radio("Wave Type", ["sin", "cos"], horizontal=True, label_visibility="collapsed")
    
    st.write("")

    st.markdown("## 📶 Signal Parameters")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        A = st.number_input("Amplitude (A)", value=None, step=0.5, placeholder="ex: 5.0")
    with col2:
        normal_F = st.number_input("Analog Frequency (F)", value=None, step=1.0, placeholder="ex: 10")
    with col3:
        sampling_F = st.number_input("Sampling Freq (Fs)", value=None, step=1.0, placeholder="ex: 50")
    with col4:
        phase_shift = st.number_input("Phase Shift (θ)", value=None, step=0.1, placeholder="ex: 0.0")

    st.divider()

    if st.button("Generate Signals", type="primary", use_container_width=True):
        if A is None or normal_F is None or sampling_F is None or phase_shift is None:
            st.warning("⚠️ Please fill in all the signal parameters before generating!")
        else:
            plot_col, info_col = st.columns([8, 2])
            
            with info_col:
                is_alias = checkAliasing(normal_F, sampling_F)
                if is_alias:
                    st.error("🚨 Aliasing\n\n(Fs < 2F)") 
                else:
                    st.success("✅ NO Aliasing\n\n(Fs >= 2F)")

            with plot_col:
                sign = "+" if phase_shift >= 0 else "-"
                t_vals, analog_y = analogSignal(wave_type, A, normal_F, phase_shift)
                
                st.latex(f"x(t) = {A} \\ {wave_type}(2\\pi ({normal_F}) t \\ {sign} \\ {abs(phase_shift)})")
                plot_analog_signal(t_vals, analog_y, "Analog Signal")
                
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                n_vals, discrete_y = discreteSignal(wave_type, A, sampling_F, normal_F, phase_shift)
                normalized_freq = normal_F / sampling_F
                
                st.latex(f"x[n] = {A} \\ {wave_type}(2\\pi ({normalized_freq:.2f}) n \\ {sign} \\ {abs(phase_shift)})")
                plot_signal(n_vals, discrete_y, "Discrete Signal")

# ==============================================================================
# TASK 3: SIGNAL QUANTIZATION
# ==============================================================================
elif "Task 3" in selected_task:
    st.title("⚛️ Task 3: Signal Quantization")
    st.caption("Scalar uniform quantization, discrete dynamic range partitioning, and PCM encoding.")
    st.divider()

    st.markdown("## 📤 Signal Input & Resolution Setup")
    col1, col2 = st.columns([5, 5])

    with col1:
        with st.container(border=True):
            st.markdown("#### **Upload Discrete Signal (.txt)**")
            q_file = st.file_uploader("Format: index, value (.txt)", type=['txt'], key="q_file")
            if q_file is not None:
                st.success(f"✅ {q_file.name} Loaded")

    with col2:
        with st.container(border=True):
            st.markdown("#### **Quantization Criteria**")
            choice_type = st.radio(
                "Specify Resolution by:",
                ["Bits", "Levels"],
                horizontal=True
            )
            
            if choice_type == "Bits":
                user_val = st.number_input("Number of Bits (b):", min_value=1, max_value=16, value=3, step=1)
                equiv_levels = 2 ** int(user_val)
                st.caption(f"ℹ️ Computed Resolution: **{equiv_levels} Levels**")
            else:
                user_val = st.number_input("Number of Quantization Levels (L):", min_value=2, max_value=256, value=4, step=1)
                import math
                equiv_bits = math.ceil(math.log2(int(user_val)))
                st.caption(f"ℹ️ Encoded Word Length: **{equiv_bits} Bits/Level**")

    st.divider()

    exec_col1, exec_col2 = st.columns([8, 2])
    with exec_col1:
        st.markdown(f"#### **Configuration:** Mode `{choice_type.lower()}` | Value `{int(user_val)}`")
    with exec_col2:
        quantize_btn = st.button("Run Quantization", type="primary", use_container_width=True)

    if quantize_btn:
        if q_file is None:
            st.warning("⚠️ Please upload a discrete signal file before running!")
        else:
            indices, samples = parse_streamlit_file(q_file)

            if len(samples) == 0:
                st.error("Uploaded signal contains no valid data.")
            else:
                backend_choice = 'bits' if choice_type == 'Bits' else 'levels'
                results = quantize_signal(samples, choice_type=backend_choice, user_value=int(user_val))

                quantized_samples = results['quantized_values']
                error_samples = results['error_values']
                encoded_values = results['encoded_values']
                interval_indices = results['interval_indices']
                avg_error = results['average_error']
                ranges = results['ranges']

                delta = ranges[0][1] - ranges[0][0]

                # Metric Cards
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Total Samples (N)", len(samples))
                with m2:
                    st.metric("Step Size (Δ)", f"{delta:.4f}")
                with m3:
                    st.metric("Levels (L)", len(ranges))
                with m4:
                    st.metric("Mean Squared Error", f"{avg_error:.5f}")

                st.divider()

                # Mathematical Formalism
                st.markdown("### 📐 Mathematical Representation")
                st.latex(r"\Delta = \frac{x_{\max} - x_{\min}}{L}, \quad e_q[n] = x_q[n] - x[n]")

                # Visualization: Original vs Quantized and Error
                tab_plots, tab_data = st.tabs(["📊 Waveform & Error Visualizer", "📋 Sample-Level Inspect Table"])

                with tab_plots:
                    st.markdown("#### **Discrete Stem Comparison**")
                    plot_signal(indices, quantized_samples, "Quantized Signal: x_q[n]", 
                                stem_color="rgba(44, 160, 44, 0.7)", marker_color="#2ca02c")
                    
                    st.markdown("#### **Quantization Error Signal**")
                    plot_signal(indices, error_samples, "Quantization Error: e_q[n] = x_q[n] - x[n]",
                                stem_color="rgba(214, 39, 40, 0.7)", marker_color="#d62728")

                with tab_data:
                    st.markdown("#### **Quantization Encodings & Reconstructions**")
                    df = pd.DataFrame({
                        "Time Index [n]": indices,
                        "Input x[n]": samples,
                        "Interval Index": interval_indices,
                        "Encoded Bits": encoded_values,
                        "Quantized x_q[n]": [round(v, 4) for v in quantized_samples],
                        "Error e_q[n]": [round(e, 4) for e in error_samples]
                    })
                    st.dataframe(df, use_container_width=True, height=350)

                st.divider()

                # Download Handler
                out_content = generate_quantization_output_file(encoded_values, quantized_samples)
                dl_col1, dl_col2 = st.columns([7, 3])
                with dl_col2:
                    st.download_button(
                        label="📥 Download Quantization Output (.txt)",
                        data=out_content,
                        file_name="quantization_output.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

else:
    st.title(selected_task)
    st.divider()
    st.info("This task is currently under development.")