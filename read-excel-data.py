#!/usr/bin/env python3
"""
Agentic AI Performance Dataset 2025 Data Processor

This script reads and processes the Agentic AI Performance Dataset 2025 Excel file,
performs required data analysis, and outputs results in JSON format.

Required Analyses:
1. Top 3 agent types with multimodal capability by percentage
2. Top 3 model architectures with multimodal capability by percentage
3. Top 3 task categories by median bias detection score

Author: Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
"""

import pandas as pd
import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_processing.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AgenticAIDataProcessor:
    """
    A class to process Agentic AI Performance Dataset 2025 data.
    """

    def __init__(self, excel_file_path: str):
        """
        Initialize the data processor.

        Args:
            excel_file_path (str): Path to the Excel file
        """
        self.excel_file_path = Path(excel_file_path)
        self.data = None
        self.processed_data = {}

    def validate_file(self) -> bool:
        """
        Validate that the Excel file exists and is readable.

        Returns:
            bool: True if file is valid, False otherwise
        """
        try:
            if not self.excel_file_path.exists():
                logger.error(f"Excel file not found: {self.excel_file_path}")
                return False

            if not self.excel_file_path.is_file():
                logger.error(f"Path is not a file: {self.excel_file_path}")
                return False

            if not self.excel_file_path.suffix.lower() in ['.xlsx', '.xls']:
                logger.error(f"File is not an Excel file: {self.excel_file_path}")
                return False

            logger.info(f"File validation successful: {self.excel_file_path}")
            return True

        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return False

    def read_excel_data(self) -> Optional[pd.DataFrame]:
        """
        Read data from Excel file.

        Returns:
            pd.DataFrame: Loaded data or None if failed
        """
        try:
            logger.info(f"Reading Excel file: {self.excel_file_path}")

            # Read Excel file
            self.data = pd.read_excel(self.excel_file_path)

            logger.info(f"Successfully read {len(self.data)} rows of data")
            logger.info(f"Columns found: {list(self.data.columns)}")

            # Display basic information about the dataset
            logger.info("Dataset Info:")
            logger.info(f"- Total rows: {len(self.data)}")
            logger.info(f"- Total columns: {len(self.data.columns)}")
            logger.info(f"- Memory usage: {self.data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

            return self.data

        except FileNotFoundError:
            logger.error(f"Excel file not found: {self.excel_file_path}")
            return None
        except pd.errors.EmptyDataError:
            logger.error("Excel file is empty")
            return None
        except Exception as e:
            logger.error(f"Error reading Excel file: {str(e)}")
            return None

    def clean_data(self) -> pd.DataFrame:
        """
        Clean and preprocess the data.

        Returns:
            pd.DataFrame: Cleaned data
        """
        try:
            if self.data is None:
                raise ValueError("No data loaded. Call read_excel_data() first.")

            logger.info("Starting data cleaning process")

            # Make a copy to avoid modifying original data
            cleaned_data = self.data.copy()

            # Remove rows with all NA values
            initial_rows = len(cleaned_data)
            cleaned_data = cleaned_data.dropna(how='all')
            removed_rows = initial_rows - len(cleaned_data)

            if removed_rows > 0:
                logger.info(f"Removed {removed_rows} rows with all NA values")

            # Convert column names to lowercase for consistency
            cleaned_data.columns = cleaned_data.columns.str.lower()

            # Remove leading/trailing whitespace from string columns
            string_columns = cleaned_data.select_dtypes(include=['object']).columns
            for col in string_columns:
                cleaned_data[col] = cleaned_data[col].astype(str).str.strip()
                # Replace empty strings with NaN
                cleaned_data[col] = cleaned_data[col].replace('', pd.NA)

            logger.info("Data cleaning completed successfully")
            return cleaned_data

        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise

    def calculate_agent_type_multimodal_percentage(self) -> List[Dict[str, Any]]:
        """
        Calculate percentage of agent types that support multimodal capability.

        Returns:
            List[Dict[str, Any]]: Top 3 agent types with multimodal capability percentage
        """
        try:
            logger.info("Calculating agent type multimodal capability percentages")

            if 'agent_type' not in self.data.columns or 'multimodal_capability' not in self.data.columns:
                logger.error("Required columns 'agent_type' or 'multimodal_capability' not found")
                return []

            # Filter for multimodal capable agents
            multimodal_agents = self.data[self.data['multimodal_capability'].astype(str).str.lower() == 'yes']

            # Count total agents by type
            total_by_type = self.data['agent_type'].value_counts()

            # Count multimodal agents by type
            multimodal_by_type = multimodal_agents['agent_type'].value_counts()

            # Calculate percentages
            results = []
            for agent_type in total_by_type.index:
                total_count = total_by_type[agent_type]
                multimodal_count = multimodal_by_type.get(agent_type, 0)
                percentage = (multimodal_count / total_count) * 100 if total_count > 0 else 0

                results.append({
                    'agent_type': agent_type,
                    'total_count': int(total_count),
                    'multimodal_count': int(multimodal_count),
                    'percentage': round(percentage, 2)
                })

            # Sort by percentage descending and get top 3
            top_results = sorted(results, key=lambda x: x['percentage'], reverse=True)[:3]

            logger.info(f"Top 3 agent types with multimodal capability:")
            for i, result in enumerate(top_results, 1):
                logger.info(f"{i}. {result['agent_type']}: {result['percentage']}%")

            return top_results

        except Exception as e:
            logger.error(f"Error calculating agent type multimodal percentage: {str(e)}")
            return []

    def calculate_model_architecture_multimodal_percentage(self) -> List[Dict[str, Any]]:
        """
        Calculate percentage of model architectures that support multimodal capability.

        Returns:
            List[Dict[str, Any]]: Top 3 model architectures with multimodal capability percentage
        """
        try:
            logger.info("Calculating model architecture multimodal capability percentages")

            if 'model_architecture' not in self.data.columns or 'multimodal_capability' not in self.data.columns:
                logger.error("Required columns 'model_architecture' or 'multimodal_capability' not found")
                return []

            # Filter for multimodal capable models
            multimodal_models = self.data[self.data['multimodal_capability'].astype(str).str.lower() == 'yes']

            # Count total models by architecture
            total_by_architecture = self.data['model_architecture'].value_counts()

            # Count multimodal models by architecture
            multimodal_by_architecture = multimodal_models['model_architecture'].value_counts()

            # Calculate percentages
            results = []
            for architecture in total_by_architecture.index:
                total_count = total_by_architecture[architecture]
                multimodal_count = multimodal_by_architecture.get(architecture, 0)
                percentage = (multimodal_count / total_count) * 100 if total_count > 0 else 0

                results.append({
                    'model_architecture': architecture,
                    'total_count': int(total_count),
                    'multimodal_count': int(multimodal_count),
                    'percentage': round(percentage, 2)
                })

            # Sort by percentage descending and get top 3
            top_results = sorted(results, key=lambda x: x['percentage'], reverse=True)[:3]

            logger.info(f"Top 3 model architectures with multimodal capability:")
            for i, result in enumerate(top_results, 1):
                logger.info(f"{i}. {result['model_architecture']}: {result['percentage']}%")

            return top_results

        except Exception as e:
            logger.error(f"Error calculating model architecture multimodal percentage: {str(e)}")
            return []

    def calculate_task_category_bias_median(self) -> List[Dict[str, Any]]:
        """
        Calculate median bias detection scores by task category.

        Returns:
            List[Dict[str, Any]]: Top 3 task categories by median bias detection score
        """
        try:
            logger.info("Calculating task category bias detection medians")

            if 'task_category' not in self.data.columns or 'bias_detection' not in self.data.columns:
                logger.error("Required columns 'task_category' or 'bias_detection' not found")
                return []

            # Convert bias_detection to numeric, handling non-numeric values
            bias_data = self.data.copy()
            bias_data['bias_detection'] = pd.to_numeric(bias_data['bias_detection'], errors='coerce')

            # Remove rows with NaN bias_detection values
            bias_data = bias_data.dropna(subset=['bias_detection'])

            # Calculate median bias detection by task category
            median_bias_by_category = bias_data.groupby('task_category')['bias_detection'].median()

            # Calculate additional statistics
            stats_by_category = bias_data.groupby('task_category')['bias_detection'].agg(['count', 'mean', 'std', 'min', 'max'])

            # Prepare results
            results = []
            for category in median_bias_by_category.index:
                results.append({
                    'task_category': category,
                    'median_score': round(float(median_bias_by_category[category]), 2),
                    'count': int(stats_by_category.loc[category, 'count']),
                    'mean_score': round(float(stats_by_category.loc[category, 'mean']), 2),
                    'std_dev': round(float(stats_by_category.loc[category, 'std']), 2) if not pd.isna(stats_by_category.loc[category, 'std']) else 0,
                    'min_score': round(float(stats_by_category.loc[category, 'min']), 2),
                    'max_score': round(float(stats_by_category.loc[category, 'max']), 2)
                })

            # Sort by median score descending and get top 3
            top_results = sorted(results, key=lambda x: x['median_score'], reverse=True)[:3]

            logger.info(f"Top 3 task categories by median bias detection score:")
            for i, result in enumerate(top_results, 1):
                logger.info(f"{i}. {result['task_category']}: {result['median_score']}")

            return top_results

        except Exception as e:
            logger.error(f"Error calculating task category bias median: {str(e)}")
            return []

    def generate_dataset_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of the dataset.

        Returns:
            Dict[str, Any]: Dataset summary statistics
        """
        try:
            logger.info("Generating dataset summary")

            summary = {
                'total_rows': len(self.data),
                'total_columns': len(self.data.columns),
                'columns': list(self.data.columns),
                'data_types': {col: str(dtype) for col, dtype in self.data.dtypes.items()},
                'missing_values': {col: int(count) for col, count in self.data.isnull().sum().items()},
                'unique_values': {col: int(count) for col, count in self.data.nunique().items()},
                'processing_timestamp': datetime.now().isoformat(),
                'source_file': str(self.excel_file_path)
            }

            logger.info(f"Dataset summary generated: {summary['total_rows']} rows, {summary['total_columns']} columns")
            return summary

        except Exception as e:
            logger.error(f"Error generating dataset summary: {str(e)}")
            return {}

    def process_data(self) -> Dict[str, Any]:
        """
        Process all data and return complete results.

        Returns:
            Dict[str, Any]: Complete processing results
        """
        try:
            logger.info("Starting complete data processing")

            # Step 1: Validate file
            if not self.validate_file():
                raise ValueError("File validation failed")

            # Step 2: Read Excel data
            if not self.read_excel_data():
                raise ValueError("Failed to read Excel data")

            # Step 3: Clean data
            self.data = self.clean_data()

            # Step 4: Perform all analyses
            self.processed_data = {
                'dataset_summary': self.generate_dataset_summary(),
                'agent_type_multimodal_ranking': self.calculate_agent_type_multimodal_percentage(),
                'model_architecture_multimodal_ranking': self.calculate_model_architecture_multimodal_percentage(),
                'task_category_bias_ranking': self.calculate_task_category_bias_median()
            }

            # Add processing metadata
            self.processed_data['metadata'] = {
                'processing_timestamp': datetime.now().isoformat(),
                'python_version': sys.version,
                'pandas_version': pd.__version__,
                'total_processed_records': len(self.data)
            }

            logger.info("Data processing completed successfully")
            return self.processed_data

        except Exception as e:
            logger.error(f"Error in data processing: {str(e)}")
            raise

    def save_to_json(self, output_file: str = 'dashboard_data.json') -> bool:
        """
        Save processed data to JSON file.

        Args:
            output_file (str): Output JSON file path

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.processed_data:
                logger.error("No processed data to save")
                return False

            output_path = Path(output_file)
            logger.info(f"Saving processed data to: {output_path}")

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.processed_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Data successfully saved to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving data to JSON: {str(e)}")
            return False


def main():
    """
    Main function to run the data processing.
    """
    try:
        # Initialize processor
        excel_file = "first-80-rows-agentic_ai_performance_dataset_20250622.xlsx"
        processor = AgenticAIDataProcessor(excel_file)

        # Process data
        results = processor.process_data()

        # Save to JSON
        if processor.save_to_json():
            print("✅ Data processing completed successfully!")
            print(f"📊 Processed {results['metadata']['total_processed_records']} records")
            print("💾 Results saved to dashboard_data.json")

            # Print summary of key findings
            print("\n📈 Key Findings:")

            if results['agent_type_multimodal_ranking']:
                print("Top 3 Agent Types with Multimodal Capability:")
                for i, agent in enumerate(results['agent_type_multimodal_ranking'], 1):
                    print(f"  {i}. {agent['agent_type']}: {agent['percentage']}%")

            if results['model_architecture_multimodal_ranking']:
                print("\nTop 3 Model Architectures with Multimodal Capability:")
                for i, arch in enumerate(results['model_architecture_multimodal_ranking'], 1):
                    print(f"  {i}. {arch['model_architecture']}: {arch['percentage']}%")

            if results['task_category_bias_ranking']:
                print("\nTop 3 Task Categories by Median Bias Detection Score:")
                for i, task in enumerate(results['task_category_bias_ranking'], 1):
                    print(f"  {i}. {task['task_category']}: {task['median_score']}")

        else:
            print("❌ Failed to save results to JSON file")

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()