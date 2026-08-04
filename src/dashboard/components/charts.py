"""
Reusable Plotly Charts
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def donut_chart(df, names, values, title):
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.45,
        title=title,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig.update_layout(
        legend_title=None,
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def line_chart(df, x, y, title):
    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title,
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title="Value",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def bar_chart(df, x, y, title):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def revenue_profit_chart(df):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["year"],
            y=df["sales"],
            name="Revenue",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["net_profit"],
            mode="lines+markers",
            name="Net Profit",
        )
    )

    fig.update_layout(
        title="Revenue vs Net Profit",
        xaxis_title="Year",
        yaxis_title="₹ Crore",
    )

    return fig


def radar_chart(labels, company_values, peer_values=None):
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=company_values,
            theta=labels,
            fill="toself",
            name="Company",
        )
    )

    if peer_values is not None:
        fig.add_trace(
            go.Scatterpolar(
                r=peer_values,
                theta=labels,
                name="Peer Average",
                line=dict(dash="dash"),
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
    )

    return fig


def bubble_chart(df, x, y, size, color, hover):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=hover,
    )

    return fig


def treemap_chart(df, path, values, color):
    fig = px.treemap(
        df,
        path=path,
        values=values,
        color=color,
    )

    return fig