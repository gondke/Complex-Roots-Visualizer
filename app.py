import numpy as np
import plotly.graph_objects as go
import streamlit as st
import sympy as sp

# Streamlit Page Setup
st.set_page_config(
    page_title="Complex Roots & Powers Visualizer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚡ Advanced Complex Roots & Rational Powers Visualizer")
st.markdown(
    "Analyze complex numbers $Z$, compute $Z^{p/q}$ in exact textbook notation, "
    "and visualize all roots on the complex plane with principal root highlighting."
)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("1. Complex Number Input ($Z$)")
input_mode = st.sidebar.radio("Input Format", ["Polar (r, θ)", "Cartesian (a + bi)"])

if input_mode == "Cartesian (a + bi)":
    real_str = st.sidebar.text_input("Real Part (a)", value="1")
    imag_str = st.sidebar.text_input("Imaginary Part (b)", value="sqrt(3)")
    
    # Parse Symbolic Input via SymPy
    try:
        a_sym = sp.sympify(real_str)
        b_sym = sp.sympify(imag_str)
    except Exception:
        st.sidebar.error("Invalid expression. Use syntax like '1', 'sqrt(3)', '1/2'.")
        a_sym, b_sym = sp.Integer(1), sp.sqrt(3)

    Z_sym = a_sym + sp.I * b_sym
    z_mag_val = float(sp.Abs(Z_sym).evalf())
    z_angle_val = float(sp.arg(Z_sym).evalf())
else:
    z_mag_val = st.sidebar.slider("Radius / Magnitude ($r_Z$)", 0.1, 10.0, 2.0, 0.1)
    z_angle_deg = st.sidebar.slider("Angle ($\\theta_Z$ in deg)", -180, 180, 60, 5)
    z_angle_val = np.radians(z_angle_deg)
    
    a_sym = sp.nsimplify(z_mag_val * np.cos(z_angle_val), rational=True)
    b_sym = sp.nsimplify(z_mag_val * np.sin(z_angle_val), rational=True)
    Z_sym = a_sym + sp.I * b_sym

st.sidebar.markdown("---")
st.sidebar.header("2. Rational Power ($Z^{p/q}$)")
p_val = st.sidebar.number_input("Numerator (p)", value=1, step=1)
q_val = st.sidebar.number_input("Denominator / Roots (q)", value=3, min_value=1, step=1)

st.sidebar.markdown("---")
st.sidebar.header("3. Transformation Number ($W$)")
transform_op = st.sidebar.radio("Operation", ["None", "Multiply by W", "Divide by W"])

if transform_op != "None":
    w_real_str = st.sidebar.text_input("W Real Part", value="0")
    w_imag_str = st.sidebar.text_input("W Imaginary Part", value="1")
    try:
        W_sym = sp.sympify(w_real_str) + sp.I * sp.sympify(w_imag_str)
    except Exception:
        W_sym = sp.I
    w_mag_val = float(sp.Abs(W_sym).evalf())
    w_angle_val = float(sp.arg(W_sym).evalf())
else:
    W_sym = sp.Integer(1)
    w_mag_val, w_angle_val = 1.0, 0.0

st.sidebar.markdown("---")
st.sidebar.header("4. Display Settings")
show_labels = st.sidebar.checkbox("Show Point Labels", value=True)
show_lines = st.sidebar.checkbox("Show Radius Vectors", value=True)
dark_mode = st.sidebar.checkbox("Dark Contrast Mode", value=True)

# ---------------------------------------------------------
# Exact Mathematical Calculations
# ---------------------------------------------------------
r_Z = sp.Abs(Z_sym)
theta_Z = sp.arg(Z_sym)

# Effective magnitude and base angle for Z^(p/q)
root_r_val = (z_mag_val ** p_val) ** (1 / q_val)
base_angle = (p_val * z_angle_val) / q_val

# Generate all q roots
k_vals = np.arange(q_val)
root_angles = base_angle + (2 * np.pi * p_val * k_vals) / q_val

# Cartesian coordinates for plotting
orig_x = root_r_val * np.cos(root_angles)
orig_y = root_r_val * np.sin(root_angles)

# Apply W transformation if requested
if transform_op == "Multiply by W":
    trans_r_val = root_r_val * w_mag_val
    trans_angles = root_angles + w_angle_val
elif transform_op == "Divide by W":
    trans_r_val = root_r_val / w_mag_val
    trans_angles = root_angles - w_angle_val
else:
    trans_r_val = root_r_val
    trans_angles = root_angles

trans_x = trans_r_val * np.cos(trans_angles)
trans_y = trans_r_val * np.sin(trans_angles)

# ---------------------------------------------------------
# Display Expressions (Textbook Output)
# ---------------------------------------------------------
st.subheader("📚 Exact Form Representations of $Z$")
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("**Cartesian Form**")
    st.latex(rf"Z = {sp.latex(Z_sym)}")

with col_b:
    st.markdown("**Polar Form**")
    st.latex(rf"Z = {sp.latex(r_Z)} \left(\cos\left({sp.latex(theta_Z)}\right) + i\sin\left({sp.latex(theta_Z)}\right)\right)")

with col_c:
    st.markdown("**Exponential Form**")
    st.latex(rf"Z = {sp.latex(r_Z)} e^{{i \left({sp.latex(theta_Z)}\right)}}")

st.markdown("---")

# ---------------------------------------------------------
# Plotly Visualization
# ---------------------------------------------------------
fig = go.Figure()

bg_color = "#0E1117" if dark_mode else "#FFFFFF"
grid_color = "#333333" if dark_mode else "#E5E5E5"
text_color = "#FFFFFF" if dark_mode else "#000000"

max_radius = max(root_r_val, trans_r_val, z_mag_val) * 1.3
circle_theta = np.linspace(0, 2 * np.pi, 300)

# 1. Base Root Circle
fig.add_trace(
    go.Scatter(
        x=root_r_val * np.cos(circle_theta),
        y=root_r_val * np.sin(circle_theta),
        mode="lines",
        line=dict(color="#00E5FF", width=1.5, dash="dash"),
        name=f"Base Circle (r={root_r_val:.2f})",
        hoverinfo="skip",
    )
)

# 2. Transformed Circle
if transform_op != "None":
    fig.add_trace(
        go.Scatter(
            x=trans_r_val * np.cos(circle_theta),
            y=trans_r_val * np.sin(circle_theta),
            mode="lines",
            line=dict(color="#FF007F", width=1.5, dash="dash"),
            name=f"Transformed Circle (r={trans_r_val:.2f})",
            hoverinfo="skip",
        )
    )

# 3. Radius Vectors
if show_lines:
    for i in range(q_val):
        color = "#FFD700" if i == 0 else "#00E5FF"
        fig.add_trace(
            go.Scatter(
                x=[0, orig_x[i]],
                y=[0, orig_y[i]],
                mode="lines",
                line=dict(color=color, width=2 if i == 0 else 1),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        if transform_op != "None":
            fig.add_trace(
                go.Scatter(
                    x=[0, trans_x[i]],
                    y=[0, trans_y[i]],
                    mode="lines",
                    line=dict(color="#FF007F", width=1),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

# 4. Roots Points (Principal vs Secondary)
# Non-principal roots
if q_val > 1:
    labels_sec = [f"R{k+1}" for k in range(1, q_val)] if show_labels else None
    fig.add_trace(
        go.Scatter(
            x=orig_x[1:],
            y=orig_y[1:],
            mode="markers+text" if show_labels else "markers",
            text=labels_sec,
            textposition="top center",
            textfont=dict(color="#00E5FF", size=12),
            marker=dict(size=11, color="#00E5FF", symbol="circle"),
            name="Secondary Roots",
            hovertemplate="<b>Root %{text}</b><br>Re: %{x:.3f}<br>Im: %{y:.3f}<extra></extra>",
        )
    )

# Principal Root (k=0) - Highlighted
fig.add_trace(
    go.Scatter(
        x=[orig_x[0]],
        y=[orig_y[0]],
        mode="markers+text" if show_labels else "markers",
        text=["Principal Root (R1)"] if show_labels else None,
        textposition="top center",
        textfont=dict(color="#FFD700", size=13),
        marker=dict(size=16, color="#FFD700", symbol="star"),
        name="Principal Root (k=0)",
        hovertemplate="<b>Principal Root</b><br>Re: %{x:.3f}<br>Im: %{y:.3f}<extra></extra>",
    )
)

# Transformed Root Points
if transform_op != "None":
    trans_text = [f"R{k+1}'" for k in range(q_val)] if show_labels else None
    fig.add_trace(
        go.Scatter(
            x=trans_x,
            y=trans_y,
            mode="markers+text" if show_labels else "markers",
            text=trans_text,
            textposition="top center",
            textfont=dict(color="#FF007F", size=12),
            marker=dict(size=12, color="#FF007F", symbol="diamond"),
            name="Transformed Roots",
            hovertemplate="<b>Transformed Root %{text}</b><br>Re: %{x:.3f}<br>Im: %{y:.3f}<extra></extra>",
        )
    )

# Layout Setup
fig.update_layout(
    title=f"Complex Plane Visualization of $Z^{{{p_val}/{q_val}}}$",
    title_font=dict(color=text_color, size=18),
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
    xaxis=dict(
        title="Real Axis (Re)",
        zeroline=True,
        zerolinecolor="#777777",
        zerolinewidth=2,
        gridcolor=grid_color,
        range=[-max_radius, max_radius],
        tickfont=dict(color=text_color),
        title_font=dict(color=text_color),
    ),
    yaxis=dict(
        title="Imaginary Axis (Im)",
        zeroline=True,
        zerolinecolor="#777777",
        zerolinewidth=2,
        gridcolor=grid_color,
        range=[-max_radius, max_radius],
        scaleanchor="x",
        scaleratio=1,
        tickfont=dict(color=text_color),
        title_font=dict(color=text_color),
    ),
    legend=dict(font=dict(color=text_color), bgcolor=bg_color),
    width=700,
    height=700,
)

# Render View
col_plot, col_symbolic = st.columns([2, 1])

with col_plot:
    st.plotly_chart(fig, use_container_width=True)

with col_plot:
    st.info("⭐ **Gold Star**: Highlighted Principal Root ($k=0$).")

with col_symbolic:
    st.subheader("📐 Exact Roots ($Z^{p/q}$)")
    
    for k in range(q_val):
        # SymPy exact symbolic calculation per root
        rk_angle = theta_Z * p_val / q_val + sp.Rational(2 * k * p_val, q_val) * sp.pi
        exact_root = (r_Z ** sp.Rational(p_val, q_val)) * (sp.cos(rk_angle) + sp.I * sp.sin(rk_angle))
        exact_root_simplified = sp.simplify(exact_root)
        
        prefix = "⭐ **Principal Root (k=0):**" if k == 0 else f"**Root R_{{{k+1}}} (k={k}):**"
        st.markdown(prefix)
        st.latex(rf"R_{{{k+1}}} = {sp.latex(exact_root_simplified)}")
        
        if transform_op != "None":
            if transform_op == "Multiply by W":
                t_root = sp.simplify(exact_root_simplified * W_sym)
                st.latex(rf"R'_{{{k+1}}} = {sp.latex(t_root)}")
            elif transform_op == "Divide by W":
                t_root = sp.simplify(exact_root_simplified / W_sym)
                st.latex(rf"R'_{{{k+1}}} = {sp.latex(t_root)}")
