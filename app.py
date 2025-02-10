# Version 1.0.0 - UTM Generator for Keboola
import streamlit as st
import json
from urllib.parse import urlparse, urlencode

# Constants
FISCAL_YEARS = ['FY24', 'FY25', 'FY26']
QUARTERS = ['Q1', 'Q2', 'Q3', 'Q4']
GEOS = ['US', 'UK', 'CEE', 'RoW']

LEAD_SOURCE_DATA = [
    {"group": "Marketing", "category": "Inbound - Product", "source": "PAYG GCP"},
    {"group": "Marketing", "category": "Inbound - Product", "source": "PAYG Azure"},
    {"group": "Marketing", "category": "Inbound - Product", "source": "PAYG AWS"},
    {"group": "Marketing", "category": "Inbound - Product", "source": "Demo Project"},
    {"group": "Marketing", "category": "Inbound - Product", "source": "Feature Request"},
    {"group": "Marketing", "category": "Events", "source": "Empower"},
    {"group": "Marketing", "category": "Events", "source": "Trade Show"},
    {"group": "Marketing", "category": "Events", "source": "Meetup/Community"},
    {"group": "Marketing", "category": "Events", "source": "Partner Event"},
    {"group": "Marketing", "category": "Events", "source": "Webinar"},
    {"group": "Marketing", "category": "Events", "source": "Workshop"},
    {"group": "Marketing", "category": "Events", "source": "CXO"},
    {"group": "Marketing", "category": "Website", "source": "Contact Form"},
    {"group": "Marketing", "category": "Website", "source": "Newsletter"},
    {"group": "Marketing", "category": "Website", "source": "Qualified Website"},
    {"group": "Marketing", "category": "Website", "source": "Integration Request"},
    {"group": "Marketing", "category": "Website", "source": "Gated Content"},
    {"group": "Marketing", "category": "Website", "source": "Expert Program"},
    {"group": "Marketing", "category": "Website", "source": "Webinar on Demand"},
    {"group": "Marketing", "category": "Website", "source": "User Review"},
    {"group": "Marketing", "category": "Website", "source": "Developer Portal"},
    {"group": "Marketing", "category": "Digital", "source": "Typeform"},
    {"group": "Marketing", "category": "Digital", "source": "LinkedIn"},
    {"group": "Marketing", "category": "Digital", "source": "Unbounce"},
    {"group": "Marketing", "category": "Digital", "source": "Trumpet"},
    {"group": "Marketing", "category": "Digital", "source": "Google Ads"},
    {"group": "Marketing", "category": "Digital", "source": "Bing"},
    {"group": "Marketing", "category": "Digital", "source": "Reddit"},
    {"group": "Marketing", "category": "Digital", "source": "Facebook"},
    {"group": "Marketing", "category": "Digital", "source": "Customer.io"},
    {"group": "Partners", "category": "Partner Connect", "source": "Snowflake Partner Connect"},
    {"group": "Partners", "category": "Marketplace", "source": "Azure Marketplace"},
    {"group": "Partners", "category": "Marketplace", "source": "Google Marketplace"},
    {"group": "Partners", "category": "Referral", "source": "Partner Referral"},
    {"group": "Product", "category": "Education", "source": "Academy"},
    {"group": "Sales", "category": "AE Outbound", "source": "Apollo"},
    {"group": "Sales", "category": "AE Outbound", "source": "Cognism"},
    {"group": "Sales", "category": "AE Outbound", "source": "Outreach Calendar"},
    {"group": "Sales", "category": "BDR Outbound", "source": "Direct"},
    {"group": "Sales", "category": "BDR Outbound", "source": "Apollo"},
    {"group": "Sales", "category": "BDR Outbound", "source": "Cognism"},
    {"group": "Sales", "category": "BDR Outbound", "source": "Lusha"},
]

def get_unique_groups():
    return list(set(item["group"] for item in LEAD_SOURCE_DATA))

def get_categories_for_group(group):
    return list(set(item["category"] for item in LEAD_SOURCE_DATA if item["group"] == group))

def get_sources_for_category(group, category):
    return list(set(item["source"] for item in LEAD_SOURCE_DATA if item["group"] == group and item["category"] == category))

def generate_salesforce_campaign_name(fiscal_year, quarter, geo, group, category, source, campaign_name):
    formatted_campaign_name = campaign_name.replace(" ", "_")
    return f"{fiscal_year}_{quarter}_{geo}_{group}_{category}_{source}_{formatted_campaign_name}"

def generate_utm_url(base_url, utm_params):
    try:
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme:
            base_url = "https://" + base_url
            parsed_url = urlparse(base_url)
        
        # Filter out empty UTM parameters
        utm_params = {k: v for k, v in utm_params.items() if v}
        
        # Create query string
        query = urlencode(utm_params)
        
        # Combine URL with UTM parameters
        if parsed_url.query:
            return f"{base_url}&{query}"
        else:
            return f"{base_url}?{query}"
    except Exception as e:
        st.error(f"Error generating URL: {str(e)}")
        return None

def load_stored_values():
    return json.loads(st.session_state.get('stored_values', '[]'))

def save_stored_values(values):
    st.session_state['stored_values'] = json.dumps(values)

def main():
    st.set_page_config(page_title="Naming Convention and UTM Generator", layout="wide")
    
    st.title("Naming Convention and UTM Generator")
    st.write("Generate and store Salesforce Campaign Names and UTM URLs")
    
    # Instructions
    with st.expander("How to use"):
        st.markdown("""
        1. **Generate or Use Existing Campaign Name:**
           - If you do not have an SF Campaign Name, use the Campaign Generator to create one
           - Generate and copy this name into Salesforce to set up your campaign
           - If you have questions contact: peter.perzo@keboola.com
           
        2. **URL Generator with UTMs:**
           - Enter the destination link and UTM parameters
           - Click Generate URL to create the UTM link
           
        3. Use Save Generated Values to store for future reference
        
        4. View and manage saved campaigns in the Stored Values section
        
        **When to Use UTMs:**
        Use UTMs whenever you are linking from a non-webpage source (e.g., email, social media, etc.) 
        to a Keboola web page and want to track traffic and conversions for that specific segment.
        """)
    
    # Create tabs
    tab1, tab2 = st.tabs(["Generate Campaign Name", "Use Existing Campaign Name"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fiscal_year = st.selectbox("Fiscal Year", FISCAL_YEARS, key="fiscal_year")
        with col2:
            quarter = st.selectbox("Quarter", QUARTERS, key="quarter")
        
        geo = st.selectbox("Geo", GEOS, key="geo")
        
        # Lead Source Selection
        lead_source_group = st.selectbox("Lead Source Group", get_unique_groups(), key="lead_source_group")
        
        if lead_source_group:
            categories = get_categories_for_group(lead_source_group)
            lead_source_category = st.selectbox("Lead Source Category", categories, key="lead_source_category")
            
            if lead_source_category:
                sources = get_sources_for_category(lead_source_group, lead_source_category)
                lead_source = st.selectbox("Lead Source", sources, key="lead_source")
        
        campaign_name = st.text_input("Campaign Name", key="campaign_name")
        
        if all([fiscal_year, quarter, geo, lead_source_group, lead_source_category, lead_source, campaign_name]):
            if st.button("Generate Salesforce Campaign Name"):
                sf_campaign_name = generate_salesforce_campaign_name(
                    fiscal_year, quarter, geo, lead_source_group, 
                    lead_source_category, lead_source, campaign_name
                )
                st.session_state['generated_campaign_name'] = sf_campaign_name
                st.code(sf_campaign_name)
    
    with tab2:
        existing_campaign_name = st.text_input(
            "Existing Salesforce Campaign Name",
            key="existing_campaign_name"
        )
        if existing_campaign_name:
            st.session_state['generated_campaign_name'] = existing_campaign_name
    
    # UTM Parameters Section
    st.divider()
    st.subheader("UTM Parameters")
    
    destination_link = st.text_input("Destination Link", placeholder="https://www.keboola.com")
    
    utm_campaign = st.text_input("UTM Campaign", 
                                value=st.session_state.get('generated_campaign_name', ''),
                                placeholder="UTM Campaign")
    
    utm_source = st.text_input("UTM Source", placeholder="e.g. google, newsletter")
    utm_medium = st.text_input("UTM Medium", placeholder="e.g. cpc, banner, email")
    utm_term = st.text_input("UTM Term", placeholder="Identify the paid keywords")
    utm_content = st.text_input("UTM Content", placeholder="Use to differentiate ads")
    
    if st.button("Generate URL"):
        if not destination_link:
            st.error("Please enter a destination link")
        else:
            utm_params = {
                'utm_campaign': utm_campaign,
                'utm_source': utm_source,
                'utm_medium': utm_medium,
                'utm_term': utm_term,
                'utm_content': utm_content
            }
            
            generated_url = generate_utm_url(destination_link, utm_params)
            if generated_url:
                st.session_state['generated_url'] = generated_url
                st.code(generated_url)
                
                # Save functionality
                if st.session_state.get('generated_campaign_name'):
                    # Move the button outside the if block to prevent nested buttons
                    st.session_state['show_save_button'] = True

    # Move save button outside the Generate URL block
    if st.session_state.get('show_save_button', False):
        if st.button("💾 Save Generated Values", key="save_button"):
            stored_values = load_stored_values()
            new_value = {
                'id': str(len(stored_values)),
                'campaignName': st.session_state['generated_campaign_name'],
                'url': st.session_state['generated_url']
            }
            stored_values.append(new_value)
            save_stored_values(stored_values)
            st.success("Values saved successfully!")
            # Reset the save button state
            st.session_state['show_save_button'] = False
            st.rerun()
    
    # Stored Values Section
    st.divider()
    if st.checkbox("Show Stored Values"):
        stored_values = load_stored_values()
        if stored_values:
            for idx, value in enumerate(stored_values):
                with st.expander(f"Campaign {idx + 1}"):
                    st.write("**Campaign Name:**")
                    st.code(value['campaignName'])
                    
                    st.write("**Generated URL:**")
                    st.code(value['url'])
                    
                    if st.button("🗑️ Remove", key=f"remove_{idx}"):
                        stored_values.pop(idx)
                        save_stored_values(stored_values)
                        st.rerun()
        else:
            st.write("No stored values available.")

if __name__ == "__main__":
    main()
