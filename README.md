# Amazon Customer Service Dashboard

A Streamlit dashboard for analyzing Amazon customer service data, created for B BUS 441 A at the University of Washington.

## Features

- **Data Table**: View and explore customer service data
- **CSAT Snapshot**: Customer satisfaction score visualizations
- **Employee Mirror Metrics**: Employee performance metrics
- **Heatmap**: Visual representation of data correlations
- **AI Chat Assistant**: OpenAI-powered chatbot for dashboard assistance

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure OpenAI API key in Streamlit Cloud secrets:
   - Add `OPENAI_API_KEY` to your Streamlit Cloud app secrets

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py` - Main dashboard application
- `chatbot.py` - AI chat assistant implementation
- `exploratory_data_analysis_2.py` - Data analysis and visualization functions
- `heatmap.py` - Heatmap visualization component
- `mirrored_bar_chart.py` - Employee metrics visualization
- `table_tab.py` - Data table display component
- `data/` - Contains the raw Amazon customer service data
- `system_messages/` - System prompts for the AI assistant

## Team

**Professor**: Nick Cuhaciyan, University of Washington

**Team Members**: Ahmed Mohamad, Cyrus Cheng, Daniel Kulik, Erik Lars Knudsen, Gavin Fisher Detert, Osvaldo Flores, Teyonna Fegler, Trevon Sorlin Gagnon