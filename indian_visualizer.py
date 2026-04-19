import pandas as pd
import plotly.express as px

# 1. Load Data
df = pd.read_csv("india_heatmap_data.csv")

if df.empty:
    print("No data found.")
    exit()

# 2. The "Atlas" Configuration
fig = px.scatter_geo(
    df,
    lat="Lat",
    lon="Long",
    size="news_count",
    
    # LABELING
    text="State",
    hover_name="State",
    
    # DATA INJECTION
    hover_data={"headlines": True, "Lat": False, "Long": False, "news_count": True},
    
    title="India News Atlas (Live)",
    projection="mercator",
    
    # We remove the dark template for a clean white look
    template="plotly_white", 
    
    # COLORS: A Scale that looks good on Beige (Red-Orange-Yellow)
    color="news_count",
    color_continuous_scale="Reds",
    size_max=35
)

# 3. "Actual Map Colors" (The Geographic Look)
fig.update_geos(
    visible=True,
    fitbounds="locations", # Auto-Zoom to India
    
    # The Palette
    showcountries=True, countrycolor="#888888", # Grey international borders
    showsubunits=True, subunitcolor="#FFFFFF",   # White state borders
    
    showland=True, landcolor="#EAE0D0",     # <--- CLASSIC BEIGE LAND
    showocean=True, oceancolor="#A3C6D4",   # <--- REALISTIC BLUE OCEAN
    showlakes=True, lakecolor="#A3C6D4",
    
    projection_type="mercator"
)

# 4. Refined Interaction (The "Dropdown" Effect)
fig.update_traces(
    marker=dict(
        opacity=0.8, 
        line=dict(width=1, color="#333333") # Dark rim around bubbles
    ),
    
    # TEXT LABELS
    textposition="top center",
    textfont=dict(family="Arial", size=10, color="black"), # Black text for visibility
    
    # THE HOVER BOX (This effectively acts as your dropdown)
    # The <br> tags we added in the processor will make this a vertical list
    hovertemplate="<b>%{hovertext}</b><br>" +
                  "<i>Stories: %{marker.size}</i><br>" +
                  "<hr>" + # A horizontal line separator
                  "%{customdata[0]}" + 
                  "<extra></extra>"
)

# 5. Final Layout Polish
fig.update_layout(
    margin={"r":0,"t":50,"l":0,"b":0},
    title_font_size=20,
    
    # Hover Label Styling (Make it look like a document)
    hoverlabel=dict(
        bgcolor="white", 
        font_size=12, 
        font_family="Arial",
        align="left" # Left-align the headlines for readability
    )
)

fig.show()