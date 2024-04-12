import streamlit as st

st.set_page_config(
    page_title='Overview',
    page_icon='volcano',
)

st.session_state.update(st.session_state)

def main():
    # Your Streamlit app content
    st.title("Volcano Widget Company: Financials")

    # Apply custom style directly to st.title
    st.markdown(
        """
        <style>
        [data-testid="StyledLinkIconContainer"] {
            color: #FFFFFF !important;
        }
        .paragraph-container {
            position: absolute;
            top: 50%;
            right: 10%;
            transform: translate(0, -10%);
            background-color: rgba(0, 0, 0, 0.7); /* Darker background color */
            padding: 20px;
            border-radius: 10px;
        }
        .paragraph-container p {
            color: white; /* Text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    page_bg_img = '''
        <style>
        [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/free-photo/erupting-mountain-spews-fiery-ash-into-sky-generated-by-ai_188544-10172.jpg?w=1060&t=st=1712862369~exp=1712862969~hmac=230f4eeee290e98e3a11a89e6741a6f2de4a1e9c0b39c487ad82b1efd5c08719");
        background-size: cover;
    }
        </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.markdown(
            """
            <div class="paragraph-container">
                <p><strong>In this application, you can explore the financials from the Volcano Widget Company. \
                    Answering questions like: Were there patterns over the last year? Is there a Segment that is trending? \
                    Is there a Country that is falling behind?
                    Navigate to the Sales, Profit, Units Sold, and Profit by Product tabs to analyze the data.</strong></p>
            </div>
            """,
            unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
