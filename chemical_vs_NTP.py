# NTP vs Chemical engines comparisons
# AE 267 Group 8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_data():
    """Load the rocket engine data from CSV file."""
    return pd.read_csv('rocket_engines.csv')

def create_category_comparison(df):
    """Create separate comparison plots for Chemical vs NTP engines."""
    category_medians = df.groupby('Category').agg({
        'ISP (s)': 'median',
        'Thrust-to-Weight': 'median',
        'Vacuum Thrust (kN)': 'median',
        'Fuel Cost (USD)': 'median'
    }).reset_index()
    
    category_medians['Fuel Cost (k USD)'] = category_medians['Fuel Cost (USD)'] / 1000
    
    metrics = ['ISP (s)', 'Thrust-to-Weight', 'Vacuum Thrust (kN)', 'Fuel Cost (k USD)']
    titles = ['ISP', 'Thrust-to-Weight Ratio', 'Vacuum Thrust', 'Fuel Cost']
    ylabels = ['ISP (s)', 'Thrust-to-Weight', 'Thrust (kN)', 'Cost (k USD)']
    
    for metric, title, ylabel in zip(metrics, titles, ylabels):
        plt.figure(figsize=(8, 6))
        ax = sns.barplot(data=category_medians, x='Category', y=metric)
        plt.title(f'Median {title}: Chemical vs NTP Engines')
        plt.ylabel(ylabel)
        
        for i, bar in enumerate(ax.patches):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                    f'{bar.get_height():.1f}',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'category_comparison_{metric.lower().replace(" ", "_")}.png')
        plt.close()

def create_comparison_plots(df):
    """Create comparison plots for different engine parameters."""
    plt.style.use('default')
    
    # 1. Bar plot of ISP by engine (sorted)
    plt.figure(figsize=(8, 6))
    sorted_df = df.sort_values('ISP (s)', ascending=False)
    ax = sns.barplot(data=sorted_df, x='ISP (s)', y='Engine')
    plt.title('ISP by Engine')
    # Add ISP value labels
    for i, bar in enumerate(ax.patches):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                f'{sorted_df.iloc[i]["ISP (s)"]:.1f}',
                ha='left', va='center')
    plt.tight_layout()
    plt.savefig('isp_by_engine.png')
    plt.close()
    
    # 2. Bar plot of Thrust-to-Weight by engine (sorted)
    plt.figure(figsize=(8, 6))
    sorted_df = df.sort_values('Thrust-to-Weight', ascending=False)
    ax = sns.barplot(data=sorted_df, x='Thrust-to-Weight', y='Engine')
    plt.title('Thrust-to-Weight Ratio by Engine')
    # Add Thrust-to-Weight value labels
    for i, bar in enumerate(ax.patches):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
                f'{sorted_df.iloc[i]["Thrust-to-Weight"]:.1f}',
                ha='left', va='center')
    plt.tight_layout()
    plt.savefig('thrust_weight_by_engine.png')
    plt.close()

def print_statistics(df):
    """Print statistical analysis of the data."""
    print("\nRocket Engine Analysis Summary:")
    print("-" * 50)
    print("\nBasic Statistics:")
    print(df.describe())
    print("\nCategory-wise Analysis:")
    print(df.groupby('Category').agg({
        'ISP (s)': ['mean', 'max'],
        'Thrust-to-Weight': ['mean', 'max'],
        'Fuel Cost (USD)': ['mean', 'min']
    }))
    
    # Cost efficiency analysis
    #df['Cost_per_Thrust'] = df['Fuel Cost (USD)'] / df['Vacuum Thrust (kN)']
    #plt.figure(figsize=(10, 6))
    #cost_efficiency_data = df[['Engine', 'Cost_per_Thrust']].sort_values('Cost_per_Thrust')
    #plt.bar(cost_efficiency_data['Engine'], cost_efficiency_data['Cost_per_Thrust'])
    #plt.yscale('log')
    #plt.xticks(rotation=45, ha='right')
    #plt.xlabel('Engine')
    #plt.ylabel('Cost per Thrust (USD/kN)')
    #plt.title('Cost Efficiency (USD per kN of thrust)')

    #for i, v in enumerate(cost_efficiency_data['Cost_per_Thrust']):
    #    plt.text(i, v, f'${v:,.0f}', ha='center', va='bottom')
    
    #plt.tight_layout()
    
    #plt.savefig('cost_efficiency_chart.png', bbox_inches='tight', dpi=300)
    #plt.close()

    # Cost efficiency analysis
    plt.figure(figsize=(10, 6))
    thrust_data = df[['Engine', 'Vacuum Thrust (kN)']].sort_values('Vacuum Thrust (kN)', ascending=False)
    plt.bar(thrust_data['Engine'], thrust_data['Vacuum Thrust (kN)'])
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Engine')
    plt.ylabel('Vacuum Thrust (kN)')
    plt.title('Total Thrust by Engine')

    for i, v in enumerate(thrust_data['Vacuum Thrust (kN)']):
        plt.text(i, v, f'{v:,.0f} kN', ha='center', va='bottom')
    
    plt.tight_layout()
    
    plt.savefig('engine_thrust_comparison.png', bbox_inches='tight', dpi=300)
    plt.close()

def create_fuel_cost_vs_thrust_plot(df):
    """Create a scatter plot comparing fuel cost vs vacuum thrust for NTP engines."""
    # Filter for NTP engines
    ntp_df = df[df['Category'] == 'NTP']
    
    plt.figure(figsize=(10, 6))
    plt.scatter(ntp_df['Vacuum Thrust (kN)'], ntp_df['Fuel Cost (USD)'] / 1000, 
                s=100, alpha=0.7)
    
    # Add labels for each point
    for i, row in ntp_df.iterrows():
        plt.annotate(row['Engine'], 
                    (row['Vacuum Thrust (kN)'], row['Fuel Cost (USD)'] / 1000),
                    xytext=(5, 5), textcoords='offset points')
    
    plt.xlabel('Vacuum Thrust (kN)')
    plt.ylabel('Fuel Cost (k USD)')
    plt.title('NTP Engines: Fuel Cost vs Vacuum Thrust')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('ntp_fuel_cost_vs_thrust.png')
    plt.close()

def create_total_fuel_cost_plot(df):
    """Bar chart showing total fuel cost for each engine."""
    plt.figure(figsize=(12, 6))

    # Filter out Apollo SPS AJ10-137
    fuel_cost_data = df[df['Engine'] != 'Apollo SPS (AJ10-137)'][['Engine', 'Fuel Cost (USD)']].sort_values('Fuel Cost (USD)', ascending=False)

    plt.bar(fuel_cost_data['Engine'], fuel_cost_data['Fuel Cost (USD)'] / 1000)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Engine')
    plt.ylabel('Total Fuel Cost (k USD)')
    plt.title('Total Fuel Cost by Engine')

    for i, v in enumerate(fuel_cost_data['Fuel Cost (USD)']):
        plt.text(i, v/1000, f'${v/1000:,.0f}k', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('total_fuel_cost.png', bbox_inches='tight', dpi=300)
    plt.close()


def create_engines_table(df):
    """Create a pretty table of engines organized by category."""
    # Select and organize columns
    table_df = df[['Engine', 'Category']]
    
    # Sort by category and then by engine name
    table_df = table_df.sort_values(['Category', 'Engine'])
    
    # Create a figure with a specific size
    plt.figure(figsize=(8, len(table_df) * 0.4 + 2))
    
    # Hide axes
    plt.axis('off')
    
    # Create the table
    table = plt.table(
        cellText=table_df.values,
        colLabels=table_df.columns,
        cellLoc='center',
        loc='center',
        colColours=['#f2f2f2'] * len(table_df.columns),
        cellColours=[['#ffffff' if i % 2 == 0 else '#f8f8f8'] * len(table_df.columns) for i in range(len(table_df))],
        edges='horizontal'
    )
    
    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    
    # Add title
    plt.title('Rocket Engines', pad=20, fontsize=14)
    
    # Save the table
    plt.tight_layout()
    plt.savefig('engines_comparison_table.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    df = load_data()
    
    create_comparison_plots(df)
    create_category_comparison(df)
    create_fuel_cost_vs_thrust_plot(df)
    create_engines_table(df)
    create_total_fuel_cost_plot(df)
    print_statistics(df)

if __name__ == "__main__":
    main() 