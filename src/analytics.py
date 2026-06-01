import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

def run_analytics():
    print("\n" + "="*35)
    print(" ACADEMY-OPS ANALYTICS ENGINE ")
    print("="*35)
    
    try:
        with sqlite3.connect('academyops.db') as conn:
            df = pd.read_sql_query("SELECT * FROM leads", conn)
    except Exception as e:
        print(f"[x] Database error: {e}")
        return

    if df.empty:
        print("[!] No leads found in the database. Cannot run analytics.")
        return

    # 1. Pipeline Stage Counts
    print("\n--- 1. Pipeline Stage Counts ---")
    stage_order = ['New', 'Contacted', 'Qualified', 'Demo', 'Enrolled', 'Lost']
    counts = df['stage'].value_counts().reindex(stage_order, fill_value=0)
    for stage, count in counts.items():
        print(f" {stage}: {count}")

    # 2. Hypothesis Test
    print("\n--- 2. Source Conversion Analysis ---")
    print("Null Hypothesis: Lead source does not affect the conversion rate.")
    
    df['is_enrolled'] = df['stage'] == 'Enrolled'
    contingency = pd.crosstab(df['source'], df['is_enrolled'])
    
    if contingency.size > 0 and contingency.shape == (2, 2):
        chi2, p_val, dof, expected = chi2_contingency(contingency)
        print(f"P-Value: {p_val:.4f}")
        if p_val < 0.05:
            print("Conclusion: Reject null hypothesis. Source statistically affects conversion.")
        else:
            print("Conclusion: Cannot reject null hypothesis.")
    else:
        print("Conclusion: Not enough variance in our small test dataset to run a Chi-Square test yet.")

    # 3. Generate Visual Charts
    print("\n--- 3. Generating Visual Charts ---")
    
    # Funnel Chart
    plt.figure(figsize=(8, 5))
    counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Lead Pipeline Funnel')
    plt.xlabel('Stage')
    plt.ylabel('Number of Leads')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/funnel_chart.png')
    print("[+] Saved funnel chart to data/funnel_chart.png")

    # Source Pie Chart
    plt.figure(figsize=(8, 5))
    df['source'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral', 'gold'])
    plt.title('Leads by Source')
    plt.ylabel('')
    plt.savefig('data/source_chart.png')
    print("[+] Saved source pie chart to data/source_chart.png")
    
    print("="*35 + "\n")

if __name__ == '__main__':
    run_analytics()