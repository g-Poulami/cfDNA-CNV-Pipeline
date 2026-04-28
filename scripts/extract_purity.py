import pandas as pd
import sys
import os

def extract_purity(params_file):
    """
    Extracts the 'nethct' (tumor fraction) from ichorCNA params file.
    Takes the solution with the highest log-likelihood (first row).
    """
    if not os.path.exists(params_file):
        raise FileNotFoundError(f"Could not find {params_file}")
        
    df = pd.read_csv(params_file, sep='\t')
    
    # ichorCNA typically names the purity column 'nethct' or 'TF'
    purity_col = 'nethct' if 'nethct' in df.columns else 'TF'
    
    purity = df.iloc[0][purity_col]
    return round(float(purity), 4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("0.1") # Default fallback
    else:
        try:
            print(extract_purity(sys.argv[1]))
        except:
            print("0.1")
