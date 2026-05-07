import streamlit as st
import pandas as pd
import numpy as np

from utils.predictor import predict_stemness, predict_marker
from utils.db import connect


# ── SAVE HISTORY ───────────────────────────────────────
def save_history(user, sample, score, cls):
    try:
        conn = connect()
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO history (username, sample_name, prediction, classification)
            VALUES (?, ?, ?, ?)
            """,
            (user, str(sample), float(score), str(cls))
        )
        conn.commit()
        conn.close()
    except Exception as e:
        st.warning(f"History save failed: {e}")


# ── RISK BADGE HTML ────────────────────────────────────
def risk_badge(label: str) -> str:
    cls = {
        "High Risk":     "badge-high",
        "Moderate Risk": "badge-medium",
        "Low Risk":      "badge-low",
    }.get(label, "badge-low")
    return f"<span class='{cls}'>{label}</span>"


# ── MAIN PAGE ──────────────────────────────────────────
def prediction_page():

    st.markdown("<h1>🧬 Stemness Prediction</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p>Upload your expression matrix and choose a prediction mode.</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # ── MODE SELECTION ─────────────────────────────────
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)

    st.markdown("### ⚙️ Prediction Mode")

    mode = st.radio(
        "",
        ["Full Transcriptome", "Marker Panel"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if mode == "Full Transcriptome":
        st.info(
            "Uses the full gene expression profile. "
            "Ensure your CSV contains all training features."
        )
    else:
        st.info(
            "Uses 8 stemness marker genes: "
            "SOX2, NANOG, POU5F1, PROM1, MYC, KLF4, ALDH1A1, CD44"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # ── FILE UPLOAD ────────────────────────────────────
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)

    st.markdown("### 📂 Upload Expression Matrix")

    file = st.file_uploader(
        "Upload CSV (samples as rows, genes as columns)",
        type=["csv"],
        label_visibility="visible"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if file is None:
        return

    # ── LOAD DATA ──────────────────────────────────────
    df = pd.read_csv(file, index_col=0)

    with st.expander("📋 Data Preview", expanded=False):
        st.dataframe(df.head(), use_container_width=True)

    st.markdown(
        f"<p>✅ Loaded <strong>{len(df)}</strong> samples × "
        f"<strong>{df.shape[1]}</strong> features</p>",
        unsafe_allow_html=True
    )

    if not st.button("✨  Run Prediction →", use_container_width=False):
        return

    # ── RUN PREDICTION ─────────────────────────────────
    with st.spinner("Running prediction…"):

        if mode == "Full Transcriptome":
            pred, prob = predict_stemness(df)

        else:
            pred = predict_marker(df)
            pred = np.array(pred)
            norm = pred / (pred.max() + 1e-9)
            prob = np.column_stack((1 - norm, norm))

    # ── BUILD RESULTS TABLE ────────────────────────────
    results = pd.DataFrame(
        {
            "Predicted Stemness": pred,
            "Risk Probability":   prob[:, 1],
        },
        index=df.index
    )

    results["Stemness Class"] = "Low"
    results.loc[results["Predicted Stemness"] >= 1.8, "Stemness Class"] = "Intermediate"
    results.loc[results["Predicted Stemness"] >  2.3, "Stemness Class"] = "High"

    results["Prognostic Group"] = results["Risk Probability"].apply(
        lambda r: "High Risk" if r > 0.70 else ("Moderate Risk" if r >= 0.30 else "Low Risk")
    )

    # ── SUMMARY METRICS ────────────────────────────────
    st.write("")
    st.markdown("### 📊 Prediction Summary")

    m1, m2, m3 = st.columns(3)

    with m1:
        high_n = (results["Stemness Class"] == "High").sum()
        st.metric("High Stemness Samples", high_n)

    with m2:
        avg_s = results["Predicted Stemness"].mean()
        st.metric("Avg. Stemness Score", f"{avg_s:.3f}")

    with m3:
        hr_n = (results["Prognostic Group"] == "High Risk").sum()
        st.metric("High Risk Samples", hr_n)

    st.write("")

    # ── RESULTS TABLE ──────────────────────────────────
    st.markdown("### 📋 Results Table")
    st.dataframe(results, use_container_width=True)

    csv_out = results.to_csv().encode("utf-8")
    st.download_button(
        "⬇  Download Predictions CSV",
        data=csv_out,
        file_name="stemquant_predictions.csv",
        mime="text/csv"
    )

    st.write("")

    # ── INTERPRETATION CARDS ───────────────────────────
    st.markdown("### 🔍 Representative Sample Interpretations")

    for category in ["High", "Intermediate", "Low"]:

        subset = results[results["Stemness Class"] == category]

        if subset.empty:
            continue

        top = subset.sort_values("Predicted Stemness", ascending=False).iloc[0]
        sample_id = subset.sort_values("Predicted Stemness", ascending=False).index[0]

        stemness  = top["Predicted Stemness"]
        risk      = top["Risk Probability"]
        prog      = top["Prognostic Group"]

        badge_html = risk_badge(prog)

        color_map = {
            "High":         ("#fef2f2", "#dc2626", "⚠️"),
            "Intermediate": ("#fffbeb", "#d97706", "⚡"),
            "Low":          ("#f0fdf4", "#16a34a", "✅"),
        }
        bg, accent, icon = color_map[category]

        st.markdown(f"""
<div style='background:{bg};border-radius:20px;padding:24px 28px;
            margin-bottom:16px;border:1px solid {accent}22;'>
    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
        <div>
            <p style='margin:0 0 4px;font-size:12px;font-weight:700;
                      color:{accent};text-transform:uppercase;letter-spacing:0.08em;'>
                {icon}  {category} Stemness Representative
            </p>
            <h3 style='margin:0 0 12px;font-size:20px;color:#1e293b;'>
                {sample_id}
            </h3>
        </div>
        {badge_html}
    </div>
    <div style='display:flex;gap:32px;'>
        <div>
            <p style='margin:0;font-size:11px;color:#64748b;font-weight:600;'>
                STEMNESS SCORE
            </p>
            <p style='margin:0;font-size:22px;font-weight:800;color:#1e293b;'>
                {stemness:.3f}
            </p>
        </div>
        <div>
            <p style='margin:0;font-size:11px;color:#64748b;font-weight:600;'>
                RISK PROBABILITY
            </p>
            <p style='margin:0;font-size:22px;font-weight:800;color:#1e293b;'>
                {risk:.3f}
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

        if category == "High":
            st.warning(
                "Strong stem-like aggressive phenotype detected. "
                "Possible therapy resistance, poor prognosis, and tumor progression."
            )
        elif category == "Intermediate":
            st.info(
                "Intermediate stemness phenotype. "
                "Partial stem-cell programs may be active."
            )
        else:
            st.success(
                "Lower stemness phenotype. "
                "Comparatively less aggressive biology."
            )

    # ── LEGEND ─────────────────────────────────────────
    st.write("")

    with st.expander("📖 Score Interpretation Guide", expanded=False):

        lg1, lg2 = st.columns(2)

        with lg1:
            st.markdown("""
**Stemness Score**
| Range | Class |
|---|---|
| < 1.8 | Low |
| 1.8 – 2.3 | Intermediate |
| > 2.3 | High |
""")

        with lg2:
            st.markdown("""
**Risk Probability**
| Range | Group |
|---|---|
| 0.00 – 0.30 | Low Risk |
| 0.30 – 0.70 | Moderate Risk |
| > 0.70 | High Risk |
""")

    # ── MARKER PANEL NOTE ──────────────────────────────
    if mode == "Marker Panel":
        with st.expander("🧪 Marker Genes Used", expanded=False):
            st.code(
                "SOX2  NANOG  POU5F1  PROM1  MYC  KLF4  ALDH1A1  CD44",
                language=None
            )

    # ── SAVE HISTORY ───────────────────────────────────
    for i, sample in enumerate(df.index):
        save_history(
            st.session_state.user,
            str(sample),
            float(prob[i, 1]),
            str(pred[i])
        )

    st.success("✅  Predictions saved to your history.")

    st.markdown(
        "<div class='sq-footer'>© 2026 StemQuant. All rights reserved.</div>",
        unsafe_allow_html=True
    )
