import streamlit as st
import pandas as pd
import altair as alt

# Function to add tooltip CSS
def add_tooltip_css():
    st.markdown("""
        <style>
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
            color: #0073e6;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 220px;
            background-color: black;
            color: white;
            text-align: center;
            border-radius: 5px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 100%;
            left: 50%;
            margin-left: -110px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        </style>
    """, unsafe_allow_html=True)

# Function to render tooltip
def render_tooltip(text):
    return f"<span class='tooltip'>ℹ️<span class='tooltiptext'>{text}</span></span>"

# Load Data
df_cj = pd.read_csv(r"D:\Vinita\Project\Final_streamlit_Project\data\haefelehome-hin_CJ.csv")

# Create two columns
col1, col2 = st.columns(2)

# Check if DataFrame is not empty
if df_cj is not None and not df_cj.empty:
    try:
        # Work with a copy of the dataframe to avoid modifying the original
        df_temp = df_cj.copy()

        # Convert Event_Time to datetime
        df_temp["Event_Time"] = pd.to_datetime(df_temp["Event_Time"], errors='coerce')

        # Drop rows with NaT values
        df_temp = df_temp.dropna(subset=["Event_Time"])

        # --- Weekday vs Weekend Analysis ---
        with col1:
            add_tooltip_css()
            tooltip_html = render_tooltip("This chart compares the total number of sessions on weekdays and weekends based on event timestamps. The data is grouped by unique customer sessions.")
            st.markdown(f"<h1 style='display: inline-block;'>Total Sessions: Weekday vs Weekend {tooltip_html}</h1>", unsafe_allow_html=True)

            # Determine Weekday or Weekend
            df_temp["Weekday_Weekend"] = df_temp["Event_Time"].dt.dayofweek.apply(lambda x: "Weekend" if x >= 5 else "Weekday")

            # Group and count unique sessions per customer
            grouped_filtered_df = df_temp.groupby(["Customer_IP", "session"]).first().reset_index()

            # Count weekday and weekend sessions
            weekday_count = grouped_filtered_df[grouped_filtered_df["Weekday_Weekend"] == "Weekday"].shape[0]
            weekend_count = grouped_filtered_df[grouped_filtered_df["Weekday_Weekend"] == "Weekend"].shape[0]

            # Data for Pie Chart
            counts = [weekday_count, weekend_count]
            labels = ["Weekday", "Weekend"]
            total_sessions = sum(counts)

            # Prepare DataFrame for Chart
            pie_data = pd.DataFrame({
                "Category": labels,
                "Count": counts,
                "Percentage": [(count / total_sessions) * 100 if total_sessions > 0 else 0 for count in counts]
            })

            # Create Pie Chart
            pie_chart = alt.Chart(pie_data).mark_arc(size=200).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Category", type="nominal"),
                tooltip=["Category", "Count", "Percentage"]
            ).properties(width=300, height=300)

            # Display the Chart
            st.altair_chart(pie_chart, use_container_width=True)

        # --- Days of the Week Pie Chart ---
        with col2:
            add_tooltip_css()
            tooltip_html = render_tooltip("This chart displays the total number of sessions across different days of the week. Each segment represents the session count for a particular day.")
            st.markdown(f"<h1 style='display: inline-block;'>Total Sessions: Days of the Week {tooltip_html}</h1>", unsafe_allow_html=True)

            # Extract day of the week AFTER grouping
            grouped_filtered_df["days_of_week"] = grouped_filtered_df["Event_Time"].dt.dayofweek.apply(
                lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x]
            )

            # Count sessions per day
            day_count = grouped_filtered_df["days_of_week"].value_counts()
            day_count = day_count.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0)

            # Prepare DataFrame for Chart
            pie_data = pd.DataFrame({
                "Day": day_count.index,
                "Count": day_count.values
            })

            # Create Pie Chart
            pie_chart = alt.Chart(pie_data).mark_arc(size=200).encode(
                theta="Count:Q",
                color=alt.Color("Day:N", sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
                tooltip=["Day:N", "Count:Q"]
            ).properties(width=300, height=300)

            # Display Chart
            st.altair_chart(pie_chart, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display messages if data is missing
else:
    with col1:
        st.title("Total Sessions: Weekday vs Weekend")
        st.markdown("""
            <div style="border: 2px solid black; padding: 20px; background-color: #454545; border-radius: 10px; text-align: center;">
                <h3 style="font-size: 30px; color: white; font-weight: bold;">No Data Available for Total Sessions: Weekday vs Weekend</h3>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.title("Total Sessions by Day of the Week")
        st.markdown("""
            <div style="border: 2px solid black; padding: 20px; background-color: #454545; border-radius: 10px; text-align: center;">
                <h3 style="font-size: 30px; color: white; font-weight: bold;">No Data Available for Total Sessions by Day of the Week</h3>
            </div>
        """, unsafe_allow_html=True)
