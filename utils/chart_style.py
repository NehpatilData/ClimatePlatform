import plotly.graph_objects as go


def style_chart(fig):
    """Apply consistent professional styling to all Plotly charts across the platform."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=60, r=40, t=60, b=50),
        font=dict(
            family="Inter, system-ui, -apple-system, sans-serif",
            size=13,
            color="#1f2937",          # dark body text
        ),
        title=dict(
            font=dict(size=18, color="#111827", family="Inter, system-ui, sans-serif"),
            x=0.02,
            xanchor="left",
        ),
        legend=dict(
            font=dict(size=12, color="#374151"),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#e5e7eb",
            borderwidth=1,
            itemsizing="constant",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        height=430,
    )

    # Axes – dark labels, readable ticks, subtle grid
    axis_style = dict(
        title_font=dict(size=13, color="#374151"),
        tickfont=dict(size=11, color="#4b5563"),
        gridcolor="#f3f4f6",
        zerolinecolor="#d1d5db",
        linecolor="#d1d5db",
        showline=True,
        linewidth=1,
        showgrid=True,
        gridwidth=1,
        automargin=True,
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)

    return fig