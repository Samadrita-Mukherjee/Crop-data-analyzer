# Simple Crop Yield Analysis - Indian States Dataset
# Step-by-Step Code with 5 Essential Charts

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# STEP 1: IMPORT & LOAD DATA
# =============================================================================

print("Step 1: Loading Data...")

# Load the dataset
df = pd.read_csv('crop_yield.csv')  

# Basic data check
print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset Info:")
print(df.info())
print("\nNull values:")
print(df.isnull().sum())

# =============================================================================
# STEP 2: DATA CLEANING / PREPARATION
# =============================================================================

print("\nStep 2: Data Cleaning...")

# Check data types
print("Current data types:")
print(df.dtypes)

# Convert Year to integer if needed  
if 'Crop_Year' in df.columns:
    df['Year'] = df['Crop_Year'].astype(int)
elif 'Year' in df.columns:
    df['Year'] = df['Year'].astype(int)

# Convert categorical columns
categorical_cols = ['State', 'Crop', 'Season']
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype('category')

# Set pandas groupby behavior to avoid warnings
pd.set_option('future.no_silent_downcasting', True)

# Handle outliers - remove rows with zero production but positive area
if 'Area' in df.columns and 'Production' in df.columns:
    outliers = df[(df['Area'] > 0) & (df['Production'] == 0)]
    print(f"Found {len(outliers)} outliers (Area > 0 but Production = 0)")
    df = df[~((df['Area'] > 0) & (df['Production'] == 0))]

print(f"Clean dataset shape: {df.shape}")

# =============================================================================
# STEP 3: 5 ESSENTIAL CHARTS
# =============================================================================

print("\nStep 3: Creating 5 Essential Charts...")

# CHART 1: Line Plot - Yield Trend Over Years
print("\nChart 1: Yield Trend Over Years (Line Plot)")

if 'Year' in df.columns and 'Yield' in df.columns:
    yearly_yield = df.groupby('Year', observed=True)['Yield'].mean()
    
    plt.figure(figsize=(12, 6))
    plt.plot(yearly_yield.index, yearly_yield.values, marker='o', linewidth=2, markersize=6, color='green')
    plt.title('Average Crop Yield Trend Over Years (1997-2020)', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('Average Yield (tons per hectare)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# CHART 2: Bar Chart - Top 10 States by Yield
print("\nChart 2: Top States by Yield (Bar Chart)")

if 'State' in df.columns and 'Yield' in df.columns:
    top_states_yield = df.groupby('State', observed=True)['Yield'].mean().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(top_states_yield)), top_states_yield.values, color='skyblue', edgecolor='navy')
    plt.title('Top 10 States by Average Yield', fontsize=14)
    plt.xlabel('States')
    plt.ylabel('Average Yield (tons per hectare)')
    plt.xticks(range(len(top_states_yield)), top_states_yield.index, rotation=45)
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

# CHART 3: Pie Chart - Seasonal Distribution
print("\nChart 3: Seasonal Distribution (Pie Chart)")

if 'Season' in df.columns and 'Yield' in df.columns:
    seasonal_yield = df.groupby('Season', observed=True)['Yield'].mean()
    
    plt.figure(figsize=(14, 8))
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'orange']
    
    # Create pie chart WITHOUT labels and percentages on the pie
    wedges, texts = plt.pie(seasonal_yield.values, 
                           startangle=90, 
                           colors=colors[:len(seasonal_yield)])
    
    plt.title('Average Yield Distribution by Season', fontsize=16, pad=20)
    plt.axis('equal')
    
    # Create legend on the side with season names and percentages
    total = sum(seasonal_yield.values)
    legend_labels = []
    for season, value in seasonal_yield.items():
        percentage = (value/total) * 100
        legend_labels.append(f'{season}: {percentage:.1f}%')
    
    plt.legend(wedges, legend_labels, 
              title="Seasons & Percentages",
              loc="center left", 
              bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=12)
    
    plt.tight_layout()
    plt.show()

# CHART 4: Scatter Plot - Rainfall vs Yield
print("\nChart 4: Rainfall vs Yield Relationship (Scatter Plot)")

if 'Annual_Rainfall' in df.columns and 'Yield' in df.columns:
    plt.figure(figsize=(12, 8))
    plt.scatter(df['Annual_Rainfall'], df['Yield'], alpha=0.6, color='blue', s=30)
    plt.title('Annual Rainfall vs Crop Yield', fontsize=14)
    plt.xlabel('Annual Rainfall (mm)')
    plt.ylabel('Crop Yield (tons per hectare)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    # Calculate and show correlation
    correlation = df['Annual_Rainfall'].corr(df['Yield'])
    print(f"Correlation between Annual Rainfall and Yield: {correlation:.3f}")

# CHART 5: Heatmap - Correlation Between Variables
print("\nChart 5: Correlation Heatmap")

# Select only numeric columns for correlation
numeric_cols = df.select_dtypes(include=['int64', 'float64'])

if len(numeric_cols.columns) > 1:
    plt.figure(figsize=(10, 8))
    correlation_matrix = numeric_cols.corr()
    
    # Create heatmap
    sns.heatmap(correlation_matrix, 
                annot=True,           # Show correlation numbers
                cmap='RdYlBu_r',     # Color scheme
                center=0,             # Center at 0
                square=True,          # Make squares
                fmt='.2f')           # Show 2 decimal places
    
    plt.title('Correlation Heatmap - Relationships Between Variables', fontsize=14)
    plt.tight_layout()
    plt.show()

# =============================================================================
# STEP 4: SUMMARY STATISTICS
# =============================================================================

print("\nStep 4: Summary Statistics...")

print("Dataset Summary:")
print(df.describe())

if 'State' in df.columns:
    print(f"\nNumber of States/UTs: {df['State'].nunique()}")

if 'Crop' in df.columns:
    print(f"Number of Different Crops: {df['Crop'].nunique()}")

if 'Year' in df.columns:
    print(f"Years covered: {df['Year'].min()} to {df['Year'].max()}")

print(f"Total records: {len(df)}")

# Key insights
print("\n=== KEY INSIGHTS ===")
if 'State' in df.columns and 'Yield' in df.columns:
    best_state = df.groupby('State', observed=True)['Yield'].mean().idxmax()
    best_yield = df.groupby('State', observed=True)['Yield'].mean().max()
    print(f"Best performing state: {best_state} (Yield: {best_yield:.2f})")

if 'Season' in df.columns and 'Production' in df.columns:
    best_season = df.groupby('Season', observed=True)['Production'].sum().idxmax()
    print(f"Most productive season: {best_season}")

if 'Annual_Rainfall' in df.columns and 'Yield' in df.columns:
    rainfall_corr = df['Annual_Rainfall'].corr(df['Yield'])
    if rainfall_corr > 0.3:
        print("✓ Rainfall has a positive impact on crop yield")
    elif rainfall_corr < -0.3:
        print("✓ Too much rainfall may reduce crop yield")
    else:
        print("✓ Rainfall has minimal impact on crop yield")

print("\n=== ANALYSIS COMPLETE ===")
print("5 essential charts created successfully!")
