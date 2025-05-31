import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import io

class DataProcessor:
    """Handles data processing and validation for the dashboard"""
    
    def __init__(self):
        self.sales_data = None
        self.expenses_data = None
        self.inventory_data = None
        self.supplier_data = None
        
    def validate_sales_data(self, df):
        """Validate sales data format"""
        required_columns = ['date', 'revenue']
        optional_columns = ['product_id', 'quantity', 'customer_id', 'category']
        
        missing_required = [col for col in required_columns if col not in df.columns]
        if missing_required:
            raise ValueError(f"Missing required columns: {missing_required}")
        
        # Convert date column
        try:
            df['date'] = pd.to_datetime(df['date'])
        except Exception as e:
            raise ValueError(f"Invalid date format in 'date' column: {e}")
        
        # Validate revenue column
        if not pd.api.types.is_numeric_dtype(df['revenue']):
            try:
                df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
            except:
                raise ValueError("Revenue column must contain numeric values")
        
        # Remove rows with null revenue
        df = df.dropna(subset=['revenue'])
        
        return df
    
    def validate_expenses_data(self, df):
        """Validate expenses data format"""
        required_columns = ['date', 'amount', 'category']
        
        missing_required = [col for col in required_columns if col not in df.columns]
        if missing_required:
            raise ValueError(f"Missing required columns: {missing_required}")
        
        # Convert date column
        try:
            df['date'] = pd.to_datetime(df['date'])
        except Exception as e:
            raise ValueError(f"Invalid date format in 'date' column: {e}")
        
        # Validate amount column
        if not pd.api.types.is_numeric_dtype(df['amount']):
            try:
                df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            except:
                raise ValueError("Amount column must contain numeric values")
        
        df = df.dropna(subset=['amount'])
        
        return df
    
    def validate_inventory_data(self, df):
        """Validate inventory data format"""
        required_columns = ['product_id', 'product_name', 'current_stock', 'reorder_level']
        optional_columns = ['supplier', 'cost_per_unit', 'last_updated']
        
        missing_required = [col for col in required_columns if col not in df.columns]
        if missing_required:
            raise ValueError(f"Missing required columns: {missing_required}")
        
        # Validate numeric columns
        numeric_columns = ['current_stock', 'reorder_level']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    raise ValueError(f"{col} column must contain numeric values")
        
        return df
    
    def process_uploaded_file(self, file, data_type):
        """Process uploaded file and validate data"""
        try:
            # Read file based on extension
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload CSV or Excel files.")
            
            # Validate based on data type
            if data_type == 'sales':
                df = self.validate_sales_data(df)
                self.sales_data = df
            elif data_type == 'expenses':
                df = self.validate_expenses_data(df)
                self.expenses_data = df
            elif data_type == 'inventory':
                df = self.validate_inventory_data(df)
                self.inventory_data = df
            else:
                raise ValueError("Invalid data type specified")
            
            return df, None
            
        except Exception as e:
            return None, str(e)
    
    def calculate_kpis(self):
        """Calculate key performance indicators"""
        kpis = {}
        
        if self.sales_data is not None:
            # Revenue metrics
            kpis['total_revenue'] = self.sales_data['revenue'].sum()
            kpis['avg_daily_revenue'] = self.sales_data.groupby('date')['revenue'].sum().mean()
            
            # Calculate revenue trend (last 30 days vs previous 30 days)
            current_date = self.sales_data['date'].max()
            last_30_days = self.sales_data[
                self.sales_data['date'] >= (current_date - timedelta(days=30))
            ]['revenue'].sum()
            
            prev_30_days = self.sales_data[
                (self.sales_data['date'] >= (current_date - timedelta(days=60))) &
                (self.sales_data['date'] < (current_date - timedelta(days=30)))
            ]['revenue'].sum()
            
            if prev_30_days > 0:
                kpis['revenue_growth'] = ((last_30_days - prev_30_days) / prev_30_days) * 100
            else:
                kpis['revenue_growth'] = 0
        
        if self.expenses_data is not None:
            # Expense metrics
            kpis['total_expenses'] = self.expenses_data['amount'].sum()
            kpis['avg_daily_expenses'] = self.expenses_data.groupby('date')['amount'].sum().mean()
            
            # Expense by category
            kpis['expenses_by_category'] = self.expenses_data.groupby('category')['amount'].sum().to_dict()
        
        # Profit margin calculation
        if self.sales_data is not None and self.expenses_data is not None:
            total_profit = kpis.get('total_revenue', 0) - kpis.get('total_expenses', 0)
            if kpis.get('total_revenue', 0) > 0:
                kpis['profit_margin'] = (total_profit / kpis['total_revenue']) * 100
            else:
                kpis['profit_margin'] = 0
            kpis['total_profit'] = total_profit
        
        if self.inventory_data is not None:
            # Inventory metrics
            kpis['total_products'] = len(self.inventory_data)
            kpis['low_stock_items'] = len(
                self.inventory_data[
                    self.inventory_data['current_stock'] <= self.inventory_data['reorder_level']
                ]
            )
            kpis['total_inventory_value'] = self.inventory_data['current_stock'].sum()
        
        return kpis
    
    def get_revenue_trend_data(self, period='daily'):
        """Get revenue trend data for charts"""
        if self.sales_data is None:
            return None
        
        if period == 'daily':
            trend_data = self.sales_data.groupby('date')['revenue'].sum().reset_index()
        elif period == 'weekly':
            self.sales_data['week'] = self.sales_data['date'].dt.to_period('W')
            trend_data = self.sales_data.groupby('week')['revenue'].sum().reset_index()
            trend_data['date'] = trend_data['week'].dt.start_time
        elif period == 'monthly':
            self.sales_data['month'] = self.sales_data['date'].dt.to_period('M')
            trend_data = self.sales_data.groupby('month')['revenue'].sum().reset_index()
            trend_data['date'] = trend_data['month'].dt.start_time
        
        return trend_data
    
    def get_expense_breakdown(self):
        """Get expense breakdown by category"""
        if self.expenses_data is None:
            return None
        
        return self.expenses_data.groupby('category')['amount'].sum().reset_index()
    
    def get_low_stock_alerts(self):
        """Get products with low stock levels"""
        if self.inventory_data is None:
            return None
        
        low_stock = self.inventory_data[
            self.inventory_data['current_stock'] <= self.inventory_data['reorder_level']
        ]
        
        return low_stock[['product_id', 'product_name', 'current_stock', 'reorder_level']]
    
    def export_data_summary(self):
        """Export data summary for reports"""
        summary = {
            'data_loaded': {
                'sales': self.sales_data is not None,
                'expenses': self.expenses_data is not None,
                'inventory': self.inventory_data is not None
            },
            'kpis': self.calculate_kpis()
        }
        
        if self.sales_data is not None:
            summary['sales_summary'] = {
                'total_records': len(self.sales_data),
                'date_range': f"{self.sales_data['date'].min()} to {self.sales_data['date'].max()}"
            }
        
        if self.expenses_data is not None:
            summary['expenses_summary'] = {
                'total_records': len(self.expenses_data),
                'categories': list(self.expenses_data['category'].unique())
            }
        
        if self.inventory_data is not None:
            summary['inventory_summary'] = {
                'total_products': len(self.inventory_data),
                'low_stock_count': len(self.get_low_stock_alerts()) if self.get_low_stock_alerts() is not None else 0
            }
        
        return summary
