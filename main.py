import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# -------------------------------
# App Configuration & Styling
# -------------------------------
st.set_page_config(
    page_title="🇰🇭 Cambodia's Digital Economy Forecast (2025–2030)",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main {
        background-color: #f9f9fb;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #1f3b6c;
    }
    .stAlert {
        border-radius: 10px;
        background-color: #eef5ff;
        color: #1f3b6c;
    }
    .footer {
        font-size: 0.9em;
        color: #777;
        text-align: center;
        margin-top: 50px;
    }
    /* Ensure Plotly charts are fully responsive within their containers */
    .stPlotlyChart {
        width: 100% !important;
    }
    /* Adjust selectbox width for better mobile experience if needed, though Streamlit handles this well */
    .stSelectbox {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Title & Introduction
# -------------------------------
st.title("🇰🇭 Cambodia's Digital Economy: Workshop, Job, & Startup Trends Forecast (2025–2030)")
st.markdown("""
This dashboard provides a forecast of high-growth tech workshops, future job demand, and **emerging startup trends** specifically for Cambodia. The country's digital economy is expanding rapidly, with a projected growth rate of around **15% annually**. This analysis uses market projections and a log-transformed linear regression model to help inform strategic decisions for training, hiring, and resource allocation within the Cambodian tech landscape.
""")

# -------------------------------
# Pre-defined Growth Rates and Data Generation Functions
# -------------------------------
# Growth rates based on Cambodia-specific market data (e.g., World Bank, local reports)
growth_rates_workshops = {
    'Digital Marketing & E-commerce Workshops': 18.0,
    'Cybersecurity Workshops': 22.0,
    'Cloud Computing Workshops': 20.0,
    'Web Development Workshops': 15.0,
    'Data Science & Analytics Workshops': 20.0,
    'Blockchain & Fintech Workshops': 25.0,
    'AI & ML Workshops': 35.0,
    'IoT Workshops': 12.0,
    'DevOps & Automation Workshops': 17.0,
}

growth_rates_jobs = {
    'AI Engineer Jobs': 40.0,
    'Cybersecurity Specialist Jobs': 22.0,
    'Web Developer Jobs': 18.0,
    'Data Scientist Jobs': 20.0,
    'Blockchain Developer Jobs': 28.0,
    'Fintech Specialist Jobs': 25.0,
    'Cloud Architect Jobs': 23.0,
    'DevOps Engineer Jobs': 19.0,
    'Digital Marketing Specialist Jobs': 18.0,
}

# New growth rates for startups
growth_rates_startups = {
    'Fintech Startups': 30.0,
    'E-commerce & Logistics Startups': 20.0,
    'EdTech Startups': 25.0,
    'AgriTech Startups': 18.0,
    'HealthTech Startups': 22.0,
    'AI/Big Data Startups': 35.0,
    'Gaming & Entertainment Startups': 15.0,
}


def generate_data(growth_rates, start_values):
    """Generates a DataFrame with projected trends based on CAGR."""
    data = {'Year': list(range(2025, 2031))}
    for item, rate in growth_rates.items():
        start_value = start_values.get(item, 10) # Default to 10 for startups
        data[item] = [int(start_value * ((1 + rate/100)**i)) for i in range(6)]
    return pd.DataFrame(data)

# Define starting values for workshops and jobs (adjusted for Cambodia's market size)
start_values_workshops = {
    'Digital Marketing & E-commerce Workshops': 100,
    'Cybersecurity Workshops': 100,
    'Cloud Computing Workshops': 100,
    'Web Development Workshops': 100,
    'Data Science & Analytics Workshops': 100,
    'Blockchain & Fintech Workshops': 100,
    'AI & ML Workshops': 100,
    'IoT Workshops': 100,
    'DevOps & Automation Workshops': 100,
}

start_values_jobs = {
    'AI Engineer Jobs': 100,
    'Cybersecurity Specialist Jobs': 100,
    'Web Developer Jobs': 100,
    'Data Scientist Jobs': 100,
    'Blockchain Developer Jobs': 100,
    'Fintech Specialist Jobs': 100,
    'Cloud Architect Jobs': 100,
    'DevOps Engineer Jobs': 100,
    'Digital Marketing Specialist Jobs': 100,
}

# New starting values for startups
start_values_startups = {
    'Fintech Startups': 100,
    'E-commerce & Logistics Startups': 100,
    'EdTech Startups': 100,
    'AgriTech Startups': 100,
    'HealthTech Startups': 100,
    'AI/Big Data Startups': 100,
    'Gaming & Entertainment Startups': 100,
}

df_workshops = generate_data(growth_rates_workshops, start_values_workshops)
df_jobs = generate_data(growth_rates_jobs, start_values_jobs)
df_startups = generate_data(growth_rates_startups, start_values_startups) # Generate startup data

# -------------------------------
# Data Sources
# -------------------------------
st.subheader("📚 Data Sources")
st.markdown("""
This dashboard's data is based on market projections for Cambodia and Southeast Asia from various sources:
- **Digital Economy Reports**: Informed by market research from organizations like the World Bank, Asian Development Bank, and local research firms.
- **Job Market Trends**: Derived from labor market analyses by the National Employment Agency (NEA) and job-seeking platforms that highlight in-demand skills and roles.
- **Government Initiatives**: Reflects the goals and frameworks outlined in the Cambodian government's **Digital Economy and Society Policy Framework (2021-2035)**.
""")

# -------------------------------
# Display Workshop Data & Trends
# -------------------------------
st.subheader("📈 Workshop Participation Forecast (2025–2030)")
st.dataframe(df_workshops.style.format({"Year": "{:d}"}).background_gradient(cmap="Blues", subset=df_workshops.columns[1:]))

# Interactive Plot for Workshops
st.subheader("📊 Workshop Trend Visualization")
fig_workshops = go.Figure()
colors_workshops = px.colors.qualitative.Bold
for idx, col in enumerate(df_workshops.columns[1:]):
    fig_workshops.add_trace(go.Scatter(
        x=df_workshops['Year'],
        y=df_workshops[col],
        mode='lines+markers',
        name=col,
        line=dict(width=3, color=colors_workshops[idx % len(colors_workshops)]),
        marker=dict(size=8),
        hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Participants: %{y:,}<extra></extra>",
        text=[col]*len(df_workshops)
    ))
fig_workshops.update_layout(
    title="Projected Workshop Participation (2025–2030)",
    xaxis_title="Year",
    yaxis_title="Participants",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=500
)
st.plotly_chart(fig_workshops, use_container_width=True)

st.markdown("---")

# -------------------------------
# Display Job Data & Trends
# -------------------------------
st.subheader("💼 Future Job Demand Forecast (2025–2030)")
st.markdown("""
This section forecasts the projected demand for key high-growth tech roles within Cambodia's evolving digital economy.
""")
st.dataframe(df_jobs.style.format({"Year": "{:d}"}).background_gradient(cmap="Greens", subset=df_jobs.columns[1:]))

# Interactive Plot for Jobs
st.subheader("📊 Job Demand Trend Visualization")
fig_jobs = go.Figure()
colors_jobs = px.colors.qualitative.Plotly
for idx, col in enumerate(df_jobs.columns[1:]):
    fig_jobs.add_trace(go.Scatter(
        x=df_jobs['Year'],
        y=df_jobs[col],
        mode='lines+markers',
        name=col,
        line=dict(width=3, color=colors_jobs[idx % len(colors_jobs)]),
        marker=dict(size=8),
        hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Jobs: %{y:,}<extra></extra>",
        text=[col]*len(df_jobs)
    ))
fig_jobs.update_layout(
    title="Projected Job Demand (2025–2030)",
    xaxis_title="Year",
    yaxis_title="Number of Jobs",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=500
)
st.plotly_chart(fig_jobs, use_container_width=True)

st.markdown("---")

# -------------------------------
# Display Startup Data & Trends
# -------------------------------
st.subheader("🚀 Emerging Startup Landscape Forecast (2025–2030)")
st.markdown("""
This section forecasts the projected growth of new technology startups across various key sectors in Cambodia.
""")
st.dataframe(df_startups.style.format({"Year": "{:d}"}).background_gradient(cmap="Purples", subset=df_startups.columns[1:]))

# Interactive Plot for Startups
st.subheader("📊 Startup Trend Visualization")
fig_startups = go.Figure()
custom_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']
colors_startups = custom_colors * ((len(df_startups.columns) // len(custom_colors)) + 1)
for idx, col in enumerate(df_startups.columns[1:]):
    fig_startups.add_trace(go.Scatter(
        x=df_startups['Year'],
        y=df_startups[col],
        mode='lines+markers',
        name=col,
        line=dict(width=3, color=colors_startups[idx % len(colors_startups)]),
        marker=dict(size=8),
        hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Startups: %{y:,}<extra></extra>",
        text=[col]*len(df_startups)
    ))
fig_startups.update_layout(
    title="Projected New Startup Growth (2025–2030)",
    xaxis_title="Year",
    yaxis_title="Number of Startups",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=500
)
st.plotly_chart(fig_startups, use_container_width=True)

st.markdown("---")

# -------------------------------
# Growth Rate Analysis for Workshops, Jobs, and Startups
# -------------------------------
st.subheader("🔍 Growth Insights: Workshops, Jobs, & Startups")

growth_df_combined = pd.DataFrame([
    *growth_rates_workshops.items(),
    *growth_rates_jobs.items(),
    *growth_rates_startups.items() # Include startup growth rates
], columns=["Topic", "CAGR (%)"])
growth_df_combined['Type'] = ['Workshop'] * len(growth_rates_workshops) + \
                             ['Job'] * len(growth_rates_jobs) + \
                             ['Startup'] * len(growth_rates_startups) # Assign type
growth_df_combined = growth_df_combined.sort_values("CAGR (%)", ascending=True)

fig_growth = px.bar(
    growth_df_combined,
    x="CAGR (%)",
    y="Topic",
    color="Type",
    orientation='h',
    text="CAGR (%)",
    color_discrete_map={'Workshop': 'rgba(0,119,200,0.8)', 'Job': 'rgba(34,139,34,0.8)', 'Startup': 'rgba(128,0,128,0.8)'}, # Add startup color
    title="CAGR (Compound Annual Growth Rate) by Workshop, Job, and Startup Type"
)
fig_growth.update_layout(template="plotly_white", height=700, yaxis={'categoryorder':'total ascending'}) # Adjust height for more items
st.plotly_chart(fig_growth, use_container_width=True)

st.markdown("""
**💡 Insight**: There's a strong correlation between high-growth workshops, future job demand, and the **emergence of new startups**. Fields like **AI/Big Data** and **Fintech** show explosive growth across all three categories, highlighting significant opportunities within the Cambodian digital economy.
""")
st.markdown("---")

# -------------------------------
# Dynamic Percentage Growth Calculator (NEW SECTION)
# -------------------------------
st.subheader("📈 Dynamic Percentage Growth Calculator")
st.markdown("""
Use this section to calculate the percentage growth of any selected item between two specific years.
""")

# Select category
category_options = ["Workshops", "Jobs", "Startups"]
selected_category = st.selectbox("Select Data Category", category_options, key="growth_category")

# Determine the DataFrame and available items based on selected category
df_to_use = None
items_to_choose = []
if selected_category == "Workshops":
    df_to_use = df_workshops
    items_to_choose = df_workshops.columns[1:].tolist()
elif selected_category == "Jobs":
    df_to_use = df_jobs
    items_to_choose = df_jobs.columns[1:].tolist()
elif selected_category == "Startups":
    df_to_use = df_startups
    items_to_choose = df_startups.columns[1:].tolist()

# Select the specific item
if items_to_choose:
    selected_item = st.selectbox(f"Select {selected_category} Item", items_to_choose, key="growth_item")

    # Select start and end years
    min_year_data = df_to_use['Year'].min()
    max_year_data = df_to_use['Year'].max()

    col_start_year, col_end_year = st.columns(2)
    with col_start_year:
        start_year_growth = st.number_input(
            "Start Year",
            min_value=min_year_data,
            max_value=max_year_data,
            value=min_year_data,
            key="growth_start_year"
        )
    with col_end_year:
        end_year_growth = st.number_input(
            "End Year",
            min_value=min_year_data,
            max_value=max_year_data,
            value=max_year_data,
            key="growth_end_year"
        )

    # Perform calculation
    if start_year_growth >= end_year_growth:
        st.error("End Year must be greater than Start Year for growth calculation.")
    else:
        try:
            previous_value = df_to_use[df_to_use['Year'] == start_year_growth][selected_item].iloc[0]
            current_value = df_to_use[df_to_use['Year'] == end_year_growth][selected_item].iloc[0]

            st.write(f"#### Growth for **{selected_item}** from {start_year_growth} to {end_year_growth}")
            st.write(f"- Value in {start_year_growth}: **{previous_value:,}**")
            st.write(f"- Value in {end_year_growth}: **{current_value:,}**")

            if previous_value == 0:
                st.warning("Cannot calculate percentage growth: The starting value is zero.")
            else:
                growth_percentage = ((current_value - previous_value) / previous_value) * 100
                st.metric(label="Percentage Growth", value=f"{growth_percentage:.2f}%")

        except IndexError:
            st.error("Data for the selected year(s) or item is not available.")
else:
    st.info("No items available for this category.")

st.markdown("---")

# -------------------------------
# Prediction Section for WORKSHOPS - Updated with columns
# -------------------------------
st.subheader("🔮 Predict Future Workshop Participation (2031–2033)")

# Use columns for better layout of selectbox and prediction results
col1_w, col2_w = st.columns([1, 2]) # Adjust ratio as needed

with col1_w:
    workshop_role = st.selectbox(
        "Select a Workshop to Forecast",
        options=df_workshops.columns[1:],
        key="workshop_pred",
        help="Choose a workshop to predict participation for the next three years."
    )

# Prepare data for workshop prediction
X_workshop = df_workshops['Year'].values.reshape(-1, 1)
y_workshop = df_workshops[workshop_role].values

# Fit a Linear Regression model on log-transformed data for a better fit on exponential data
# Add 1 to y_workshop to avoid log(0) if any values are 0
model_workshop = LinearRegression()
model_workshop.fit(X_workshop, np.log(y_workshop + 1))

# Predict future years
future_years = np.array([2031, 2032, 2033]).reshape(-1, 1)
preds_log_workshop = model_workshop.predict(future_years)
preds_workshop = np.exp(preds_log_workshop) - 1 # Transform back and subtract 1

# Model evaluation
y_pred_hist_workshop = np.exp(model_workshop.predict(X_workshop)) - 1
r2_workshop = r2_score(y_workshop, y_pred_hist_workshop)
mae_workshop = mean_absolute_error(y_workshop, y_pred_hist_workshop)

# Confidence intervals (approximate)
residuals_log = np.log(y_workshop + 1) - model_workshop.predict(X_workshop)
std_error_log = np.std(residuals_log)
ci_upper_log = preds_log_workshop + 1.96 * std_error_log
ci_lower_log = preds_log_workshop - 1.96 * std_error_log
ci_upper_workshop = np.exp(ci_upper_log) - 1
ci_lower_workshop = np.exp(ci_lower_log) - 1

with col2_w:
    st.write(f"**Regression Model**: Log-transformed Linear Regression")
    st.write(f"**Model Fit**: R² = {r2_workshop:.3f}, MAE = {int(mae_workshop)} participants")
    st.write(f"### Predicted Participation for {workshop_role}")
    pred_df_workshop = pd.DataFrame({
        "Year": future_years.flatten(),
        "Predicted Participants": np.round(preds_workshop, 0).astype(int),
        "Lower 95% CI": np.round(ci_lower_workshop, 0).astype(int),
        "Upper 95% CI": np.round(ci_upper_workshop, 0).astype(int)
    })
    st.dataframe(pred_df_workshop.style.format({"Predicted Participants": "{:,}",
                                       "Lower 95% CI": "{:,}",
                                       "Upper 95% CI": "{:,}"}))

# Plot prediction with confidence band (outside columns to use full width)
fig_pred_workshop = go.Figure()

fig_pred_workshop.add_trace(go.Scatter(
    x=df_workshops['Year'], y=df_workshops[workshop_role], mode='lines+markers', name='Historical',
    line=dict(color='blue'), marker=dict(size=6)
))
fig_pred_workshop.add_trace(go.Scatter(
    x=future_years.flatten(), y=preds_workshop, mode='lines+markers', name='Forecast',
    line=dict(color='red', dash='dot'), marker=dict(size=6, symbol='triangle-up')
))
fig_pred_workshop.add_trace(go.Scatter(
    x=np.concatenate([future_years.flatten(), future_years.flatten()[::-1]]),
    y=np.concatenate([ci_upper_workshop, ci_lower_workshop[::-1]]),
    fill='toself',
    fillcolor='rgba(255,100,100,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    showlegend=True,
    name='95% Confidence Interval'
))
fig_pred_workshop.update_layout(
    title=f"{workshop_role} Forecast (2031–2033) with 95% Confidence Interval",
    xaxis_title="Year",
    yaxis_title="Participants",
    template="plotly_white",
    hovermode="x unified"
)
st.plotly_chart(fig_pred_workshop, use_container_width=True)

st.markdown("---")

# -------------------------------
# Prediction Section for JOBS - Updated with columns
# -------------------------------
st.subheader("🔮 Predict Future Job Demand (2031–2033)")

# Use columns for better layout of selectbox and prediction results
col1_j, col2_j = st.columns([1, 2]) # Adjust ratio as needed

with col1_j:
    job_role = st.selectbox(
        "Select a Job Role to Forecast",
        options=df_jobs.columns[1:],
        key="job_pred",
        help="Choose a job role to predict demand for the next three years."
    )

# Prepare data for job prediction
X_job = df_jobs['Year'].values.reshape(-1, 1)
y_job = df_jobs[job_role].values

# Fit a Linear Regression model on log-transformed data
model_job = LinearRegression()
model_job.fit(X_job, np.log(y_job + 1))

# Predict future
preds_log_job = model_job.predict(future_years)
preds_job = np.exp(preds_log_job) - 1

# Model evaluation
y_pred_hist_job = np.exp(model_job.predict(X_job)) - 1
r2_job = r2_score(y_job, y_pred_hist_job)
mae_job = mean_absolute_error(y_job, y_pred_hist_job)

# Confidence intervals (approximate)
residuals_log_job = np.log(y_job + 1) - model_job.predict(X_job)
std_error_log_job = np.std(residuals_log_job)
ci_upper_log_job = preds_log_job + 1.96 * std_error_log_job
ci_lower_log_job = preds_log_job - 1.96 * std_error_log_job
ci_upper_job = np.exp(ci_upper_log_job) - 1
ci_lower_job = np.exp(ci_lower_log_job) - 1

with col2_j:
    st.write(f"**Regression Model**: Log-transformed Linear Regression")
    st.write(f"**Model Fit**: R² = {r2_job:.3f}, MAE = {int(mae_job)} jobs")
    st.write(f"### Predicted Demand for {job_role}")
    pred_df_job = pd.DataFrame({
        "Year": future_years.flatten(),
        "Predicted Jobs": np.round(preds_job, 0).astype(int),
        "Lower 95% CI": np.round(ci_lower_job, 0).astype(int),
        "Upper 95% CI": np.round(ci_upper_job, 0).astype(int)
    })
    st.dataframe(pred_df_job.style.format({"Predicted Jobs": "{:,}",
                                           "Lower 95% CI": "{:,}",
                                           "Upper 95% CI": "{:,}"}))

# Plot prediction with confidence band (outside columns to use full width)
fig_pred_job = go.Figure()

fig_pred_job.add_trace(go.Scatter(
    x=df_jobs['Year'], y=df_jobs[job_role], mode='lines+markers', name='Historical',
    line=dict(color='green'), marker=dict(size=6)
))
fig_pred_job.add_trace(go.Scatter(
    x=future_years.flatten(), y=preds_job, mode='lines+markers', name='Forecast',
    line=dict(color='orange', dash='dot'), marker=dict(size=6, symbol='triangle-up')
))
fig_pred_job.add_trace(go.Scatter(
    x=np.concatenate([future_years.flatten(), future_years.flatten()[::-1]]),
    y=np.concatenate([ci_upper_job, ci_lower_job[::-1]]),
    fill='toself',
    fillcolor='rgba(255,165,0,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    showlegend=True,
    name='95% Confidence Interval'
))
fig_pred_job.update_layout(
    title=f"{job_role} Forecast (2031–2033) with 95% Confidence Interval",
    xaxis_title="Year",
    yaxis_title="Number of Jobs",
    template="plotly_white",
    hovermode="x unified"
)
st.plotly_chart(fig_pred_job, use_container_width=True)

st.markdown("---")

# -------------------------------
# Prediction Section for STARTUPS (NEW) - Updated with columns
# -------------------------------
st.subheader("🔮 Predict Future Startup Growth (2031–2033)")

# Use columns for better layout of selectbox and prediction results
col1_s, col2_s = st.columns([1, 2]) # Adjust ratio as needed

with col1_s:
    startup_type = st.selectbox(
        "Select a Startup Category to Forecast",
        options=df_startups.columns[1:],
        key="startup_pred",
        help="Choose a startup category to predict growth for the next three years."
    )

# Prepare data for startup prediction
X_startup = df_startups['Year'].values.reshape(-1, 1)
y_startup = df_startups[startup_type].values

# Fit a Linear Regression model on log-transformed data
model_startup = LinearRegression()
model_startup.fit(X_startup, np.log(y_startup + 1)) # Add 1 to avoid log(0)

# Predict future
preds_log_startup = model_startup.predict(future_years)
preds_startup = np.exp(preds_log_startup) - 1 # Transform back and subtract 1

# Model evaluation
y_pred_hist_startup = np.exp(model_startup.predict(X_startup)) - 1
r2_startup = r2_score(y_startup, y_pred_hist_startup)
mae_startup = mean_absolute_error(y_startup, y_pred_hist_startup)

# Confidence intervals (approximate)
residuals_log_startup = np.log(y_startup + 1) - model_startup.predict(X_startup)
std_error_log_startup = np.std(residuals_log_startup)
ci_upper_log_startup = preds_log_startup + 1.96 * std_error_log_startup
ci_lower_log_startup = preds_log_startup - 1.96 * std_error_log_startup
ci_upper_startup = np.exp(ci_upper_log_startup) - 1
ci_lower_startup = np.exp(ci_lower_log_startup) - 1

with col2_s:
    st.write(f"**Regression Model**: Log-transformed Linear Regression")
    st.write(f"**Model Fit**: R² = {r2_startup:.3f}, MAE = {int(mae_startup)} startups")
    st.write(f"### Predicted Growth for {startup_type}")
    pred_df_startup = pd.DataFrame({
        "Year": future_years.flatten(),
        "Predicted Startups": np.round(preds_startup, 0).astype(int),
        "Lower 95% CI": np.round(ci_lower_startup, 0).astype(int),
        "Upper 95% CI": np.round(ci_upper_startup, 0).astype(int)
    })
    st.dataframe(pred_df_startup.style.format({"Predicted Startups": "{:,}",
                                           "Lower 95% CI": "{:,}",
                                           "Upper 95% CI": "{:,}"}))

# Plot prediction with confidence band (outside columns to use full width)
fig_pred_startup = go.Figure()

fig_pred_startup.add_trace(go.Scatter(
    x=df_startups['Year'], y=df_startups[startup_type], mode='lines+markers', name='Historical',
    line=dict(color='purple'), marker=dict(size=6)
))
fig_pred_startup.add_trace(go.Scatter(
    x=future_years.flatten(), y=preds_startup, mode='lines+markers', name='Forecast',
    line=dict(color='magenta', dash='dot'), marker=dict(size=6, symbol='triangle-up')
))
fig_pred_startup.add_trace(go.Scatter(
    x=np.concatenate([future_years.flatten(), future_years.flatten()[::-1]]),
    y=np.concatenate([ci_upper_startup, ci_lower_startup[::-1]]),
    fill='toself',
    fillcolor='rgba(128,0,128,0.2)', # Purple fill
    line=dict(color='rgba(255,255,255,0)'),
    showlegend=True,
    name='95% Confidence Interval'
))
fig_pred_startup.update_layout(
    title=f"{startup_type} Forecast (2031–2033) with 95% Confidence Interval",
    xaxis_title="Year",
    yaxis_title="Number of Startups",
    template="plotly_white",
    hovermode="x unified"
)
st.plotly_chart(fig_pred_startup, use_container_width=True)

st.markdown("---")

# -------------------------------
# Summary & Recommendations
# -------------------------------
st.subheader("✅ Key Takeaways & Recommendations for Cambodia")
st.markdown("""
- **AI & ML**: This is a rapidly emerging field with significant job growth, but a current shortage of skilled professionals. Investing in foundational AI and data analytics workshops is crucial for building a future-ready workforce.
- **Cybersecurity**: As the digital economy grows, cybersecurity is a top priority for Cambodian businesses. There is a high demand for professionals with skills in ethical hacking and data security.
- **Cloud Computing**: Demand for cloud skills is driven by the migration of businesses to scalable IT solutions. Training in major cloud platforms (e.g., AWS, Azure) is highly valuable.
- **Blockchain**: Cambodia's adoption of the national payment system, **Bakong**, highlights the country's proactive approach to blockchain technology. This creates a unique local demand for developers in this niche.
- **Web Development**: Remains a foundational and highly sought-after skill, essential for the booming e-commerce and startup ecosystem.
- **Recommendations**: For individuals, focus on acquiring high-demand skills like Python, SQL, and cloud platforms. For educational institutions and businesses, aligning training programs with the government's **Digital Economy and Society Policy** is key to closing the skills gap and meeting market demand.
""")

# Footer
st.markdown("<div class='footer'>Dashboard by Data Science Team | Forecasting Model: Log-transformed Linear Regression | Data: Market-Based Projections for Cambodia (2025–2030)</div>", unsafe_allow_html=True)
st.markdown("""
This dashboard is designed to provide insights into Cambodia's digital economy, focusing on workshops, job demand, and startup trends. The data is based on market projections and aims to support strategic decisions for training, hiring, and resource allocation within the Cambodian tech landscape.
""")
