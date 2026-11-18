"""Shared presentation, charts, and source-trace controls."""
from html import escape
import re
import pandas as pd
import plotly.express as px
import streamlit as st

PALETTE = {"ink": "#17324D", "navy": "#102B45", "teal": "#007E87",
           "copper": "#B65F3D", "muted": "#52677A"}


def _emphasis(value: str) -> str:
    """Preserve the small amount of Markdown emphasis used in page copy."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escape(value))


def inject_style() -> None:
    st.markdown("""<style>
    :root {--ink:#17324D;--navy:#102B45;--teal:#007E87;--muted:#52677A;}
    @keyframes motion-fade-up {
      from {opacity:0;transform:translateY(8px)}
      to {opacity:1;transform:translateY(0)}
    }
    .stApp {background:#F3F6F8;color:var(--ink);}
    .block-container {max-width:1220px;padding-top:1.1rem;padding-bottom:2.5rem;}
    [data-testid="stSidebar"] {background:#102B45;border-right:1px solid #25455D;}
    [data-testid="stSidebar"] * {color:#E6F0F2;}
    [data-testid="stSidebar"] a {transition:background-color 160ms ease,color 160ms ease;}
    [data-testid="stSidebar"] a:hover {background:#22465B;}
    [data-testid="stSidebar"] [aria-current="page"] {background:#28566A;}
    [data-testid="stSidebar"] [data-testid="stSidebarNav"]::before {
      content:"EU POLICY OBSERVATORY";display:block;color:#80CFC9;font-size:.72rem;
      font-weight:750;letter-spacing:.16em;padding:1.3rem 1.1rem .9rem;}
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {padding-top:.3rem;}
    .sidebar-meta {border-top:1px solid #355369;margin:.8rem .5rem 0;padding:1.1rem .55rem;
      color:#DCE9ED;font-size:.82rem;line-height:1.7;}
    .sidebar-meta strong {font-size:.9rem;letter-spacing:.04em;color:#FFFFFF;}
    .sidebar-meta span {color:#A8C8CF;}
    .page-hero {background:#102B45;border:1px solid #23475B;border-left:5px solid #59C5BB;
      border-radius:14px;padding:1.35rem 1.7rem 1.4rem;margin:.45rem 0 1.1rem;
      box-shadow:0 10px 24px rgba(16,43,69,.10);}
    .page-hero .eyebrow {color:#80CFC9;font-size:.73rem;font-weight:750;
      letter-spacing:.15em;text-transform:uppercase;margin-bottom:.4rem;}
    .page-hero h1 {color:#FFFFFF;font-size:2.25rem;line-height:1.13;
      font-weight:760;letter-spacing:-.035em;margin:0 0 .55rem;}
    .page-hero p {color:#DCE9ED;font-size:1.02rem;line-height:1.5;margin:0;max-width:920px;}
    .page-hero strong {color:#FFFFFF;}
    h2,h3 {color:var(--ink);letter-spacing:-.02em;}
    div[data-testid="stMetric"] {background:#FFFFFF;border:1px solid #D7E2E8;
      border-top:4px solid #007E87;border-radius:12px;padding:1rem 1.1rem;
      box-shadow:0 6px 18px rgba(16,43,69,.045);min-height:126px;
      transition:transform 180ms ease,box-shadow 180ms ease,border-color 180ms ease;}
    div[data-testid="stMetric"]:hover {transform:translateY(-2px);
      box-shadow:0 10px 24px rgba(16,43,69,.11);border-color:#AFC8D0;}
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {color:#52677A;font-size:.85rem;}
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {color:#102B45;font-weight:750;}
    div[data-testid="stVerticalBlockBorderWrapper"] > div {border-color:#D7E2E8;
      border-radius:12px;background:#FFFFFF;}
    .insight {background:#E7F2F2;border-left:4px solid #007E87;border-radius:7px;
      padding:.75rem 1rem;margin:.2rem 0 1rem;color:#17324D;line-height:1.45;}
    .insight .label {color:#006F79;font-size:.68rem;font-weight:800;letter-spacing:.12em;
      text-transform:uppercase;margin-bottom:.2rem;}
    .insight p {margin:0;font-size:.94rem;}
    .source-footer {display:flex;flex-wrap:wrap;gap:.35rem 1.4rem;border-top:1px solid #CFDCE3;
      margin-top:1.4rem;padding-top:.9rem;color:#52677A;font-size:.78rem;}
    .source-footer strong {color:#17324D;}
    .source-footer a {color:#17324D;text-decoration:underline;text-underline-offset:2px;}
    [data-testid="stCaptionContainer"] {line-height:1.35;color:#52677A;}
    [data-testid="stWidgetLabel"] {font-weight:650;color:#17324D;}
    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div,
    .stButton > button {transition:border-color 160ms ease,box-shadow 160ms ease,background-color 160ms ease;}
    .stSelectbox [data-baseweb="select"]:hover > div,
    .stMultiSelect [data-baseweb="select"]:hover > div {border-color:#73AEB1;}
    .stSelectbox [data-baseweb="select"]:focus-within > div,
    .stMultiSelect [data-baseweb="select"]:focus-within > div {
      border-color:#007E87;box-shadow:0 0 0 2px rgba(0,126,135,.16);}
    .stButton > button:hover {border-color:#73AEB1;color:#006F79;}
    .stButton > button:focus-visible {outline:3px solid rgba(0,126,135,.45);outline-offset:2px;}
    @media (prefers-reduced-motion: no-preference) {
      .page-hero.motion-entry {animation:motion-fade-up 320ms cubic-bezier(.2,.7,.2,1) backwards;}
      body:has(.page-hero.motion-entry) .insight,
      body:has(.page-hero.motion-entry) h2,
      body:has(.page-hero.motion-entry) h3,
      body:has(.page-hero.motion-entry) [data-testid="stVerticalBlockBorderWrapper"] {
        animation:motion-fade-up 340ms cubic-bezier(.2,.7,.2,1) 45ms backwards;
      }
      body:has(.page-hero.motion-entry) [data-testid="stMetric"] {
        animation:motion-fade-up 320ms cubic-bezier(.2,.7,.2,1) backwards;
      }
      body:has(.page-hero.motion-entry) [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {animation-delay:45ms;}
      body:has(.page-hero.motion-entry) [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {animation-delay:105ms;}
      body:has(.page-hero.motion-entry) [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {animation-delay:165ms;}
      body:has(.page-hero.motion-entry) [data-testid="stVerticalBlockBorderWrapper"] {animation-delay:90ms;}
    }
    @media (prefers-reduced-motion: reduce) {
      *,*::before,*::after {scroll-behavior:auto !important;animation:none !important;transition:none !important;}
    }
    @media(max-width:800px) {.page-hero{padding:1.1rem}.page-hero h1{font-size:1.7rem}}
    </style>""", unsafe_allow_html=True)


def header(kicker: str, title: str, introduction: str) -> None:
    motion_class = " motion-entry" if st.session_state.get("_motion_page_entry", False) else ""
    st.markdown(
        f'<section class="page-hero{motion_class}"><div class="eyebrow">{escape(kicker)}</div>'
        f'<h1>{escape(title)}</h1><p>{_emphasis(introduction)}</p></section>',
        unsafe_allow_html=True,
    )


def insight(message: str, *, label: str = "Key finding") -> None:
    st.markdown(
        f'<aside class="insight"><div class="label">{escape(label)}</div>'
        f'<p>{_emphasis(message)}</p></aside>', unsafe_allow_html=True,
    )


def chart(fig, *, key: str, transition_ms: int = 240) -> None:
    fig.update_layout(
        template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color=PALETTE["ink"], size=12),
        title_font=dict(size=17, color=PALETTE["ink"], family="Arial, sans-serif"),
        margin=dict(l=15, r=50, t=55, b=35),
        hoverlabel=dict(bgcolor="white", font_color=PALETTE["ink"]),
        legend_title_text="", height=max(340, min(710, fig.layout.height or 390)),
        transition={"duration": max(0, transition_ms), "easing": "cubic-in-out"},
    )
    fig.update_xaxes(showline=True, linecolor="#AFC3CC", gridcolor="#E7EDF0",
                     zeroline=False, tickfont_color=PALETTE["muted"])
    fig.update_yaxes(showline=False, gridcolor="#E7EDF0", zeroline=False,
                     tickfont_color=PALETTE["muted"])
    with st.container(border=True):
        st.plotly_chart(fig, width="stretch", key=key, config={"displayModeBar": False})


def trace(row: pd.Series | None, title: str = "Source trace for a displayed statistic") -> None:
    with st.expander(title):
        if row is None:
            st.info("No non-missing observation is available for this selection.")
            return
        st.markdown(f"**{row['country_name']} · {int(row['year'])} · {row['percentage']:.2f}%**")
        fields = ["source_dataset", "source_url", "country_code", "year", "size_emp",
                  "size_label", "nace_r2", "industry_label", "indicator_code", "unit",
                  "denominator_definition", "observation_status", "status_label", "source_updated",
                  "retrieved_utc", "raw_file", "raw_sha256", "source_observation_index"]
        details = {field: ("(none)" if pd.isna(row[field]) or row[field] == "" else str(row[field]))
                   for field in fields}
        st.dataframe(pd.DataFrame(details.items(), columns=["Field", "Source value"]),
                     hide_index=True, width="stretch")
        st.caption("The repository bundles the raw Eurostat JSON-stat cube; the file path, SHA-256 and observation index above identify the exact source cell for independent verification.")


def status_note(frame: pd.DataFrame) -> None:
    flagged = frame.loc[frame["observation_status"].ne("")]
    missing = int(frame["percentage"].isna().sum())
    st.caption(f"Selection: {len(frame):,} source cells · {missing:,} missing values · {len(flagged):,} flagged cells. Missing cells are omitted from charts, never treated as zero.")
    if not flagged.empty:
        with st.expander("Quality flags in this selection"):
            st.dataframe(flagged[["country_name", "year", "size_emp", "nace_r2", "percentage", "observation_status", "status_label"]],
                         hide_index=True, width="stretch")


def footer() -> None:
    st.markdown(
        '<div class="source-footer"><span><strong>Sources:</strong> '
        '<a href="https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ai/default/table?lang=en" target="_blank" rel="noopener">Eurostat isoc_eb_ai</a> / '
        '<a href="https://ec.europa.eu/eurostat/databrowser/view/isoc_eb_ain2/default/table?lang=en" target="_blank" rel="noopener">isoc_eb_ain2</a></span>'
        '<span><strong>Unit:</strong> percentages of the stated denominator</span>'
        '<span><strong>Eurostat dataset updated:</strong> 15 June 2026</span>'
        '<span><strong>Source files retrieved:</strong> 21 October 2026</span></div>',
        unsafe_allow_html=True,
    )


def country_picker(frame: pd.DataFrame, *, key: str, default: str = "DK", label: str = "Country") -> str:
    options = (frame[["country_code", "country_name"]].drop_duplicates()
               .sort_values("country_name"))
    mapping = dict(zip(options.country_code, options.country_name))
    codes = list(mapping)
    return st.selectbox(label, codes, index=codes.index(default) if default in codes else 0,
                        format_func=lambda c: mapping[c], key=key)


def bar(frame: pd.DataFrame, x: str, y: str, *, title: str, color: str = "#007F86", orientation="h"):
    return px.bar(frame, x=x, y=y, orientation=orientation, title=title,
                  color_discrete_sequence=[color], hover_data={x: ":.2f"} if x == "percentage" else None)
