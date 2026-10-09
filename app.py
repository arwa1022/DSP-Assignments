from Assignment_1.DSP_Assignment_1 import addSignals, advance, delay, folding, multiplySignalByConst, subtractSignals
from Assignment_2.DSP_Assignment_2 import checkAliasing, analogSignal, discreteSignal
import streamlit as st
import plotly.graph_objects as go


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

def plot_signal(indices, samples, title):
    fig = go.Figure()

    for x, y in zip(indices, samples):
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=y, line=dict(color='rgba(31, 119, 180, 0.7)', width=2))

    fig.add_trace(go.Scatter(x=indices, y=samples, mode='markers', name=title,
        marker=dict(size=6, color="#50aff3", line=dict(color='rgba(31, 119, 180, 1)', width=1))
    ))
    
    is_small_data = len(indices) <= 30
    
    if is_small_data:
        for x in indices:
            fig.add_annotation(x=x, y=0, text=str(x), showarrow=False, yshift=-20, font=dict(color="black", size=14))
            
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(color="black", size=20)), 
        plot_bgcolor='white', paper_bgcolor='white',  
        xaxis=dict( title=dict(text="Time Index [n]", font=dict(color="black", size=18)), 
            showticklabels=not is_small_data, showline=not is_small_data, zeroline=False, gridcolor='lightgray'), 
        yaxis=dict( title=dict(text="Amplitude", font=dict(color="black", size=18)), tickfont=dict(color="black", size=16), 
            showline=True, linewidth=2, linecolor='black', zeroline=True, zerolinewidth=2, zerolinecolor='black', gridcolor='lightgray'),
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
        "🚀 Task 2: Signal Generation", 
        "Task 3: ",
        "Task 4: "
    ],
    label_visibility="collapsed"
)

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
        [
            "➕ Add", 
            "➖ Subtract", 
            "✖️ Multiply", 
            "⏳ Delay", 
            "⏩ Advance", 
            "🔄 Folding"],
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

elif "Task 2" in selected_task:
    st.title("🚀 Task 2: Signal Generation")
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
else:
    st.title(selected_task)
    st.info("This task is currently under development.")