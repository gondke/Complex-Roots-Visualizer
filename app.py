import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Streamlit Page Setup (Fixed keyword argument from page_layout to layout)
st.set_page_config(
    page_title="Complex Roots Visualizer",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("⚡ Complex Roots & Dynamic Transformation Visualizer")
st.markdown(
    "Explore the $n$-th roots of a complex number $Z = r e^{i\\theta}$ on the complex plane "
    "and dynamically apply multiplication or division by a secondary complex number $W$."
)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("1. Target Complex Number ($Z$)")
z_mag = st.sidebar.slider("Radius / Magnitude ($r_Z$)", 0.1, 10.0, 1.0, 0.1)
z_angle_deg = st.sidebar.slider("Angle / Argument ($\\theta_Z$ in deg)", 0, 360, 0, 5)
n_roots = st.sidebar.slider("Number of Roots ($n$)", 1, 12, 5)

st.sidebar.markdown("---")
st.sidebar.header("2. Transformation Number ($W$)")
transform_op = st.sidebar.radio("Operation", ["None", "Multiply by W", "Divide by W"])

if transform_op != "None":
    w_mag = st.sidebar.slider("W Magnitude ($r_W$)", 0.1, 5.0, 1.5, 0.1)
    w_angle_deg = st.sidebar.slider("W Angle ($\\theta_W$ in deg)", -180, 180, 45, 5)
else:
    w_mag = 1.0
    w_angle_deg = 0

st.sidebar.markdown("---")
st.sidebar.header("3. Display Settings")
show_labels = st.sidebar.checkbox("Show Point Labels", value=True)
show_lines = st.sidebar.checkbox("Show Radius Vectors", value=True)
dark_mode = st.sidebar.checkbox("Dark Contrast Mode", value=True)

# ---------------------------------------------------------
# Mathematical Calculations
# ---------------------------------------------------------
z_theta = np.radians(z_angle_deg)
w_theta = np.radians(w_angle_deg)

# Base n-th roots of Z
root_r = z_mag ** (1 / n_roots)
k_values = np.arange(n_roots)
root_angles = (z_theta + 2 * np.pi * k_values) / n_roots

# Convert roots to rectangular coordinates
orig_x = root_r * np.cos(root_angles)
orig_y = root_r * np.sin(root_angles)

# Transformation logic
if transform_op == "Multiply by W":
    trans_r = root_r * w_mag
    trans_angles = root_angles + w_theta
elif transform_op == "Divide by W":
    trans_r = root_r / w_mag
    trans_angles = root_angles - w_theta
else:
    trans_r = root_r
    trans_angles = root_angles

trans_x = trans_r * np.cos(trans_angles)
trans_y = trans_r * np.sin(trans_angles)

# Compute circle bounds
max_radius = max(root_r, trans_r, z_mag) * 1.3
circle_theta = np.linspace(0, 2 * np.pi, 200)

# ---------------------------------------------------------
# Plotly Visualization
# ---------------------------------------------------------
fig = go.Figure()

# Background & Grid styling based on theme
bg_color = "#0E1117" if dark_mode else "#FFFFFF"
grid_color = "#333333" if dark_mode else "#E5E5E5"
text_color = "#FFFFFF" if dark_mode else "#000000"

# 1. Base Root Circle
fig.add_trace(
    go.Scatter(
        x=root_r * np.cos(circle_theta),
        y=root_r * np.sin(circle_theta),
        mode="lines",
        line=dict(color="#00E5FF", width=1.5, dash="dash"),
        name=f"Base Circle (r={root_r:.2f})",
        hoverinfo="skip",
    )
)

# 2. Transformed Circle (if applicable)
if transform_op != "None":
    fig.add_trace(
        go.Scatter(
            x=trans_r * np.cos(circle_theta),
            y=trans_r * np.sin(circle_theta),
            mode="lines",
            line=dict(color="#FF007F", width=1.5, dash="dash"),
            name=f"Transformed Circle (r={trans_r:.2f})",
            hoverinfo="skip",
        )
    )

# 3. Radius Vectors
if show_lines:
    for i in range(n_roots):
        # Base lines
        fig.add_trace(
            go.Scatter(
                x=[0, orig_x[i]],
                y=[0, orig_y[i]],
                mode="lines",
                line=dict(color="#00E5FF", width=1),
                showlegend=False,
                hoverinfo="skip",
            )
        )
        # Transformed lines
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

# 4. Base Root Points
base_text = [f"R{k+1}" for k in range(n_roots)] if show_labels else None
fig.add_trace(
    go.Scatter(
        x=orig_x,
        y=orig_y,
        mode="markers+text" if show_labels else "markers",
        text=base_text,
        textposition="top center",
        textfont=dict(color="#00E5FF", size=12),
        marker=dict(size=12, color="#00E5FF", symbol="circle"),
        name="Original Roots",
        hovertemplate="<b>Original Root %{text}</b><br>Re: %{x:.3f}<br>Im: %{y:.3f}<extra></extra>",
    )
)

# 5. Transformed Root Points
if transform_op != "None":
    trans_text = [f"R{k+1}'" for k in range(n_roots)] if show_labels else None
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

# Chart Layout Adjustments
fig.update_layout(
    title="Complex Plane ($z = x + iy$)",
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

# Render Plot
col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Root Coordinates")
    st.markdown("**Original Roots:**")
    for i in range(n_roots):
        val = complex(orig_x[i], orig_y[i])
        st.write(f"$\\text{{R}}_{{{i+1}}}$: `{val.real:+.3f} {val.imag:+.3f}j`")

    if transform_op != "None":
        st.markdown(f"**Transformed Roots ({transform_op}):**")
        for i in range(n_roots):
            val_t = complex(trans_x[i], trans_y[i])
            st.write(f"$\\text{{R}}_{{{i+1}}}'$: `{val_t.real:+.3f} {val_t.imag:+.3f}j`")
