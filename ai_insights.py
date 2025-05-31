import json
import os
import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Google Gemini
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

class AIInsights:
    """Generates AI-powered business insights and recommendations"""
    
    def __init__(self):
        self.model = None
        if GOOGLE_API_KEY:
            try:
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                st.warning(f"Could not initialize Gemini model: {e}")
        else:
            st.warning("Google API key not found. AI recommendations will not be available.")
    
    def generate_business_recommendations(self, kpis, sales_data=None, expenses_data=None, inventory_data=None):
        """Generate comprehensive business recommendations based on data"""
        if not self.model:
            return self._get_fallback_recommendations()
            
        try:
            # Prepare data summary for AI analysis
            data_summary = self._prepare_data_summary(kpis, sales_data, expenses_data, inventory_data)
            
            prompt = f"""
            You are a business consultant analyzing data for a small to medium enterprise (SME). 
            Based on the following business data, provide actionable recommendations to improve operations, 
            reduce costs, and increase profitability.
            
            Business Data:
            {json.dumps(data_summary, indent=2)}
            
            Please provide your analysis in JSON format with the following structure:
            {{
                "overall_health": "excellent/good/fair/poor",
                "key_insights": [
                    "insight 1",
                    "insight 2",
                    "insight 3"
                ],
                "recommendations": [
                    {{
                        "category": "cost_optimization/revenue_growth/inventory_management/operations",
                        "priority": "high/medium/low",
                        "action": "specific action to take",
                        "expected_impact": "estimated financial or operational impact",
                        "implementation_difficulty": "easy/medium/hard"
                    }}
                ],
                "alerts": [
                    {{
                        "type": "warning/critical/info",
                        "message": "alert message",
                        "action_needed": "immediate action required"
                    }}
                ]
            }}
            
            Focus on:
            1. Cost optimization opportunities
            2. Revenue growth strategies
            3. Inventory management improvements
            4. Operational efficiency gains
            5. Risk mitigation
            
            Return only valid JSON, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean the response to ensure it's valid JSON
            if result_text.startswith('```json'):
                result_text = result_text.replace('```json', '').replace('```', '')
            
            return json.loads(result_text)
            
        except Exception as e:
            st.error(f"Error generating AI recommendations: {str(e)}")
            return self._get_fallback_recommendations()
    
    def analyze_cost_optimization(self, expenses_data, kpis):
        """Analyze expenses for cost optimization opportunities"""
        if not self.model:
            return {
                "high_cost_categories": ["Office Supplies", "Marketing"],
                "optimization_opportunities": [
                    {
                        "category": "Office Supplies",
                        "current_amount": "15% of total expenses",
                        "recommended_action": "Switch to bulk purchasing and negotiate better rates",
                        "estimated_savings": "5-10% reduction",
                        "risk_level": "low"
                    }
                ],
                "expense_ratio_analysis": "Expense analysis requires API configuration",
                "quick_wins": ["Review subscription services", "Negotiate supplier contracts"]
            }
            
        try:
            if expenses_data is None:
                return {"error": "No expense data available for analysis"}
            
            # Calculate expense insights
            expense_summary = {
                "total_expenses": kpis.get('total_expenses', 0),
                "expense_categories": kpis.get('expenses_by_category', {}),
                "expense_to_revenue_ratio": (kpis.get('total_expenses', 0) / kpis.get('total_revenue', 1)) * 100
            }
            
            prompt = f"""
            Analyze the following expense data for cost optimization opportunities:
            
            {json.dumps(expense_summary, indent=2)}
            
            Provide specific cost-cutting recommendations in JSON format:
            {{
                "high_cost_categories": ["category1", "category2"],
                "optimization_opportunities": [
                    {{
                        "category": "expense category",
                        "current_amount": "current monthly/annual spend",
                        "recommended_action": "specific action",
                        "estimated_savings": "estimated monthly savings",
                        "risk_level": "low/medium/high"
                    }}
                ],
                "expense_ratio_analysis": "analysis of expense-to-revenue ratio",
                "quick_wins": ["immediate actions that can reduce costs"]
            }}
            
            Return only valid JSON, no additional text.
            """
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if result_text.startswith('```json'):
                result_text = result_text.replace('```json', '').replace('```', '')
            
            return json.loads(result_text)
            
        except Exception as e:
            return {"error": f"Failed to analyze cost optimization: {str(e)}"}
    
    def generate_inventory_insights(self, inventory_data, sales_data=None):
        """Generate insights for inventory management"""
        try:
            if inventory_data is None:
                return {"error": "No inventory data available for analysis"}
            
            # Calculate inventory metrics
            low_stock_items = inventory_data[
                inventory_data['current_stock'] <= inventory_data['reorder_level']
            ]
            
            inventory_summary = {
                "total_products": len(inventory_data),
                "low_stock_count": len(low_stock_items),
                "total_inventory_value": inventory_data['current_stock'].sum(),
                "average_stock_level": inventory_data['current_stock'].mean(),
                "low_stock_products": low_stock_items[['product_name', 'current_stock', 'reorder_level']].to_dict('records')[:5]
            }
            
            prompt = f"""
            Analyze the following inventory data and provide optimization recommendations:
            
            {json.dumps(inventory_summary, indent=2)}
            
            Provide inventory management insights in JSON format:
            {{
                "inventory_health": "excellent/good/fair/poor",
                "reorder_recommendations": [
                    {{
                        "product": "product name",
                        "current_stock": "current level",
                        "recommended_order": "suggested order quantity",
                        "urgency": "immediate/soon/can_wait"
                    }}
                ],
                "optimization_strategies": [
                    "strategy 1",
                    "strategy 2"
                ],
                "cost_reduction_opportunities": [
                    "opportunity 1",
                    "opportunity 2"
                ],
                "alerts": [
                    "critical inventory alerts"
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an inventory management expert. Provide practical inventory optimization advice."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Failed to analyze inventory: {str(e)}"}
    
    def analyze_revenue_opportunities(self, sales_data, kpis):
        """Analyze sales data for revenue growth opportunities"""
        try:
            if sales_data is None:
                return {"error": "No sales data available for analysis"}
            
            # Calculate sales insights
            sales_summary = {
                "total_revenue": kpis.get('total_revenue', 0),
                "revenue_growth": kpis.get('revenue_growth', 0),
                "avg_daily_revenue": kpis.get('avg_daily_revenue', 0),
                "profit_margin": kpis.get('profit_margin', 0)
            }
            
            # Add product performance if available
            if 'product_id' in sales_data.columns:
                product_performance = sales_data.groupby('product_id')['revenue'].sum().sort_values(ascending=False)
                sales_summary['top_products'] = product_performance.head(5).to_dict()
                sales_summary['underperforming_products'] = product_performance.tail(5).to_dict()
            
            prompt = f"""
            Analyze the following sales data for revenue growth opportunities:
            
            {json.dumps(sales_summary, indent=2)}
            
            Provide revenue optimization recommendations in JSON format:
            {{
                "revenue_trend_analysis": "analysis of current revenue trend",
                "growth_opportunities": [
                    {{
                        "strategy": "specific growth strategy",
                        "potential_impact": "estimated revenue increase",
                        "implementation_effort": "low/medium/high",
                        "timeframe": "short-term/medium-term/long-term"
                    }}
                ],
                "product_recommendations": [
                    "product-specific recommendations"
                ],
                "pricing_insights": [
                    "pricing strategy recommendations"
                ],
                "market_expansion_ideas": [
                    "ideas for market expansion"
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a revenue optimization expert. Provide actionable strategies to increase revenue."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            return {"error": f"Failed to analyze revenue opportunities: {str(e)}"}
    
    def _prepare_data_summary(self, kpis, sales_data, expenses_data, inventory_data):
        """Prepare a comprehensive data summary for AI analysis"""
        summary = {
            "kpis": kpis,
            "data_availability": {
                "sales_data": sales_data is not None,
                "expenses_data": expenses_data is not None,
                "inventory_data": inventory_data is not None
            }
        }
        
        # Add data-specific insights
        if sales_data is not None:
            summary["sales_insights"] = {
                "total_transactions": len(sales_data),
                "date_range": f"{sales_data['date'].min()} to {sales_data['date'].max()}"
            }
        
        if expenses_data is not None:
            summary["expense_insights"] = {
                "total_expense_records": len(expenses_data),
                "expense_categories": list(expenses_data['category'].unique())
            }
        
        if inventory_data is not None:
            summary["inventory_insights"] = {
                "products_count": len(inventory_data),
                "low_stock_count": len(inventory_data[inventory_data['current_stock'] <= inventory_data['reorder_level']])
            }
        
        return summary
    
    def _get_fallback_recommendations(self):
        """Provide fallback recommendations when AI analysis fails"""
        return {
            "overall_health": "unknown",
            "key_insights": [
                "Unable to generate AI insights at this time",
                "Please ensure your OpenAI API key is configured correctly",
                "Manual data analysis is recommended"
            ],
            "recommendations": [
                {
                    "category": "operations",
                    "priority": "medium",
                    "action": "Review your data quality and completeness",
                    "expected_impact": "Improved decision making",
                    "implementation_difficulty": "easy"
                }
            ],
            "alerts": [
                {
                    "type": "warning",
                    "message": "AI recommendations are currently unavailable",
                    "action_needed": "Check API configuration"
                }
            ]
        }
