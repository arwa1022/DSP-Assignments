from Assignment_1.DSP_Assignment_1 import addSignals, advance, delay, folding, multiplySignalByConst, subtractSignals
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
    fig.add_trace(go.Scatter(
        x=indices, y=samples,
        mode='markers+lines',
        name=title,
        marker=dict(size=15, color='#1f77b4'),
        line=dict(color='rgba(31, 119, 180, 0.5)', width=3.5)
    ))
    fig.update_layout(
        title=f"<b>{title}</b>",
        xaxis_title="Time Index [n]",
        yaxis_title="Amplitude",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40)
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
        "Task 2: ", 
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
                st.success(f"✔️ {file1.name} - Uploaded & Parsed")
                
    with col2:
        with st.container(border=True):
            st.markdown("#### **Upload Signal 2 (.txt)**")

            file2 = st.file_uploader("Format: index, value (.txt)", type=['txt'], key="file2")
            if file2 is not None:
                st.success(f"✔️ {file2.name} - Uploaded & Parsed")
                
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
                    st.success("✔️ Computation Executed Successfully")
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
else:
    st.title(selected_task)
    st.info("This task is currently under development.")