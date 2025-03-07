import pandas as pd

def merge_isco_data(automation_file, isco_file, output_file):
    # Read the automation potential file
    df_automation = pd.read_excel(automation_file, dtype={'ISCO-08 (3 digits)': str})
    
    # Read the ISCO-2008-EL file
    df_isco = pd.read_excel(isco_file, dtype={'ISCO-08\nΚώδικας': str})
    
    # Rename columns for easier merging
    df_automation.rename(columns={'ISCO-08 (3 digits)': 'ISCO_Code', 'Automation potential': 'Automation_Potential'}, inplace=True)
    df_isco.rename(columns={'ISCO-08\nΚώδικας': 'ISCO_Code', 'ΠΕΡΙΓΡΑΦΗ': 'Description'}, inplace=True)
    
    # Keep only the necessary columns
    df_isco = df_isco[['ISCO_Code', 'Description']]
    
    # Convert automation potential to integer percentage format
    df_automation['Automation_Potential'] = (df_automation['Automation_Potential'] * 100).round().astype(int)
    
    # Merge the two dataframes on ISCO_Code
    merged_df = pd.merge(df_automation, df_isco, on='ISCO_Code', how='left')
    
    # Reorder columns
    merged_df = merged_df[['ISCO_Code', 'Description', 'Automation_Potential']]
    
    # Save to Excel
    merged_df.to_excel(output_file, index=False)
    
    print(f"Merged file saved as {output_file}")

merge_isco_data("automation_potential_fixed_ISCO08.xlsx", "ISCO-2008-EL.xls", "merged_ISCO_automation.xlsx")
