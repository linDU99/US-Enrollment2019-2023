# enrollment_dash_app.py

# Create dash App: US College Enrollment Trends 2019 - 2023
# GitHub repository link: https://github.com/linDU99/US-Enrollment2019-2023.git


import dash
from dash import Dash, dcc, html, Output, Input, dash_table  # dcc - Dash Core Components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Load data from the same folder as the script
script_dir = os.path.dirname(__file__)
csv_path1 = os.path.join(script_dir, "Data-1EnrollmentBy3Groups.csv")
df1 = pd.read_csv(csv_path1)

csv_path2 = os.path.join(script_dir, "Data-2TotalEnrollment.csv")
df2_total = pd.read_csv(csv_path2)

# Convert the "Enrollment" column to integer
# Note: The "Enrollment" column have commas. Values like "4,543,556" are stored as strings, , not numbers. 
df1["Enrollment"] = (
    df1["Enrollment"]
    .replace({",": ""}, regex=True)   # Remove commas
    .astype(int))                     # Convert to integer

df1["Year"] = df1["Year"].astype(str)  # Convert to string for plotting


#========================================================================================================
# Initialize app
app = dash.Dash(__name__)
app.title = "US College Enrollment Trends"

# Layout
app.layout = html.Div([
    html.H1("US College Enrollment Trends 2019 - 2023", style={"color": "#1f77b4",'textAlign':'center'}),
    html.P("Display enrollment changes of U.S. degree-granting institutes over the years \
        by education level, gender, and study status.", style={'textAlign':'center','fontSize': 20}),
    html.P("Data source: The Integrated Postsecondary Education Data System (IPEDS) of the National Center for \
        Education Statistics (NCES)", style={'textAlign':'center', "fontSize": 15, "fontStyle": "italic"}),

    html.Hr(),  # Section divider for selection filters
    html.Div([
        html.Div([
            html.Label("Year Selection:", style={"color": 'darkblue', 'fontSize': 14, 'fontWeight': 'bold', 
                        "marginLeft": '500px', "marginRight": '8px'}),
            dcc.Checklist(
                ['2019', '2020', '2021', '2022', '2023'],  # Strings
                ['2019', '2020', '2021', '2022', '2023'],  # Default to all years
                inline=True,
                id="year-checklist")
        ], style={"display": 'flex', "alignItems": 'center', "color": 'darkblue'})  
    ], style={"width": "100%", "textAlign": "left", "padding": "10px"}),  #"justifyContent": "center"

    html.Div([
        html.Div([
            html.Label("Gender: ", style={"color": 'darkblue', 'fontSize': 14, 'fontWeight': 'bold', 
                        "marginLeft": '500px', "marginRight": '8px'}),
            dcc.Checklist(
                ['Women', 'Men'],
                ['Women', 'Men'],  # Default 
                inline=True,
                id="gender-checklist")
        ], style={"display": 'flex', "alignItems": 'left', 'fontSize': 14,})
    ], style={"width": "100%", "textAlign": "left", "padding": "10px"}), 

    html.Div([
        html.Div([
            html.Label("Study Status: ", style={"color": 'darkblue', 'fontSize': 14, 'fontWeight': 'bold', 
                        "marginLeft": '500px', "marginRight": '8px'}),
            dcc.Checklist(
                ['Full-Time', 'Part-Time'],
                ['Full-Time', 'Part-Time'],  # Default 
                inline=True,
                id="status-checklist")
        ], style={"display": 'flex', "alignItems": 'left', 'fontSize': 14,})
    ], style={ "textAlign": "left", "padding": "10px"}),
    
    # Secetion of plots
    html.Hr(style={"marginLeft": '450px', "marginRight": '520px'}),
    html.Div(id="multi-plot-container"),  # Container for all plots

    # Section of table 
    html.Hr(style={"marginLeft": '430px', "marginRight": '430px'}),
    # html.Hr(),
    html.H3("Summary Table: Total Enrollment by Education Level and Gender", style={"textAlign": "center"}),

    dash_table.DataTable(
        id='summary-table',
        columns=[{"name": i, "id": i} for i in df2_total.columns],
        data=df2_total.to_dict("records"),
        style_table={"overflowX": "auto", "margin": "2px"},
        style_cell={"textAlign": "center", "padding": "2px", "fontFamily": "Arial", "fontSize": 11},
        style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"}
    ), 
],style={"marginBottom": "40px"})

#========================================================================================================
# Callback to update the summary table based on selected filters
@app.callback(
    Output("multi-plot-container", "children"),
    Input("year-checklist", "value"),
    Input("gender-checklist", "value"),
    Input("status-checklist", "value")
)
def update_graphs(selected_years, selected_gender, selected_status):
    # Step 1: Filter df1
    filtered_df = df1[
        df1["Year"].isin(selected_years) &
        df1["Gender"].isin(selected_gender) &
        df1["Study_Status"].isin(selected_status)
    ]

    plots = []
    final_line_figs = []

    for level in ["Undergraduates", "Graduates"]:
        df_sub = filtered_df[filtered_df["Education_Level"] == level]

        # Step 2: Group data
        data1 = df_sub.groupby("Year")["Enrollment"].sum().reset_index()
        data2 = (df_sub.groupby(["Year", "Gender"])["Enrollment"]
            .sum().reset_index())
        # Percentage of women by year
        total_by_year = data2.groupby("Year")["Enrollment"].sum().reset_index(name="Total")
        women_by_year = data2[data2["Gender"] == "Women"].groupby("Year")["Enrollment"].sum().reset_index(name="Women")
        data3 = pd.merge(total_by_year, women_by_year, on="Year", how="left")
        data3["Pct_Women"] = 100 * data3["Women"] / data3["Total"]

        # Step 3: Create line plot
        line_fig = px.line(
            data1,
            x="Year",
            y="Enrollment",
            markers=True,
            title=f"{level} - Total Enrollment Over Years",
            text="Enrollment" # value to be used as number label
        )
        line_fig.update_traces(
            mode='lines+markers+text',      # ensure text is shown
            textposition='top center',      # adjust if needed (try bottom too)
            texttemplate='%{text:,}',       # format with comma
            textfont=dict(size=10)
        )
        # Calculate y-axis range with padding
        y_min = data1["Enrollment"].min() * 0.98
        y_max = data1["Enrollment"].max() * 1.03

        line_fig.update_layout(
            template="plotly_white",
            width=700, height=350,
            margin=dict(t=40, l=100),
            yaxis=dict(range=[y_min, y_max]),  # Set y-axis range
        )

        # Step 4: Create bar plot
        bar_fig = px.bar(
            data2,
            x="Year",
            y="Enrollment",
            color="Gender",
            barmode="group",
            title=f"{level} - Enrollment by Gender"
        )
        bar_fig.update_layout(
            template="plotly_white",
            width=600, height=350,
            margin=dict(t=40)
        )

        # Step 5: Create line plot - Percentage
        line_fig2_w = px.line(
            data3,
            x="Year",
            y="Pct_Women",
            markers=True,
            title=f"{level} - % Women Enrollment by Year",
            text="Pct_Women"  # value to be used as percentage label
        )
        line_fig2_w.update_traces(
            mode='lines+markers+text',      # ensure text is shown
            textposition='top center',      # adjust if needed (try bottom too)
            texttemplate='%{text:.1f}%',     # format as percentage with one decimal
            textfont=dict(size=10)
        )
        line_fig2_w.update_layout(
            yaxis=dict(range=[50, 66]),  # Set y-axis range for percentage
            yaxis_title="Percentage of women (%)")
        final_line_figs.append(line_fig2_w)  # Collect for final display

        # Step 6: Add both plots side by side in one row
        row1 = html.Div([
            dcc.Graph(figure=line_fig, style={"display": "inline-block", "width": "48%"}),
            dcc.Graph(figure=bar_fig, style={"display": "inline-block", "width": "48%"})
        ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "30px"})

        plots.append(row1)

    # Add a section title or horizontal line before percentage plots
    plots.append(html.Hr())
    plots.append(html.H3("Percentage of Female Students Over Years", style={"textAlign": "center", "color": "darkblue"}))

    # Step 7: Callback for percentage line plots
    row_final = html.Div([
        dcc.Graph(figure=final_line_figs[0], style={"display": "inline-block", "width": "48%"}),
        dcc.Graph(figure=final_line_figs[1], style={"display": "inline-block", "width": "48%"})
    ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "40px"})

    plots.append(row_final)

    # Step 8: Return all rows (4+2 plots)
    return plots


# Run server
if __name__ == "__main__":
    app.run(debug=True)

# Note: The app will run on http://127.0.0.1:8050/