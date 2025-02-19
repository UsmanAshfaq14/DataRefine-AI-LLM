import pandas as pd
import numpy as np
from typing import Dict, Union, List, Tuple
import json
from io import StringIO
import sys
sys.stdout.reconfigure(encoding='utf-8')

class DataRefineAI:
    def __init__(self):
        self.validation_report = {
            "data_overview": {"total_rows": 0, "total_columns": 0},
            "missing_data": {
                "numeric_fields_missing": 0,
                "categorical_fields_missing": 0,
                "columns_with_missing": [],
                "interpolation_details": []  # Added this field
            },
            "duplicate_records": {
                "total_duplicates": 0,
                "conflicting_records": 0
            },
            "normalization": {
                "text_fields": False,
                "numeric_fields": False
            },
            "final_status": {
                "rows_after_cleaning": 0,
                "columns_after_cleaning": 0
            }
        }

    def load_data(self, data: str) -> pd.DataFrame:
        """Load data from CSV string into pandas DataFrame."""
        return pd.read_csv(StringIO(data), skipinitialspace=True)

    def detect_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """Detect and categorize column data types."""
        data_types = {}
        for column in df.columns:
            if column == 'age':
                data_types[column] = 'numeric'
            elif column == 'name':
                data_types[column] = 'categorical'
            else:
                data_types[column] = 'id'
        return data_types

    def calculate_interpolation(self, series: pd.Series, index: int) -> Dict:
        """Calculate interpolation details for a specific missing value."""
        # Find the nearest non-null values before and after the missing value
        before_mask = series.notna()[:index]
        after_mask = series.notna()[index:]
        
        if before_mask.any() and after_mask.any():
            left_idx = before_mask.index[before_mask][-1]
            right_idx = after_mask.index[after_mask][0]
            left_val = series[left_idx]
            right_val = series[right_idx]
            
            # Calculate interpolated value
            position_ratio = (index - left_idx) / (right_idx - left_idx)
            interpolated_value = left_val + (right_val - left_val) * position_ratio
            
            return {
                "missing_index": index,
                "left_value": left_val,
                "right_value": right_val,
                "left_index": left_idx,
                "right_index": right_idx,
                "interpolated_value": round(interpolated_value, 2),
                "calculation": f"Value_{left_val} + ({right_val} - {left_val}) × ({index} - {left_idx})/({right_idx} - {left_idx})"
            }
        return None

    def interpolate_numeric(self, series: pd.Series) -> Tuple[pd.Series, List[Dict]]:
        """Interpolate missing numeric values and return interpolation details."""
        interpolation_details = []
        
        # Get indices of missing values
        missing_indices = series[series.isna()].index
        
        # Calculate interpolation details for each missing value
        for idx in missing_indices:
            details = self.calculate_interpolation(series, idx)
            if details:
                interpolation_details.append(details)
        
        # Perform the interpolation
        interpolated_series = series.interpolate(method='linear')
        
        return interpolated_series, interpolation_details

    def fill_categorical(self, series: pd.Series) -> pd.Series:
        """Fill missing categorical values with mode or 'Unknown'."""
        mode = series.mode()
        if len(mode) > 0:
            return series.fillna(mode[0])
        return series.fillna('Unknown')

    def normalize_text(self, series: pd.Series) -> pd.Series:
        """Normalize text fields to consistent case."""
        return series.str.lower() if isinstance(series, pd.Series) else series

    def handle_missing_values(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Handle missing values in the dataset."""
        data_types = self.detect_data_types(df)
        missing_report = {
            "numeric_fields_missing": 0,
            "categorical_fields_missing": 0,
            "columns_with_missing": [],
            "interpolation_details": []
        }

        for column in df.columns:
            missing_count = df[column].isna().sum()
            if missing_count > 0:
                missing_report["columns_with_missing"].append(column)
                
                if data_types[column] == 'numeric':
                    df[column], interpolation_details = self.interpolate_numeric(df[column])
                    missing_report["numeric_fields_missing"] += missing_count
                    missing_report["interpolation_details"].extend([
                        {
                            "column": column,
                            **detail
                        } for detail in interpolation_details
                    ])
                elif data_types[column] == 'categorical':
                    df[column] = self.fill_categorical(df[column])
                    missing_report["categorical_fields_missing"] += missing_count

        return df, missing_report

    def remove_duplicates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Remove duplicate records and identify conflicts."""
        initial_rows = len(df)
        df_no_duplicates = df.drop_duplicates()
        
        duplicate_report = {
            "total_duplicates": initial_rows - len(df_no_duplicates),
            "conflicting_records": 0
        }

        return df_no_duplicates, duplicate_report

    def normalize_data_types(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """Normalize data types across the dataset."""
        data_types = self.detect_data_types(df)
        normalization_report = {
            "text_fields": False,
            "numeric_fields": False
        }

        for column, dtype in data_types.items():
            if dtype == 'categorical':
                df[column] = self.normalize_text(df[column])
                normalization_report["text_fields"] = True
            elif dtype == 'numeric':
                df[column] = pd.to_numeric(df[column], errors='coerce')
                normalization_report["numeric_fields"] = True

        return df, normalization_report

    def clean_data(self, data: str) -> Tuple[str, Dict]:
        """Main method to clean and validate the dataset."""
        # Load data
        df = self.load_data(data)
        
        # Initial data overview
        self.validation_report["data_overview"]["total_rows"] = len(df)
        self.validation_report["data_overview"]["total_columns"] = len(df.columns)

        # Clean data
        df, missing_report = self.handle_missing_values(df)
        df, duplicate_report = self.remove_duplicates(df)
        df, normalization_report = self.normalize_data_types(df)

        # Update validation report
        self.validation_report["missing_data"].update(missing_report)
        self.validation_report["duplicate_records"].update(duplicate_report)
        self.validation_report["normalization"].update(normalization_report)
        self.validation_report["final_status"]["rows_after_cleaning"] = len(df)
        self.validation_report["final_status"]["columns_after_cleaning"] = len(df.columns)

        return df.to_csv(index=False), self.validation_report

    def generate_report(self) -> str:
        """Generate a formatted validation report."""
        report = """
Summary Report

1. Data Overview:
   - Total Rows: {total_rows}
   - Total Columns: {total_columns}

2. Missing Data Handling:
   - Numeric Fields missing: {numeric_missing}
   - Categorical Fields missing: {categorical_missing}
   - Columns with Missing Data: {missing_columns}

   Interpolation Details:
{interpolation_details}

3. Duplicate Records:
   - Total Duplicates Removed: {duplicates}
   - Conflicting Records: {conflicts}

4. Data Normalization:
   - Text Fields Normalization: {text_norm}
   - Numeric Fields Normalization: {numeric_norm}

5. Final Dataset Status:
   - Number of Rows After Cleaning: {final_rows}
   - Number of Columns After Cleaning: {final_columns}
""".format(
            total_rows=self.validation_report["data_overview"]["total_rows"],
            total_columns=self.validation_report["data_overview"]["total_columns"],
            numeric_missing=self.validation_report["missing_data"]["numeric_fields_missing"],
            categorical_missing=self.validation_report["missing_data"]["categorical_fields_missing"],
            missing_columns=", ".join(self.validation_report["missing_data"]["columns_with_missing"]),
            interpolation_details=self._format_interpolation_details(),
            duplicates=self.validation_report["duplicate_records"]["total_duplicates"],
            conflicts=self.validation_report["duplicate_records"]["conflicting_records"],
            text_norm=self.validation_report["normalization"]["text_fields"],
            numeric_norm=self.validation_report["normalization"]["numeric_fields"],
            final_rows=self.validation_report["final_status"]["rows_after_cleaning"],
            final_columns=self.validation_report["final_status"]["columns_after_cleaning"]
        )
        return report

    def _format_interpolation_details(self) -> str:
        """Format interpolation details for the report."""
        if not self.validation_report["missing_data"]["interpolation_details"]:
            return "   No interpolation performed"
        
        details = []
        for item in self.validation_report["missing_data"]["interpolation_details"]:
            detail = f"""   Column: {item['column']}
   - Missing at index: {item['missing_index']}
   - Left value (index {item['left_index']}): {item['left_value']}
   - Right value (index {item['right_index']}): {item['right_value']}
   - Interpolation calculation: {item['calculation']}
   - Interpolated value: {item['interpolated_value']}
"""
            details.append(detail)
        return "\n".join(details)

if __name__ == "__main__":
    # Your provided data
    data = """name,region,country,address
Mira Flowers,Kayseri,United Kingdom,Ap #574-2118 Sagittis. Road
Ivory Velasquez,Tarapacá,Turkey,"P.O. Box 950, 5927 Nulla. Street"
Hadley Miles,Junín,Singapore,470-5141 Proin Road
Sasha Cunningham,Burgenland,Indonesia,163-6935 Ac Rd.
McKenzie Weaver,Akwa Ibom,United States,6562 Eu St.
Timon Gonzalez,Central Luzon,Sweden,182 Ipsum St.
Hadassah Barlow,Coquimbo,Canada,"P.O. Box 121, 1146 Dignissim Road"
Nevada Travis,South Island,Ukraine,"P.O. Box 877, 6669 Lacus Street"
Charde Williams,Swiętokrzyskie,Russian Federation,4839 Leo. St.
Kai Hahn,Castilla y León,Colombia,Ap #569-9856 Lorem Rd.
"""

    # Create instance and process data
    data_refiner = DataRefineAI()
    cleaned_data, validation_report = data_refiner.clean_data(data)

    # Print the validation report
    print(data_refiner.generate_report())
    print("\nCleaned Dataset:")
    print(cleaned_data)