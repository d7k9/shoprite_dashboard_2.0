import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64 # Import base64
import os


# Data extracted from the surveys
# SA = South Africa, ZM = Zambia

survey_data = {
    'SA': {
        'store_info': {
            'name': 'Shoprite Bridgetown, CapeTown',
            'country': 'South Africa'
        },
        'strategic_intent': {
            'reflects_logo_slogan': 'Yes', # Yes
            'staff_projects_vision': 4 # Likert 1-5 (4)
        },
        'brands_available': {
            'Supermarket': True, 'Furniture (OK)': False, 'Ticketing (Computicket)': False,
            'Logistics (Branded trucks)': False, 'Hospitality (CFS)': False, 'Fresh produce (Freshmark)': True,
            'Franchise (OK)': False, 'Cellular service (k\'nect)': True, 'Liquors (Liquorshop)': True,
            'Financial services (Money Market)': True, 'Pharmaceuticals (Medirite/Transfarm)': False
        },
        'going_green': {
            'Recycling of shopping bags': 1,
            'Sustainable energy source (Solar panels)': 3,
            'Management of food losses and waste': 2,
            'Reusing and recycling packaging material': 2,
            'Other initiatives (text)': None # No specific text provided for "Any other initiatives" just rank 2
        },
        'csr': {
            'evidence_found': 'No', # No
            'initiative_description': None
        },
        'organisational_structure': {
            'management_photos_displayed': 'No' # No
        },
        'culture': {
            'customer_relations_person_at_entrance': 'Yes', # Yes
            'celebrate_employee_of_month': 'No', # No
            'staff_displays_corporate_image_dress_code': 4, # Likert 1-5 (4)
            'celebration_theme_sport_cultural_religious': 'No' # No
        },
        'marketing_store_appearance': {
            'lowest_price_special_in_stock_marked': 5, # Likert 1-5 (5)
            'Signage and Information': 'Adequate',
            'Cleanliness': 'Clean',
            'Stock Levels': 'Full Shelves',
            'Maintaining the Cold Chain': 'Correct Temperature',
            'Meat and Fresh Produce': 'Fresh'
        },
        'customer_experience': { # Scale 1 (Bad) to 5 (Good)
            'Welcoming Upon Entry': 2.5, # Estimated from checkmark position (between 2 and 3)
            'Store Layout': 4,
            'Signage': 4,
            'Enquiries To Staff': 5,
            'Till Checkout': 4
        },
        'group_statements': {
            'private_label_products_visible': 5, # Likert 1-5 (5)
            'shelf_stocking': 'Shelves consistently full and well-managed'
        },
        'price_comparison': { # Prices in ZAR
            'Bread': {'Shoprite': 12.99, 'Pick n Pay': 12.99, 'Food Lover\'s': 16.00, 'Woolworths': 20.99},
            'Rice (1Kg)': {'Shoprite': 38.99, 'Pick n Pay': 37.99, 'Food Lover\'s': 33.99, 'Woolworths': 20.99},
            'Oil (2ltr)': {'Shoprite': 79.99, 'Pick n Pay': 68.99, 'Food Lover\'s': 64.99, 'Woolworths': 49.99}
        }
    },
    'ZM': {
        'store_info': {
            'name': 'Shoprite Mandahill Mall, Lusaka',
            'country': 'Zambia'
        },
        'strategic_intent': {
            'reflects_logo_slogan': 'Yes', # Yes
            'staff_projects_vision': 3 # Likert 1-5 (3)
        },
        'brands_available': {
            'Supermarket': True, 'Furniture (OK)': False, 'Ticketing (Computicket)': True,
            'Logistics (Branded trucks)': False, 'Hospitality (CFS)': False, 'Fresh produce (Freshmark)': True,
            'Franchise (OK)': False, 'Cellular service (k\'nect)': False, 'Liquors (Liquorshop)': True,
            'Financial services (Money Market)': True, 'Pharmaceuticals (Medirite/Transfarm)': False
        },
        'going_green': {
            'Recycling of shopping bags': 1,
            'Sustainable energy source (Solar panels)': 2,
            'Management of food losses and waste': 2,
            'Reusing and recycling packaging material': 1,
            'Other initiatives (text)': "Prioritization of organic products that are certified by environmental standards was shown by product labelling." # Rank 1
        },
        'csr': {
            'evidence_found': 'Yes', # Yes
            'initiative_description': 'Observed new employees receiving hands-on training and guidance from experienced staff members, demonstrating a strong commitment to skills development and knowledge sharing in the workplace.'
        },
        'organisational_structure': {
            'management_photos_displayed': 'Yes' # Yes
        },
        'culture': {
            'customer_relations_person_at_entrance': 'Yes', # Yes
            'celebrate_employee_of_month': 'Yes', # Yes
            'staff_displays_corporate_image_dress_code': 5, # Likert 1-5 (5)
            'celebration_theme_sport_cultural_religious': 'No' # No
        },
        'marketing_store_appearance': {
            'lowest_price_special_in_stock_marked': 5, # Likert 1-5 (5)
            'Signage and Information': 'Adequate',
            'Cleanliness': 'Clean',
            'Stock Levels': 'Full Shelves',
            'Maintaining the Cold Chain': 'Correct Temperature',
            'Meat and Fresh Produce': 'Fresh'
        },
        'customer_experience': { # Scale 1 (Bad/non-compliant) to 5 (Good/compliant) - ZM uses X for selection.
                                  # Welcoming: X on 4; Store Layout: X on 2; Signage: X on 5; Enquiries: X on 3; Till Checkout: X on 2
            'Welcoming Upon Entry': 4,
            'Store Layout': 2,
            'Signage': 5,
            'Enquiries To Staff': 3,
            'Till Checkout': 2
        },
        'group_statements': {
            'private_label_products_visible': 5, # Likert 1-5 (5)
            'shelf_stocking': 'Shelves consistently full and well-managed'
        },
        'price_comparison': { # Prices given with "R", assumed to be relative comparison units or ZMW intended. Using as given.
            'Bread': {'Shoprite': 16.77, 'Pick n Pay': 16.77, 'Food Lover\'s': 17.78, 'Woolworths': 19.12},
            'Rice (1Kg)': {'Shoprite': 26.83, 'Pick n Pay': 114.06, 'Food Lover\'s': 127.47, 'Woolworths': 135.53},
            'Oil (2ltr)': {'Shoprite': 100.63, 'Pick n Pay': 111.37, 'Food Lover\'s': 118.08, 'Woolworths': 130.83}
        }
    }
}

# Define positive mapping for store appearance
positive_appearance_map = {
    'Signage and Information': 'Adequate',
    'Cleanliness': 'Clean',
    'Stock Levels': 'Full Shelves',
    'Maintaining the Cold Chain': 'Correct Temperature',
    'Meat and Fresh Produce': 'Fresh'
}


# --- Data (Copy the survey_data dictionary and positive_appearance_map from above here) ---
survey_data = {
    'SA': {
        'store_info': {
            'name': 'Shoprite Bridgetown, CapeTown',
            'country': 'South Africa'
        },
        'strategic_intent': {
            'reflects_logo_slogan': 'Yes', # Yes
            'staff_projects_vision': 4 # Likert 1-5 (4)
        },
        'brands_available': {
            'Supermarket': True, 'Furniture (OK)': False, 'Ticketing (Computicket)': False,
            'Logistics (Branded trucks)': False, 'Hospitality (CFS)': False, 'Fresh produce (Freshmark)': True,
            'Franchise (OK)': False, 'Cellular service (k\'nect)': True, 'Liquors (Liquorshop)': True,
            'Financial services (Money Market)': True, 'Pharmaceuticals (Medirite/Transfarm)': False
        },
        'going_green': {
            'Recycling of shopping bags': 1,
            'Sustainable energy source (Solar panels)': 3,
            'Management of food losses and waste': 2,
            'Reusing and recycling packaging material': 2,
            'Other initiatives (text)': None # No specific text provided for "Any other initiatives" just rank 2
        },
        'csr': {
            'evidence_found': 'No', # No
            'initiative_description': None
        },
        'organisational_structure': {
            'management_photos_displayed': 'No' # No
        },
        'culture': {
            'customer_relations_person_at_entrance': 'Yes', # Yes
            'celebrate_employee_of_month': 'No', # No
            'staff_displays_corporate_image_dress_code': 4, # Likert 1-5 (4)
            'celebration_theme_sport_cultural_religious': 'No' # No
        },
        'marketing_store_appearance': {
            'lowest_price_special_in_stock_marked': 5, # Likert 1-5 (5)
            'Signage and Information': 'Adequate',
            'Cleanliness': 'Clean',
            'Stock Levels': 'Full Shelves',
            'Maintaining the Cold Chain': 'Correct Temperature',
            'Meat and Fresh Produce': 'Fresh'
        },
        'customer_experience': { # Scale 1 (Bad) to 5 (Good)
            'Welcoming Upon Entry': 2.5, # Estimated from checkmark position (between 2 and 3)
            'Store Layout': 4,
            'Signage': 4,
            'Enquiries To Staff': 5,
            'Till Checkout': 4
        },
        'group_statements': {
            'private_label_products_visible': 5, # Likert 1-5 (5)
            'shelf_stocking': 'Shelves consistently full and well-managed'
        },
        'price_comparison': { # Prices in ZAR
            'Bread': {'Shoprite': 12.99, 'Pick n Pay': 12.99, 'Food Lover\'s': 16.00, 'Woolworths': 20.99},
            'Rice (1Kg)': {'Shoprite': 38.99, 'Pick n Pay': 37.99, 'Food Lover\'s': 33.99, 'Woolworths': 20.99},
            'Oil (2ltr)': {'Shoprite': 79.99, 'Pick n Pay': 68.99, 'Food Lover\'s': 64.99, 'Woolworths': 49.99}
        }
    },
    'ZM': {
        'store_info': {
            'name': 'Shoprite Mandahill Mall, Lusaka',
            'country': 'Zambia'
        },
        'strategic_intent': {
            'reflects_logo_slogan': 'Yes', # Yes
            'staff_projects_vision': 3 # Likert 1-5 (3)
        },
        'brands_available': {
            'Supermarket': True, 'Furniture (OK)': False, 'Ticketing (Computicket)': True,
            'Logistics (Branded trucks)': False, 'Hospitality (CFS)': False, 'Fresh produce (Freshmark)': True,
            'Franchise (OK)': False, 'Cellular service (k\'nect)': False, 'Liquors (Liquorshop)': True,
            'Financial services (Money Market)': True, 'Pharmaceuticals (Medirite/Transfarm)': False
        },
        'going_green': {
            'Recycling of shopping bags': 1,
            'Sustainable energy source (Solar panels)': 2,
            'Management of food losses and waste': 2,
            'Reusing and recycling packaging material': 1,
            'Other initiatives (text)': "Prioritization of organic products that are certified by environmental standards was shown by product labelling." # Rank 1
        },
        'csr': {
            'evidence_found': 'Yes', # Yes
            'initiative_description': 'Observed new employees receiving hands-on training and guidance from experienced staff members, demonstrating a strong commitment to skills development and knowledge sharing in the workplace.'
        },
        'organisational_structure': {
            'management_photos_displayed': 'Yes' # Yes
        },
        'culture': {
            'customer_relations_person_at_entrance': 'Yes', # Yes
            'celebrate_employee_of_month': 'Yes', # Yes
            'staff_displays_corporate_image_dress_code': 5, # Likert 1-5 (5)
            'celebration_theme_sport_cultural_religious': 'No' # No
        },
        'marketing_store_appearance': {
            'lowest_price_special_in_stock_marked': 5, # Likert 1-5 (5)
            'Signage and Information': 'Adequate',
            'Cleanliness': 'Clean',
            'Stock Levels': 'Full Shelves',
            'Maintaining the Cold Chain': 'Correct Temperature',
            'Meat and Fresh Produce': 'Fresh'
        },
        'customer_experience': { # Scale 1 (Bad/non-compliant) to 5 (Good/compliant) - ZM uses X for selection.
            'Welcoming Upon Entry': 4,
            'Store Layout': 2,
            'Signage': 5,
            'Enquiries To Staff': 3,
            'Till Checkout': 2
        },
        'group_statements': {
            'private_label_products_visible': 5, # Likert 1-5 (5)
            'shelf_stocking': 'Shelves consistently full and well-managed'
        },
        'price_comparison': { # Prices given with "R", assumed to be relative comparison units or ZMW intended. Using as given.
            'Bread': {'Shoprite': 16.77, 'Pick n Pay': 16.77, 'Food Lover\'s': 17.78, 'Woolworths': 19.12},
            'Rice (1Kg)': {'Shoprite': 26.83, 'Pick n Pay': 114.06, 'Food Lover\'s': 127.47, 'Woolworths': 135.53},
            'Oil (2ltr)': {'Shoprite': 100.63, 'Pick n Pay': 111.37, 'Food Lover\'s': 118.08, 'Woolworths': 130.83}
        }
    }
}

positive_appearance_map = {
    'Signage and Information': 'Adequate',
    'Cleanliness': 'Clean',
    'Stock Levels': 'Full Shelves',
    'Maintaining the Cold Chain': 'Correct Temperature',
    'Meat and Fresh Produce': 'Fresh'
}
# --- END OF DATA ---

# --- Call the function to set background (AFTER st.set_page_config and data definition) ---

st.set_page_config(layout="wide")
st.title("🛒 Unobtrusive Survey Insights: Shoprite Zambia & South Africa")

# --- SIDEBAR ---
st.sidebar.header("Display Options")
country_options = ["Both", "South Africa", "Zambia"]
selected_country_option = st.sidebar.selectbox("Select Country/Comparison:", country_options)

if selected_country_option == "South Africa":
    countries_to_display = ['SA']
elif selected_country_option == "Zambia":
    countries_to_display = ['ZM']
else:
    countries_to_display = ['SA', 'ZM']

# --- Helper function to get data for selected countries ---
def get_selected_data(data_dict_key, sub_key=None):
    plot_data = []
    for country_code in countries_to_display:
        country_name = survey_data[country_code]['store_info']['country']
        if sub_key:
            value = survey_data[country_code][data_dict_key][sub_key]
        else:
            value = survey_data[country_code][data_dict_key]
        plot_data.append({'Country': country_name, 'Value': value, 'Code': country_code})
    return pd.DataFrame(plot_data)

# --- SECTIONS ---

# 1. STRATEGIC INTENT
st.header("🎯 Strategic Intent")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Store Reflects Logo & Slogan")
    intent_data = []
    for country_code in countries_to_display:
        intent_data.append({
            'Country': survey_data[country_code]['store_info']['country'],
            'Response': survey_data[country_code]['strategic_intent']['reflects_logo_slogan']
        })
    intent_df = pd.DataFrame(intent_data)
    
    if not intent_df.empty:
        # Count Yes/No responses for each country
        count_df = intent_df.groupby(['Country', 'Response']).size().reset_index(name='Count')
        fig = px.bar(count_df, x="Country", y="Count", color="Response", barmode="group",
                     title="Store Reflects Logo & Slogan?",
                     color_discrete_map={'Yes': 'green', 'No': 'red'},
                     labels={'Count': 'Number of Stores (1 per country in this dataset)'})
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Staff Projects Vision, Mission & Values")
    staff_vision_data = []
    for country_code in countries_to_display:
        staff_vision_data.append({
            'Country': survey_data[country_code]['store_info']['country'],
            'Rating': survey_data[country_code]['strategic_intent']['staff_projects_vision']
        })
    staff_vision_df = pd.DataFrame(staff_vision_data)
    if not staff_vision_df.empty:
        fig = px.bar(staff_vision_df, x="Country", y="Rating", color="Country",
                     title="Staff Projection of Vision (1-5 Scale)",
                     labels={'Rating': 'Average Rating (1=Strongly Disagree, 5=Strongly Agree)'},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(yaxis=dict(range=[0, 5.5]))
        st.plotly_chart(fig, use_container_width=True)

# 2. BRANDS AVAILABLE
st.header("🏪 Brands Available")
brand_list = list(survey_data['SA']['brands_available'].keys()) # Get all possible brands from one entry
selected_brands_sidebar = st.sidebar.multiselect(
    "Select Brands to Display:",
    options=brand_list,
    default=brand_list[:5] # Default to first 5 brands
)

if selected_brands_sidebar:
    brands_data = []
    for country_code in countries_to_display:
        for brand in selected_brands_sidebar:
            available = survey_data[country_code]['brands_available'].get(brand, False)
            brands_data.append({
                'Country': survey_data[country_code]['store_info']['country'],
                'Brand': brand,
                'Available': 1 if available else 0,
                'Status': 'Available' if available else 'Not Available'
            })
    brands_df = pd.DataFrame(brands_data)

    if not brands_df.empty:
        fig = px.bar(brands_df, x="Brand", y="Available", color="Country", barmode="group",
                     title="Availability of Selected Shoprite Brands",
                     labels={"Available": "Available (1=Yes, 0=No)"},
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_yaxes(tickvals=[0, 1], ticktext=['No', 'Yes'])
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Select brands from the sidebar to display.")


# 3. GOING GREEN PHILOSOPHY
st.header("🌿 Going Green Philosophy")
st.sidebar.markdown("---")
st.sidebar.subheader("Going Green Options")
gg_initiatives = list(survey_data['SA']['going_green'].keys())
# Ensure 'Other initiatives (text)' is handled correctly if it exists
if 'Other initiatives (text)' in gg_initiatives:
    gg_initiatives.remove('Other initiatives (text)')

gg_data = []
for country_code in countries_to_display:
    country_name = survey_data[country_code]['store_info']['country']
    for initiative in gg_initiatives:
        # Ensure the initiative exists for the country before accessing
        rank = survey_data[country_code]['going_green'].get(initiative)
        if rank is not None: # Add this check
            gg_data.append({'Country': country_name, 'Initiative': initiative, 'Rank': rank})

if gg_data:
    gg_df = pd.DataFrame(gg_data)
    fig = go.Figure()
    # Using a dictionary for colors to ensure consistency if a country is deselected
    country_colors = {
        'South Africa': 'rgba(70,180,70,0.8)', # A slightly brighter green
        'Zambia': 'rgba(255,165,0,0.8)' # A standard orange
    }

    # Check if gg_df['Country'] is not empty before iterating
    if not gg_df.empty:
        for country in gg_df['Country'].unique():
            country_specific_df = gg_df[gg_df['Country'] == country]
            fig.add_trace(go.Scatterpolar(
                r=country_specific_df['Rank'],
                theta=country_specific_df['Initiative'],
                fill='toself',
                name=country,
                line_color=country_colors.get(country, 'rgba(128,128,128,0.7)') # Default to grey
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3.5], # Rank is 1, 2, 3. Extend slightly.
                tickvals=[1, 2, 3],
                ticktext=['Most Evidence', 'Some Evidence', 'No Evidence'],
                angle=90, # Start ticks at the top
                tickfont=dict(color='white'), # Make tick labels white for better contrast on dark bg
                gridcolor='lightgrey', # Make grid lines lighter for visibility
                linecolor='lightgrey' # Radial axis line color
            ),
            angularaxis=dict(
                tickfont=dict(color='white'), # Make angular labels white
                linecolor='lightgrey' # Angular axis line color
            ),
            bgcolor='darkgrey', # Set the background color of the polar area
        ),
        showlegend=True,
        title="Going Green Initiatives (Lower Rank = More Evidence)",
        paper_bgcolor='rgba(0,0,0,0)', # Transparent background for the overall chart paper
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background for the plot area outside polar
        legend=dict(font=dict(color='white')) # Ensure legend text is readable if not on dark bg
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("Other Initiatives Noted:")
    for country_code in countries_to_display:
        # Check if 'Other initiatives (text)' exists in the country's data
        other_text = survey_data[country_code]['going_green'].get('Other initiatives (text)')
        if other_text:
            st.write(f"**{survey_data[country_code]['store_info']['country']}:** {other_text}")
else:
    st.write("No 'Going Green' data to display for the selected country/countries.")

# 4. CORPORATE SOCIAL RESPONSIBILITY (CSR)
st.header("🤝 Corporate Social Responsibility")
csr_data = []
for country_code in countries_to_display:
    csr_data.append({
        'Country': survey_data[country_code]['store_info']['country'],
        'Evidence Found': survey_data[country_code]['csr']['evidence_found'],
        'Initiative': survey_data[country_code]['csr']['initiative_description']
    })
csr_df = pd.DataFrame(csr_data)

if not csr_df.empty:
    count_df = csr_df.groupby(['Country', 'Evidence Found']).size().reset_index(name='Count')
    fig = px.bar(count_df, x="Country", y="Count", color="Evidence Found",
                 barmode="group", title="Evidence of CSR Initiatives",
                 color_discrete_map={'Yes': 'purple', 'No': 'lightgrey'},
                 labels={'Count': 'Observation (1 per store)'})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("CSR Initiative Descriptions (if observed):")
    for _, row in csr_df.iterrows():
        if row['Evidence Found'] == 'Yes' and row['Initiative']:
            st.write(f"**{row['Country']}:** {row['Initiative']}")


# 5. ORGANISATIONAL STRUCTURE
st.header("🏢 Organisational Structure")
org_data = []
for country_code in countries_to_display:
    org_data.append({
        'Country': survey_data[country_code]['store_info']['country'],
        'Management Photos Displayed': survey_data[country_code]['organisational_structure']['management_photos_displayed']
    })
org_df = pd.DataFrame(org_data)

if not org_df.empty:
    count_df = org_df.groupby(['Country', 'Management Photos Displayed']).size().reset_index(name='Count')
    fig = px.pie(count_df, values='Count', names='Management Photos Displayed', 
                 title=f"Management Photos Displayed ({', '.join(org_df['Country'].unique())})",
                 color='Management Photos Displayed',
                 color_discrete_map={'Yes': 'teal', 'No': 'orange'},
                 hole=0.3)
    if len(countries_to_display) > 1 and len(org_df['Country'].unique()) > 1 :
         fig = px.bar(count_df, x="Country", y="Count", color="Management Photos Displayed",
                      barmode="group", title="Management Photos Displayed",
                      color_discrete_map={'Yes': 'teal', 'No': 'orange'})

    st.plotly_chart(fig, use_container_width=True)

# 6. CULTURE
st.header("🎭 Culture")
culture_questions_binary = {
    'Customer Relations Person at Entrance': 'customer_relations_person_at_entrance',
    'Celebrates Employee of the Month': 'celebrate_employee_of_month',
    'Celebration/Display Theme (Sporting, Cultural, etc.)': 'celebration_theme_sport_cultural_religious'
}
culture_data_binary = []
for country_code in countries_to_display:
    country_name = survey_data[country_code]['store_info']['country']
    for q_display, q_key in culture_questions_binary.items():
        response = survey_data[country_code]['culture'][q_key]
        culture_data_binary.append({
            'Country': country_name,
            'Question': q_display,
            'Response': response
        })
culture_df_binary = pd.DataFrame(culture_data_binary)

if not culture_df_binary.empty:
    count_df_binary = culture_df_binary.groupby(['Country', 'Question', 'Response']).size().reset_index(name='Count')
    fig_culture_binary = px.bar(count_df_binary[count_df_binary['Response'] == 'Yes'], # Only plot 'Yes' for clarity, 'No' is implied
                                x="Question", y="Count", color="Country", barmode="group",
                                title="Observed Cultural Elements (Yes Responses)",
                                color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_culture_binary, use_container_width=True)

# Staff displays corporate image (Likert)
culture_likert_data = []
for country_code in countries_to_display:
    culture_likert_data.append({
        'Country': survey_data[country_code]['store_info']['country'],
        'Rating': survey_data[country_code]['culture']['staff_displays_corporate_image_dress_code']
    })
culture_likert_df = pd.DataFrame(culture_likert_data)
if not culture_likert_df.empty:
    fig_culture_likert = px.bar(culture_likert_df, x="Country", y="Rating", color="Country",
                                title="Staff Displays Corporate Image (Dress Code) - Rating 1-5",
                                labels={'Rating': 'Average Rating (1=Strongly Disagree, 5=Strongly Agree)'},
                                color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_culture_likert.update_layout(yaxis=dict(range=[0, 5.5]))
    st.plotly_chart(fig_culture_likert, use_container_width=True)


# 7. MARKETING (STORE APPEARANCE)
st.header("🛍️ Marketing: Store Appearance & Specials")
col_m1, col_m2 = st.columns(2)
with col_m1:
    st.subheader("Lowest Price Special In Stock & Marked")
    marketing_special_data = []
    for country_code in countries_to_display:
        marketing_special_data.append({
            'Country': survey_data[country_code]['store_info']['country'],
            'Rating': survey_data[country_code]['marketing_store_appearance']['lowest_price_special_in_stock_marked']
        })
    marketing_special_df = pd.DataFrame(marketing_special_data)
    if not marketing_special_df.empty:
        fig = px.bar(marketing_special_df, x="Country", y="Rating", color="Country",
                     title="Lowest Price Special (1-5 Scale)",
                     labels={'Rating': 'Rating (1=Strongly Disagree, 5=Strongly Agree)'},
                     color_discrete_sequence=px.colors.carto.Pastel)
        fig.update_layout(yaxis=dict(range=[0, 5.5]))
        st.plotly_chart(fig, use_container_width=True)

with col_m2:
    st.subheader("Overall Store Appearance Attributes")
    appearance_data = []
    attributes = list(positive_appearance_map.keys())
    for country_code in countries_to_display:
        country_name = survey_data[country_code]['store_info']['country']
        for attr in attributes:
            observed_value = survey_data[country_code]['marketing_store_appearance'][attr]
            is_positive = 1 if observed_value == positive_appearance_map[attr] else 0
            appearance_data.append({
                'Country': country_name,
                'Attribute': attr,
                'IsPositive': is_positive,
                'Status': 'Positive' if is_positive else 'Negative/Other'
            })
    appearance_df = pd.DataFrame(appearance_data)
    if not appearance_df.empty:
        # Sum of positive attributes per country
        summary_df = appearance_df[appearance_df['IsPositive']==1].groupby('Country')['IsPositive'].sum().reset_index(name='PositiveAttributeCount')
        fig = px.bar(summary_df, x="Country", y="PositiveAttributeCount", color="Country",
                     title=f"Number of Positive Store Appearance Attributes (out of {len(attributes)})",
                     color_discrete_sequence=px.colors.qualitative.Antique)
        fig.update_layout(yaxis=dict(range=[0, len(attributes)+0.5]))
        st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Attributes: {', '.join(attributes)}")


# 8. CUSTOMER EXPERIENCE
st.header("😊 Customer Experience")
st.sidebar.markdown("---")
st.sidebar.subheader("Customer Experience Options")
cx_aspects = list(survey_data['SA']['customer_experience'].keys())
cx_data = []
for country_code in countries_to_display:
    country_name = survey_data[country_code]['store_info']['country']
    for aspect in cx_aspects:
        rating = survey_data[country_code]['customer_experience'][aspect]
        cx_data.append({'Country': country_name, 'Aspect': aspect, 'Rating': rating})

if cx_data:
    cx_df = pd.DataFrame(cx_data)
    fig_cx = go.Figure()
    colors_cx = {'South Africa': 'rgba(220,50,50,0.7)', 'Zambia': 'rgba(50,50,220,0.7)'} # Reds, Blues

    for country in cx_df['Country'].unique():
        country_specific_df = cx_df[cx_df['Country'] == country]
        fig_cx.add_trace(go.Scatterpolar(
            r=country_specific_df['Rating'],
            theta=country_specific_df['Aspect'],
            fill='toself',
            name=country,
            line_color=colors_cx.get(country, 'grey')
        ))
    fig_cx.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5.5] # Ratings are 1-5
            )
        ),
        showlegend=True,
        title="Customer Experience Ratings (1=Bad/Non-compliant, 5=Good/Compliant)"
    )
    st.plotly_chart(fig_cx, use_container_width=True)

# 9. GROUP STATEMENTS
st.header("📊 Group Statements (Internal Observations)")
col_g1, col_g2 = st.columns(2)
with col_g1:
    st.subheader("Private Label Products Visibility")
    pl_data = []
    for country_code in countries_to_display:
        pl_data.append({
            'Country': survey_data[country_code]['store_info']['country'],
            'Rating': survey_data[country_code]['group_statements']['private_label_products_visible']
        })
    pl_df = pd.DataFrame(pl_data)
    if not pl_df.empty:
        fig = px.bar(pl_df, x="Country", y="Rating", color="Country",
                     title="Private Label Visibility (1-5 Scale)",
                     labels={'Rating': 'Rating (1=Strongly Disagree, 5=Strongly Agree)'},
                     color_discrete_sequence=px.colors.sequential.Plasma_r)
        fig.update_layout(yaxis=dict(range=[0, 5.5]))
        st.plotly_chart(fig, use_container_width=True)

with col_g2:
    st.subheader("Shelf Stocking Observation")
    stocking_data = []
    for country_code in countries_to_display:
        stocking_data.append({
            'Country': survey_data[country_code]['store_info']['country'],
            'Observation': survey_data[country_code]['group_statements']['shelf_stocking']
        })
    stocking_df = pd.DataFrame(stocking_data)
    if not stocking_df.empty:
        st.dataframe(stocking_df.set_index('Country'), use_container_width=True)
        # For a more visual representation if there were more categories or stores:
        # count_df = stocking_df.groupby(['Country', 'Observation']).size().reset_index(name='Count')
        # fig = px.bar(count_df, x="Country", y="Count", color="Observation", barmode="group")
        # st.plotly_chart(fig, use_container_width=True)


# 10. PRICE COMPARISON
st.header("💲 Price Comparison")
st.sidebar.markdown("---")
st.sidebar.subheader("Price Comparison Options")
products_to_compare = list(survey_data['SA']['price_comparison'].keys())
selected_product_price = st.sidebar.selectbox("Select Product for Price Comparison:", products_to_compare)

all_competitors = ['Shoprite', 'Pick n Pay', 'Food Lover\'s', 'Woolworths']
selected_competitors_price = st.sidebar.multiselect(
    "Select Competitors to Compare:",
    options=all_competitors,
    default=all_competitors
)

if selected_product_price and selected_competitors_price:
    price_data = []
    for country_code in countries_to_display:
        country_name = survey_data[country_code]['store_info']['country']
        currency_label = " (ZAR)" if country_code == 'SA' else " (Units as per survey)" # Clarify currency
        for competitor in selected_competitors_price:
            price = survey_data[country_code]['price_comparison'] \
                               .get(selected_product_price, {}) \
                               .get(competitor)
            if price is not None:
                price_data.append({
                    'Country': country_name + currency_label,
                    'Product': selected_product_price,
                    'Competitor': competitor,
                    'Price': price
                })
    price_df = pd.DataFrame(price_data)

    if not price_df.empty:
        fig_price = px.bar(price_df, x="Competitor", y="Price", color="Country",
                           barmode="group", title=f"Price Comparison for: {selected_product_price}",
                           labels={"Price": "Retail Price"},
                           color_discrete_sequence=px.colors.carto.Temps)
        st.plotly_chart(fig_price, use_container_width=True)
else:
    st.write("Select a product and competitors from the sidebar to see price comparisons.")

st.sidebar.markdown("---")
