import streamlit as st
import pandas as pd

# Google Sheets CSV Export URL (constant)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1W1BJWBI8nycdey0_3-F13WUQGI7Gjx5rgYGpjOvUq3Q/export?format=csv"

# Function to load Google Sheet data as CSV
def load_data(sheet_url):
    # Read the Google Sheet data directly as a CSV
    data = pd.read_csv(sheet_url)
    return data

# Function to clean platform names
def clean_platforms(data):
    # Replace NaN values and standardize platform names
    data["Platform"] = data["Platform"].fillna("").str.lower().str.strip()
    return sorted(set(data["Platform"].tolist()))  # Return sorted unique platform names

# Main app function
def main():
    st.title("Brand Manager Dashboard")
    st.write("View and filter your brand management data in real-time!")

    try:
        # Load data from the constant Google Sheet URL
        data = load_data(SHEET_URL)

        # Clean platforms and get unique values
        platforms = clean_platforms(data)

        # Dropdown for platform selection with placeholder
        st.subheader("Select a Platform")
        selected_platform = st.selectbox("Choose a Platform", options=["Select an option"] + platforms)

        # Proceed only if a valid platform is selected
        if selected_platform != "Select an option":
            # Filter data by selected platform
            filtered_data = data[data["Platform"].str.lower() == selected_platform]

            # Create a list of unique brands for the selected platform
            if not filtered_data.empty:
                brands = filtered_data["Brand"].unique().tolist()
                st.subheader("Select a Brand")
                selected_brand = st.selectbox("Choose a Brand", options=["Select an option"] + brands)

                # Proceed only if a valid brand is selected
                if selected_brand != "Select an option":
                    # Filter data by selected brand
                    brand_data = filtered_data[filtered_data["Brand"] == selected_brand]

                    # Display the tier and other details for the selected brand
                    if not brand_data.empty:
                        row = brand_data.iloc[0]  # Get the first row (should be only one)
                        st.write(f"**Brand:** {row['Brand']}")
                        st.write(f"**Tier:** {row['Tier']}")
                        st.write(f"**Category:** {row['Category']}")
                        st.write(f"**Handled by:** {row['Manager']}")
                    else:
                        st.write("No details found for the selected brand.")
            else:
                st.write("No brands found for the selected platform.")
        else:
            st.write("Please select a platform to continue.")

    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
