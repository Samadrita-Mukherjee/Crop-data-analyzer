import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Crop Yield Dashboard", page_icon="🌾", layout="wide")

# Title
st.title("🌾 Crop Yield Analysis Dashboard")
st.markdown("### Indian States Dataset (1997-2020)")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('crop_yield.csv')
    
    # Convert Year
    if 'Crop_Year' in df.columns:
        df['Year'] = df['Crop_Year'].astype(int)
    
    # Clean outliers
    if 'Area' in df.columns and 'Production' in df.columns:
        df = df[~((df['Area'] > 0) & (df['Production'] == 0))]
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# State filter
states = ['All States'] + sorted(df['State'].unique().tolist())
selected_state = st.sidebar.selectbox("Select State", states)

# Crop filter
crops = ['All Crops'] + sorted(df['Crop'].unique().tolist())
selected_crop = st.sidebar.selectbox("Select Crop", crops)

# Season filter
seasons = ['All Seasons'] + sorted(df['Season'].unique().tolist())
selected_season = st.sidebar.selectbox("Select Season", seasons)

# Year range filter
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Apply filters
filtered_df = df.copy()

if selected_state != 'All States':
    filtered_df = filtered_df[filtered_df['State'] == selected_state]

if selected_crop != 'All Crops':
    filtered_df = filtered_df[filtered_df['Crop'] == selected_crop]

if selected_season != 'All Seasons':
    filtered_df = filtered_df[filtered_df['Season'] == selected_season]

filtered_df = filtered_df[(filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])]

# Display summary statistics
st.subheader("📊 Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(filtered_df))

with col2:
    avg_yield = filtered_df['Yield'].mean()
    st.metric("Average Yield", f"{avg_yield:.2f}")

with col3:
    total_production = filtered_df['Production'].sum()
    st.metric("Total Production", f"{total_production:,.0f}")

with col4:
    total_area = filtered_df['Area'].sum()
    st.metric("Total Area", f"{total_area:,.0f}")

st.markdown("---")

# CHART 1: Line Plot - Yield Trend Over Years
st.subheader("📈 Chart 1: Yield Trend Over Years")

if len(filtered_df) > 0:
    yearly_yield = filtered_df.groupby('Year')['Yield'].mean()
    
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(yearly_yield.index, yearly_yield.values, marker='o', linewidth=2, markersize=6, color='green')
    ax1.set_title('Average Crop Yield Trend Over Years', fontsize=14)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Average Yield (tons per hectare)')
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig1)
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# CHART 2: Bar Chart - Top 10 States by Yield
st.subheader("📊 Chart 2: Top 10 States by Average Yield")

if len(filtered_df) > 0 and selected_state == 'All States':
    top_states_yield = filtered_df.groupby('State')['Yield'].mean().sort_values(ascending=False).head(10)
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    bars = ax2.bar(range(len(top_states_yield)), top_states_yield.values, color='skyblue', edgecolor='navy')
    ax2.set_title('Top 10 States by Average Yield', fontsize=14)
    ax2.set_xlabel('States')
    ax2.set_ylabel('Average Yield (tons per hectare)')
    ax2.set_xticks(range(len(top_states_yield)))
    ax2.set_xticklabels(top_states_yield.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig2)
elif selected_state != 'All States':
    st.info("💡 Select 'All States' to view state comparison.")
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# CHART 3: Pie Chart - Seasonal Distribution
st.subheader("🥧 Chart 3: Seasonal Distribution")

if len(filtered_df) > 0:
    seasonal_yield = filtered_df.groupby('Season')['Yield'].mean()
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'orange']
    
    wedges, texts = ax3.pie(seasonal_yield.values, 
                           startangle=90, 
                           colors=colors[:len(seasonal_yield)])
    
    ax3.set_title('Average Yield Distribution by Season', fontsize=14)
    ax3.axis('equal')
    
    # Create legend
    total = sum(seasonal_yield.values)
    legend_labels = []
    for season, value in seasonal_yield.items():
        percentage = (value/total) * 100
        legend_labels.append(f'{season}: {percentage:.1f}%')
    
    ax3.legend(wedges, legend_labels, 
              title="Seasons & Percentages",
              loc="center left", 
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=10)
    
    plt.tight_layout()
    st.pyplot(fig3)
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# CHART 4: Scatter Plot - Rainfall vs Yield
st.subheader("💧 Chart 4: Rainfall vs Yield Relationship")

if len(filtered_df) > 0:
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    ax4.scatter(filtered_df['Annual_Rainfall'], filtered_df['Yield'], alpha=0.6, color='blue', s=30)
    ax4.set_title('Annual Rainfall vs Crop Yield', fontsize=14)
    ax4.set_xlabel('Annual Rainfall (mm)')
    ax4.set_ylabel('Crop Yield (tons per hectare)')
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig4)
    
    # Calculate and show correlation
    correlation = filtered_df['Annual_Rainfall'].corr(filtered_df['Yield'])
    st.info(f"📊 Correlation between Annual Rainfall and Yield: **{correlation:.3f}**")
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# CHART 5: Heatmap - Correlation Between Variables
st.subheader("🔥 Chart 5: Correlation Heatmap")

if len(filtered_df) > 0:
    numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64'])
    
    fig5, ax5 = plt.subplots(figsize=(10, 8))
    correlation_matrix = numeric_cols.corr()
    
    sns.heatmap(correlation_matrix, 
                annot=True,
                cmap='RdYlBu_r',
                center=0,
                square=True,
                fmt='.2f',
                ax=ax5)
    
    ax5.set_title('Correlation Heatmap - Relationships Between Variables', fontsize=14)
    plt.tight_layout()
    st.pyplot(fig5)
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

# Key Insights Section
st.subheader("💡 Key Insights")

if len(filtered_df) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Best Performing State:**")
        best_state = filtered_df.groupby('State')['Yield'].mean().idxmax()
        best_yield = filtered_df.groupby('State')['Yield'].mean().max()
        st.success(f"🏆 {best_state} (Yield: {best_yield:.2f})")
        
        st.write("**Most Productive Season:**")
        best_season = filtered_df.groupby('Season')['Production'].sum().idxmax()
        st.success(f"🌸 {best_season}")
    
    with col2:
        st.write("**Top Crop by Yield:**")
        best_crop = filtered_df.groupby('Crop')['Yield'].mean().idxmax()
        best_crop_yield = filtered_df.groupby('Crop')['Yield'].mean().max()
        st.success(f"🌾 {best_crop} (Yield: {best_crop_yield:.2f})")
        
        st.write("**Rainfall Impact:**")
        rainfall_corr = filtered_df['Annual_Rainfall'].corr(filtered_df['Yield'])
        if rainfall_corr > 0.3:
            st.success("✓ Rainfall has a positive impact on crop yield")
        elif rainfall_corr < -0.3:
            st.warning("⚠ Too much rainfall may reduce crop yield")
        else:
            st.info("ℹ Rainfall has minimal impact on crop yield")
else:
    st.warning("No data available for the selected filters.")

# Footer
st.markdown("---")
st.markdown("### 📚 About This Dashboard")
st.write("This interactive dashboard analyzes crop yield data from Indian states (1997-2020).")
st.write("Use the sidebar filters to explore different states, crops, seasons, and time periods.")
