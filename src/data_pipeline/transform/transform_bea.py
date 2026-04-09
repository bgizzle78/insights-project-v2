# Imports
import pandas as pd
from src.config import BEA_PROCESSED_PATH, BEA_FINAL_PATH, START_YEAR, END_YEAR
from src.utils import save_csv, map_bea_industries


# Load processed data
def load_processed_data() -> pd.DataFrame:
    """Load the processed BEA CSV file."""
    try:
        df = pd.read_csv(BEA_PROCESSED_PATH)
        print(f"Loaded {len(df)} rows from {BEA_PROCESSED_PATH}")
        return df
    except FileNotFoundError:
        print(f"File not found: {BEA_PROCESSED_PATH}")
        raise

# Reshape data
def reshape_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    """Convert wide-format BEA data to long format (years as rows)."""
    year_cols = [col for col in df.columns if col.isdigit() and START_YEAR <= int(col) <= END_YEAR]

    df_long = df.melt(
        id_vars=['geo_name', 'line_code', 'industry_classification', 'description'],
        value_vars=year_cols,
        var_name='year',
        value_name='gdp'
    )

    df_long['year'] = df_long['year'].astype(int)
    df_long['gdp'] = pd.to_numeric(df_long['gdp'], errors='coerce')

    print(f"Reshaped to long format: {len(df_long)} rows")
    return df_long

# Filter year range
def filter_years(df: pd.DataFrame) -> pd.DataFrame:
    """Filter BEA data to START_YEAR-END_YEAR."""
    df_filtered = df[(df['year'] >= START_YEAR) & (df['year'] <= END_YEAR)]
    print(f"Filtered years {START_YEAR}-{END_YEAR}: {len(df_filtered)} rows remain")
    return df_filtered

# Map BEA industries
def map_industries(df: pd.DataFrame) -> pd.DataFrame:
    """Map BEA industry descriptions to standardized categories."""
    df = map_bea_industries(df, column='description')
    print("Mapped BEA industry descriptions to standardized industries")
    return df

# Filter + aggregate to top-level industries
def filter_and_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only top-level industries and aggregate GDP per year."""
    
    # Remove sub-industries
    df = df[df['industry'] != 'Other / Unknown']
    print(f"Filtered out sub-industries: {len(df)} rows remain")

    # Aggregate GDP by year + industry
    df_agg = (
        df.groupby(['year', 'industry'], as_index=False)['gdp']
          .sum()
    )

    print("Aggregated GDP to one value per industry per year")
    return df_agg

# Save final dataset
def save_final(df: pd.DataFrame):
    """Save the transformed BEA GDP data to final CSV."""
    save_csv(df, BEA_FINAL_PATH)
    print(f"Saved final BEA data to {BEA_FINAL_PATH}")

# Main pipeline
def main():
    df = load_processed_data()
    df = reshape_wide_to_long(df)
    df = filter_years(df)      
    df = map_industries(df)
    df = filter_and_aggregate(df)
    save_final(df)
    print("BEA transform pipeline completed successfully!")

# Run script
if __name__ == "__main__":
    main()