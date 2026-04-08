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
    """Filter BEA data to START_YEAR–END_YEAR."""
    df_filtered = df[(df['year'] >= START_YEAR) & (df['year'] <= END_YEAR)]
    print(f"Filtered years {START_YEAR}-{END_YEAR}: {len(df_filtered)} rows remain")
    return df_filtered


# Map BEA industries
def map_industries(df: pd.DataFrame) -> pd.DataFrame:
    """Map BEA industry descriptions to standardized categories."""
    df = map_bea_industries(df, column='description')
    print("Mapped BEA industry descriptions to standardized industries")
    return df


# Filter out sub-industries
def filter_top_level_industries(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only mapped top-level industries (drop 'Other / Unknown')."""
    initial_rows = len(df)
    df = df[df['industry'] != 'Other / Unknown']
    print(f"Filtered sub-industries: {initial_rows - len(df)} rows removed, {len(df)} rows remain")
    return df


def aggregate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate GDP by year and top-level industry. Returns a DataFrame with one row per year per industry."""
    print("Aggregating GDP by year and top-level industry...")

    # Sum GDP per year + industry
    gdp_by_industry = (
        df.groupby(['year', 'industry'], as_index=False)['gdp']
          .sum()
          .rename(columns={'gdp': 'industry_gdp'})
    )

    # Total GDP per year
    total_gdp = (
        gdp_by_industry.groupby('year', as_index=False)['industry_gdp']
        .sum()
        .rename(columns={'industry_gdp': 'total_gdp'})
    )

    # Merge total back to calculate % of total GDP
    gdp_by_industry = gdp_by_industry.merge(total_gdp, on='year', how='left')
    gdp_by_industry['pct_total_gdp'] = gdp_by_industry['industry_gdp'] / gdp_by_industry['total_gdp'] * 100

    print("Aggregation complete: one row per year per top-level industry")
    return gdp_by_industry, total_gdp


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
    df = filter_top_level_industries(df)
    gdp_by_industry, total_gdp = aggregate_metrics(df)

    # Keep only clean, analysis-ready columns
    df = df[['geo_name', 'year', 'industry', 'gdp']]

    save_final(gdp_by_industry)
    print("BEA transform pipeline completed successfully!")


# Run script
if __name__ == "__main__":
    main()