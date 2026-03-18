"""
Data Export Module
Supports exporting data to CSV and JSON formats
"""

import json
import csv
from datetime import datetime
from typing import List, Dict
import pandas as pd
import os


class Exporter:
    """Data export class"""
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize exporter
        
        Args:
            output_dir: Output directory path
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✓ Created output directory: {self.output_dir}")
    
    def _generate_filename(self, prefix: str, extension: str) -> str:
        """
        Generate filename with timestamp
        
        Args:
            prefix: Filename prefix
            extension: File extension (without dot)
        
        Returns:
            Complete file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.{extension}"
        return os.path.join(self.output_dir, filename)
    
    def export_to_csv(self, data: List[Dict], filename_prefix: str = "reddit_data") -> str:
        """
        Export data to CSV file
        
        Args:
            data: List of data to export
            filename_prefix: Filename prefix
        
        Returns:
            Path of exported file
        """
        if not data:
            print("⚠ No data to export")
            return ""
        
        filepath = self._generate_filename(filename_prefix, "csv")
        
        try:
            # Export using pandas, handle encoding
            df = pd.DataFrame(data)
            
            # Convert datetime columns to strings
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]):
                    df[col] = df[col].astype(str)
            
            # Export to CSV with UTF-8 encoding and BOM (for Excel compatibility)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            print(f"✓ Data exported to CSV: {filepath}")
            print(f"  Rows: {len(data)}, Columns: {len(df.columns)}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error exporting CSV: {str(e)}")
            return ""
    
    def export_to_json(self, data: List[Dict], filename_prefix: str = "reddit_data") -> str:
        """
        Export data to JSON file
        
        Args:
            data: List of data to export
            filename_prefix: Filename prefix
        
        Returns:
            Path of exported file
        """
        if not data:
            print("⚠ No data to export")
            return ""
        
        filepath = self._generate_filename(filename_prefix, "json")
        
        try:
            # Handle datetime objects
            def json_serial(obj):
                """JSON serialization helper function to handle datetime objects"""
                if isinstance(obj, datetime):
                    return obj.isoformat()
                raise TypeError(f"Type {type(obj)} is not serializable")
            
            # Export to JSON with indentation formatting, ensure non-ASCII characters are preserved
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=json_serial)
            
            print(f"✓ Data exported to JSON: {filepath}")
            print(f"  Records: {len(data)}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error exporting JSON: {str(e)}")
            return ""
    
    def export_summary(self, summary_text: str, filename_prefix: str = "summary") -> str:
        """
        Export summary text
        
        Args:
            summary_text: Summary text content
            filename_prefix: Filename prefix
        
        Returns:
            Path of exported file
        """
        if not summary_text:
            print("⚠ No summary to export")
            return ""
        
        filepath = self._generate_filename(filename_prefix, "txt")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(summary_text)
            
            print(f"✓ Summary exported to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error exporting summary: {str(e)}")
            return ""
    
    def export_trends(self, trends_df: pd.DataFrame, filename_prefix: str = "trends") -> str:
        """
        Export trend analysis data
        
        Args:
            trends_df: Trends data DataFrame
            filename_prefix: Filename prefix
        
        Returns:
            Path of exported file
        """
        if trends_df.empty:
            print("⚠ No trends data to export")
            return ""
        
        filepath = self._generate_filename(filename_prefix, "csv")
        
        try:
            trends_df.to_csv(filepath, encoding='utf-8-sig')
            print(f"✓ Trends data exported to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error exporting trends data: {str(e)}")
            return ""
    
    def export_all(
        self,
        posts: List[Dict],
        summary: str,
        trends: pd.DataFrame = None,
        format: str = "both"
    ) -> Dict[str, str]:
        """
        Export all data
        
        Args:
            posts: Post data
            summary: Summary text
            trends: Trends data (optional)
            format: Export format (csv, json, both)
        
        Returns:
            Dictionary of exported file paths
        """
        exported_files = {}
        
        print("\n" + "="*60)
        print("Starting data export...")
        print("="*60)
        
        # Export post data
        if format in ["csv", "both"]:
            csv_path = self.export_to_csv(posts, "posts")
            if csv_path:
                exported_files['posts_csv'] = csv_path
        
        if format in ["json", "both"]:
            json_path = self.export_to_json(posts, "posts")
            if json_path:
                exported_files['posts_json'] = json_path
        
        # Export summary
        summary_path = self.export_summary(summary)
        if summary_path:
            exported_files['summary'] = summary_path
        
        # Export trends data (if available)
        if trends is not None and not trends.empty:
            trends_path = self.export_trends(trends)
            if trends_path:
                exported_files['trends'] = trends_path
        
        print("="*60)
        print(f"✓ Export complete! {len(exported_files)} files exported")
        print("="*60 + "\n")
        
        return exported_files
