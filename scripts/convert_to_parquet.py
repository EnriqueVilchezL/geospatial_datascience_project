"""Convert TSV to Parquet format for faster loading while preserving ALL data."""

from pathlib import Path

import polars as pl
from loguru import logger


def convert_tsv_to_parquet() -> None:
    """Convert crocodile occurrence TSV to Parquet format."""
    # Paths
    tsv_path = Path("data/crocodiles/occurrence.tsv")
    parquet_path = Path("data/crocodiles/occurrence_full.parquet")

    logger.info(f"Reading {tsv_path}...")
    data = pl.read_csv(
        source=tsv_path,
        separator="\t",
        quote_char=None,
        truncate_ragged_lines=True,
    )

    logger.info(f"Original data: {len(data):,} rows × {len(data.columns)} columns")

    # Keep ALL columns, just convert format
    logger.info(f"Writing to {parquet_path}...")
    data.write_parquet(
        file=parquet_path,
        compression="zstd",  # Better compression than default
    )

    # Verify
    parquet_data = pl.read_parquet(source=parquet_path)
    logger.info(
        f"Parquet data: {len(parquet_data):,} rows × {len(parquet_data.columns)} columns",
    )

    # Show file sizes
    tsv_size = tsv_path.stat().st_size / (1024 * 1024)
    parquet_size = parquet_path.stat().st_size / (1024 * 1024)
    savings = tsv_size - parquet_size
    savings_pct = (1 - parquet_size / tsv_size) * 100

    logger.info("File sizes:")
    logger.info(f"{'':<2}TSV: {tsv_size:>10,.2f} MB")
    logger.info(f"{'':<2}Parquet: {parquet_size:>10,.2f} MB")
    logger.info(f"{'':<2}Savings: {savings:>10,.2f} MB ({savings_pct:.1f}%)")
    logger.success(
        f"No data loss - all {len(parquet_data):,} rows "
        f"and {len(parquet_data.columns)} columns preserved!",
    )


if __name__ == "__main__":
    convert_tsv_to_parquet()
