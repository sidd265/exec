import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, r2_score
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import streamlit as st

class BusinessForecasting:
    """Handles business forecasting using statistical models"""
    
    def __init__(self):
        self.models = {}
        self.forecast_data = {}
    
    def prepare_time_series_data(self, data, date_col, value_col, period='daily'):
        """Prepare time series data for forecasting"""
        try:
            # Ensure date column is datetime
            data[date_col] = pd.to_datetime(data[date_col])
            
            # Group by period
            if period == 'daily':
                grouped_data = data.groupby(data[date_col].dt.date)[value_col].sum().reset_index()
            elif period == 'weekly':
                grouped_data = data.groupby(data[date_col].dt.to_period('W'))[value_col].sum().reset_index()
                grouped_data[date_col] = grouped_data[date_col].dt.start_time
            elif period == 'monthly':
                grouped_data = data.groupby(data[date_col].dt.to_period('M'))[value_col].sum().reset_index()
                grouped_data[date_col] = grouped_data[date_col].dt.start_time
            
            # Sort by date and reset index
            grouped_data = grouped_data.sort_values(date_col).reset_index(drop=True)
            
            # Create time-based features
            grouped_data['time_index'] = range(len(grouped_data))
            grouped_data['day_of_week'] = pd.to_datetime(grouped_data[date_col]).dt.dayofweek
            grouped_data['month'] = pd.to_datetime(grouped_data[date_col]).dt.month
            grouped_data['quarter'] = pd.to_datetime(grouped_data[date_col]).dt.quarter
            
            return grouped_data
            
        except Exception as e:
            st.error(f"Error preparing time series data: {str(e)}")
            return None
    
    def forecast_revenue(self, sales_data, forecast_periods=30, model_type='linear'):
        """Forecast revenue for specified periods"""
        try:
            if sales_data is None or len(sales_data) < 7:
                return None, "Insufficient data for forecasting (minimum 7 data points required)"
            
            # Prepare data
            ts_data = self.prepare_time_series_data(sales_data, 'date', 'revenue', 'daily')
            if ts_data is None or len(ts_data) < 7:
                return None, "Unable to prepare time series data"
            
            # Prepare features and target
            X = ts_data[['time_index']].values
            y = ts_data['revenue'].values
            
            # Choose model based on type
            if model_type == 'polynomial':
                poly_features = PolynomialFeatures(degree=2)
                X_poly = poly_features.fit_transform(X)
                model = LinearRegression()
                model.fit(X_poly, y)
            else:  # linear
                model = LinearRegression()
                model.fit(X, y)
            
            # Generate future time indices
            last_time_index = ts_data['time_index'].max()
            future_indices = np.array([[last_time_index + i + 1] for i in range(forecast_periods)])
            
            # Make predictions
            if model_type == 'polynomial':
                future_indices_poly = poly_features.transform(future_indices)
                predictions = model.predict(future_indices_poly)
            else:
                predictions = model.predict(future_indices)
            
            # Ensure predictions are non-negative
            predictions = np.maximum(predictions, 0)
            
            # Create future dates
            last_date = ts_data['date'].max()
            future_dates = [last_date + timedelta(days=i+1) for i in range(forecast_periods)]
            
            # Calculate model performance
            if model_type == 'polynomial':
                train_predictions = model.predict(X_poly)
            else:
                train_predictions = model.predict(X)
            
            mae = mean_absolute_error(y, train_predictions)
            r2 = r2_score(y, train_predictions)
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'date': future_dates,
                'predicted_revenue': predictions,
                'confidence_lower': predictions * 0.85,  # Simple confidence interval
                'confidence_upper': predictions * 1.15
            })
            
            # Store model and results
            self.models['revenue'] = model
            self.forecast_data['revenue'] = {
                'historical': ts_data,
                'forecast': forecast_df,
                'metrics': {'mae': mae, 'r2': r2, 'model_type': model_type}
            }
            
            return forecast_df, None
            
        except Exception as e:
            return None, f"Error in revenue forecasting: {str(e)}"
    
    def forecast_expenses(self, expenses_data, forecast_periods=30):
        """Forecast expenses based on historical data"""
        try:
            if expenses_data is None or len(expenses_data) < 7:
                return None, "Insufficient expense data for forecasting"
            
            # Prepare data
            ts_data = self.prepare_time_series_data(expenses_data, 'date', 'amount', 'daily')
            if ts_data is None or len(ts_data) < 7:
                return None, "Unable to prepare expense time series data"
            
            # Simple moving average for expenses (they tend to be more stable)
            window_size = min(7, len(ts_data) // 2)
            moving_avg = ts_data['amount'].rolling(window=window_size).mean().iloc[-1]
            
            # Generate future dates
            last_date = ts_data['date'].max()
            future_dates = [last_date + timedelta(days=i+1) for i in range(forecast_periods)]
            
            # Create predictions with some variation
            base_prediction = moving_avg
            predictions = []
            for i in range(forecast_periods):
                # Add small random variation (±10%)
                variation = np.random.normal(0, 0.1)
                prediction = base_prediction * (1 + variation)
                predictions.append(max(prediction, 0))  # Ensure non-negative
            
            # Create forecast dataframe
            forecast_df = pd.DataFrame({
                'date': future_dates,
                'predicted_expenses': predictions,
                'confidence_lower': [p * 0.8 for p in predictions],
                'confidence_upper': [p * 1.2 for p in predictions]
            })
            
            self.forecast_data['expenses'] = {
                'historical': ts_data,
                'forecast': forecast_df,
                'metrics': {'method': 'moving_average', 'window_size': window_size}
            }
            
            return forecast_df, None
            
        except Exception as e:
            return None, f"Error in expense forecasting: {str(e)}"
    
    def forecast_inventory_needs(self, sales_data, inventory_data, forecast_periods=30):
        """Forecast inventory requirements based on sales patterns"""
        try:
            if sales_data is None or inventory_data is None:
                return None, "Sales and inventory data required for forecasting"
            
            # Check if product_id exists in sales data
            if 'product_id' not in sales_data.columns:
                return None, "Product ID not found in sales data"
            
            # Calculate sales velocity per product
            sales_velocity = sales_data.groupby('product_id').agg({
                'quantity': 'sum',
                'date': ['min', 'max']
            }).reset_index()
            
            sales_velocity.columns = ['product_id', 'total_quantity', 'first_sale', 'last_sale']
            sales_velocity['days_active'] = (sales_velocity['last_sale'] - sales_velocity['first_sale']).dt.days + 1
            sales_velocity['daily_velocity'] = sales_velocity['total_quantity'] / sales_velocity['days_active']
            
            # Merge with inventory data
            inventory_forecast = inventory_data.merge(
                sales_velocity[['product_id', 'daily_velocity']], 
                on='product_id', 
                how='left'
            )
            
            # Fill missing velocities with 0
            inventory_forecast['daily_velocity'] = inventory_forecast['daily_velocity'].fillna(0)
            
            # Calculate forecasted needs
            inventory_forecast['forecasted_demand'] = inventory_forecast['daily_velocity'] * forecast_periods
            inventory_forecast['predicted_stock'] = inventory_forecast['current_stock'] - inventory_forecast['forecasted_demand']
            inventory_forecast['reorder_needed'] = inventory_forecast['predicted_stock'] <= inventory_forecast['reorder_level']
            inventory_forecast['suggested_order'] = np.where(
                inventory_forecast['reorder_needed'],
                inventory_forecast['reorder_level'] + inventory_forecast['forecasted_demand'],
                0
            )
            
            self.forecast_data['inventory'] = {
                'forecast': inventory_forecast,
                'forecast_periods': forecast_periods
            }
            
            return inventory_forecast, None
            
        except Exception as e:
            return None, f"Error in inventory forecasting: {str(e)}"
    
    def create_forecast_visualization(self, data_type='revenue'):
        """Create visualization for forecast data"""
        try:
            if data_type not in self.forecast_data:
                return None
            
            forecast_info = self.forecast_data[data_type]
            
            if data_type == 'revenue' or data_type == 'expenses':
                historical = forecast_info['historical']
                forecast = forecast_info['forecast']
                
                fig = go.Figure()
                
                # Historical data
                value_col = 'revenue' if data_type == 'revenue' else 'amount'
                predicted_col = f'predicted_{data_type}'
                
                fig.add_trace(go.Scatter(
                    x=historical['date'],
                    y=historical[value_col],
                    mode='lines+markers',
                    name=f'Historical {data_type.title()}',
                    line=dict(color='blue')
                ))
                
                # Forecast data
                fig.add_trace(go.Scatter(
                    x=forecast['date'],
                    y=forecast[predicted_col],
                    mode='lines+markers',
                    name=f'Forecasted {data_type.title()}',
                    line=dict(color='red', dash='dash')
                ))
                
                # Confidence interval
                fig.add_trace(go.Scatter(
                    x=list(forecast['date']) + list(forecast['date'][::-1]),
                    y=list(forecast['confidence_upper']) + list(forecast['confidence_lower'][::-1]),
                    fill='toself',
                    fillcolor='rgba(255,0,0,0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Confidence Interval',
                    showlegend=True
                ))
                
                fig.update_layout(
                    title=f'{data_type.title()} Forecast',
                    xaxis_title='Date',
                    yaxis_title=data_type.title(),
                    hovermode='x unified'
                )
                
                return fig
            
            elif data_type == 'inventory':
                # For inventory, create a bar chart of reorder recommendations
                forecast = forecast_info['forecast']
                reorder_items = forecast[forecast['reorder_needed']]
                
                if len(reorder_items) == 0:
                    return None
                
                fig = px.bar(
                    reorder_items,
                    x='product_name',
                    y='suggested_order',
                    title='Inventory Reorder Recommendations',
                    labels={'suggested_order': 'Suggested Order Quantity', 'product_name': 'Product'}
                )
                
                fig.update_layout(xaxis_tickangle=-45)
                return fig
            
        except Exception as e:
            st.error(f"Error creating forecast visualization: {str(e)}")
            return None
    
    def get_forecast_summary(self):
        """Get summary of all forecasts"""
        summary = {}
        
        for data_type, forecast_info in self.forecast_data.items():
            if data_type in ['revenue', 'expenses']:
                forecast_df = forecast_info['forecast']
                predicted_col = f'predicted_{data_type}'
                
                summary[data_type] = {
                    'next_30_days_total': forecast_df[predicted_col].sum(),
                    'daily_average': forecast_df[predicted_col].mean(),
                    'trend': 'increasing' if forecast_df[predicted_col].iloc[-1] > forecast_df[predicted_col].iloc[0] else 'decreasing',
                    'model_accuracy': forecast_info.get('metrics', {})
                }
            
            elif data_type == 'inventory':
                forecast_df = forecast_info['forecast']
                reorder_count = len(forecast_df[forecast_df['reorder_needed']])
                
                summary[data_type] = {
                    'products_needing_reorder': reorder_count,
                    'total_suggested_orders': forecast_df['suggested_order'].sum(),
                    'forecast_period_days': forecast_info['forecast_periods']
                }
        
        return summary
