import streamlit as st
import pandas as pd
from utils.data_processor import DataProcessor

# Page configuration
st.set_page_config(
    page_title="Home - OpsIntel.info",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()

def main():
    """Main landing page for OpsIntel.info"""

    # Custom CSS for professional styling
    st.markdown("""
    <style>
    /* Hide Streamlit's default components */
    .stDeployButton {display:none;}
    header[data-testid="stHeader"] {display:none;}

    /* Full width responsive layout */
    .stApp {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .stMainBlockContainer {
        padding: 1rem !important;
        width: 100% !important;
        max-width: 100% !important;
    }

    /* Responsive container widths */
    @media (min-width: 1024px) {
        .stMainBlockContainer {
            padding: 2rem 4rem !important;
        }
    }

    @media (min-width: 1400px) {
        .stMainBlockContainer {
            padding: 2rem 6rem !important;
        }
    }

    /* Main content wrapper */
    .main-content {
        width: 100%;
        padding: 0 2rem;
    }

    /* Navigation bar */
    .nav-container {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 1rem 2rem;
        margin: 0 0 2rem 0;
        border-bottom: 1px solid #334155;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    .nav-logo {
        display: flex;
        align-items: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }

    .nav-link {
        color: #CBD5E1;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s;
        font-weight: 500;
        cursor: pointer;
    }

    .nav-link:hover {
        color: #F8FAFC;
        background: rgba(139, 92, 246, 0.3);
        transform: translateY(-1px);
    }

    .nav-link.active {
        color: #8B5CF6;
        background: rgba(139, 92, 246, 0.2);
    }

    /* Mobile responsive navigation */
    @media (max-width: 768px) {
        .nav-container {
            flex-direction: column;
            gap: 1rem;
            padding: 1rem;
        }

        .nav-links {
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .nav-link {
            font-size: 0.9rem;
            padding: 0.4rem 0.8rem;
        }
    }

    /* Hero section */
    .hero-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 4rem 2rem;
        margin: 0 0 3rem 0;
        border-radius: 16px;
        border: 1px solid #334155;
        text-align: center;
        width: 100%;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-align: center;
        line-height: 1.2;
    }

    /* Responsive text sizing */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }

        .hero-subtitle {
            font-size: 1.1rem;
        }
    }

    @media (max-width: 480px) {
        .hero-title {
            font-size: 2rem;
        }

        .hero-subtitle {
            font-size: 1rem;
        }
    }

    .hero-subtitle {
        font-size: 1.3rem;
        color: #CBD5E1;
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
        line-height: 1.6;
    }

    .cta-button {
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.3s;
        text-decoration: none;
        display: inline-block;
        margin-top: 1rem;
    }

    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
    }

    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        width: 100%;
    }

    .feature-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #475569;
        transition: transform 0.3s;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        border-color: #8B5CF6;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        color: #CBD5E1;
        line-height: 1.6;
    }

    /* Benefits section */
    .benefits-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 3rem 2rem;
        margin: 3rem 0;
        border-radius: 16px;
        border: 1px solid #334155;
        width: 100%;
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #F8FAFC;
        text-align: center;
        margin-bottom: 2rem;
    }

    .benefit-item {
        display: flex;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #334155;
    }

    .benefit-icon {
        font-size: 1.5rem;
        margin-right: 1rem;
        min-width: 2rem;
    }

    .benefit-text {
        color: #CBD5E1;
        font-size: 1.1rem;
    }
    </style>

    <!-- Navigation -->
    <div class="nav-container">
        <div class="nav-logo">
            🚀 OPSINTEL
        </div>
        <div class="nav-links">
            <div class="nav-link active">Home</div>
            <div class="nav-link">Dashboard</div>
            <div class="nav-link">AI Insights</div>
            <div class="nav-link">Forecasting</div>
            <div class="nav-link">Upload Data</div>
        </div>
    </div>

    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Home</h1>
        <p class="hero-subtitle">Transform spreadsheets into smart business decisions. Get AI-powered insights that identify profit opportunities, reduce costs, and predict your next best move.</p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: #8B5CF6; font-weight: 700;">85%</div>
                <div style="color: #CBD5E1; font-size: 0.9rem;">Average profit increase</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: #8B5CF6; font-weight: 700;">3 min</div>
                <div style="color: #CBD5E1; font-size: 0.9rem;">Setup time</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: #8B5CF6; font-weight: 700;">24/7</div>
                <div style="color: #CBD5E1; font-size: 0.9rem;">Business monitoring</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main CTA button - moved to top as requested
    if st.button("🚀 Analyze My Business", type="primary", use_container_width=True):
        st.switch_page("pages/2_📊_Data_Upload.py")

    # Features section with modern cards
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">AI Recommendations</div>
            <div class="feature-desc">Upload sales, expenses, and inventory files</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Sales Data</div>
            <div class="feature-desc">Revenue & profit tracking with performance trending</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Expenses Data</div>
            <div class="feature-desc">Cost optimization alerts and expense analysis</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📦</div>
            <div class="feature-title">Inventory Data</div>
            <div class="feature-desc">Stock management and reorder recommendations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI Recommendations section
    st.markdown("""
    <div class="benefits-container">
        <h2 class="section-title">🤖 AI Recommendations</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
            <div>
                <h3 style="color: #8B5CF6; margin-bottom: 1rem;">Revenue Growth Strategy</h3>
                <p style="color: #CBD5E1;">Invest more in your top performing product line</p>
            </div>
            <div>
                <h3 style="color: #8B5CF6; margin-bottom: 1rem;">Reduce Operating Costs</h3>
                <p style="color: #CBD5E1;">Renegotiate supplier contracts to save expenses</p>
            </div>
            <div>
                <h3 style="color: #8B5CF6; margin-bottom: 1rem;">Cash Flow</h3>
                <p style="color: #CBD5E1;">Optimize inventory levels for better cash flow</p>
            </div>
            <div>
                <h3 style="color: #8B5CF6; margin-bottom: 1rem;">Restock Alert</h3>
                <p style="color: #CBD5E1;">Product example, today recommends end soon</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Inventory Management section
    st.markdown("""
    <div class="benefits-container">
        <h2 class="section-title">📦 Inventory Management</h2>
        <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; background: #1E293B; border-radius: 12px;">
                <thead>
                    <tr style="background: #334155;">
                        <th style="padding: 1rem; color: #F8FAFC; text-align: left;">Product</th>
                        <th style="padding: 1rem; color: #F8FAFC; text-align: center;">Current Stock</th>
                        <th style="padding: 1rem; color: #F8FAFC; text-align: center;">Reorder Level</th>
                        <th style="padding: 1rem; color: #F8FAFC; text-align: center;">Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #475569;">
                        <td style="padding: 1rem; color: #CBD5E1;">📱 Product A</td>
                        <td style="padding: 1rem; color: #CBD5E1; text-align: center;">25</td>
                        <td style="padding: 1rem; color: #CBD5E1; text-align: center;">20</td>
                        <td style="padding: 1rem; text-align: center;"><span style="background: #059669; color: white; padding: 0.25rem 0.75rem; border-radius: 6px;">✓</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #475569;">
                        <td style="padding: 1rem; color: #CBD5E1;">📊 Product B</td>
                        <td style="padding: 1rem; color: #CBD5E1; text-align: center;">8</td>
                        <td style="padding: 1rem; color: #CBD5E1; text-align: center;">10</td>
                        <td style="padding: 1rem; text-align: center;"><span style="background: #DC2626; color: white; padding: 0.25rem 0.75rem; border-radius: 6px;">Low</span></td>
                    </tr>
                    <tr>
                        <td style="padding: 1rem; color: #CBD5E1;">🏢 Product C</td>
                        <td style="padding: 1rem; color: #CBD5E1; text-align: center;">12</td>
                        <td style="padding: 1rem; color: #CBD5E1; text-align: center;">15</td>
                        <td style="padding: 1rem; text-align: center;"><span style="background: #059669; color: white; padding: 0.25rem 0.75rem; border-radius: 6px;">✓</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Scenario Analysis section
    st.markdown("""
    <div class="benefits-container">
        <h2 class="section-title">🔮 Scenario Analysis</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <div>
                <h3 style="color: #8B5CF6; margin-bottom: 1rem;">Revenue Forecast</h3>
                <div style="background: #334155; padding: 1.5rem; border-radius: 12px; height: 200px; display: flex; align-items: center; justify-content: center;">
                    <div style="color: #CBD5E1; text-align: center;">
                        📈 Interactive forecasting chart would appear here
                    </div>
                </div>
                <p style="color: #CBD5E1; margin-top: 1rem;">Scenario B suggests the optimal forecast strategy</p>
            </div>
            <div>
                <h3 style="color: #8B5CF6; margin-bottom: 1rem;">View Recommendations</h3>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div style="background: #334155; padding: 1rem; border-radius: 8px;">
                        <strong style="color: #F8FAFC;">Revenue Growth Strategy</strong>
                        <p style="color: #CBD5E1; margin: 0.5rem 0 0 0;">Increase in your top performing category</p>
                    </div>
                    <div style="background: #334155; padding: 1rem; border-radius: 8px;">
                        <strong style="color: #F8FAFC;">Reduce Operating Costs</strong>
                        <p style="color: #CBD5E1; margin: 0.5rem 0 0 0;">Renegotiate supplier contracts to save expenses</p>
                    </div>
                    <div style="background: #334155; padding: 1rem; border-radius: 8px;">
                        <strong style="color: #F8FAFC;">Cash Flow</strong>
                        <p style="color: #CBD5E1; margin: 0.5rem 0 0 0;">Optimize inventory levels for better cash flow</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Data status indicator (minimal)
    data_processor = st.session_state.data_processor
    has_data = (
        (hasattr(data_processor, 'sales_data') and data_processor.sales_data is not None) or
        (hasattr(data_processor, 'expenses_data') and data_processor.expenses_data is not None) or
        (hasattr(data_processor, 'inventory_data') and data_processor.inventory_data is not None)
    )

    if has_data:
        st.success("✅ Business data loaded - You can now explore full analytics!")

if __name__ == "__main__":
    main()