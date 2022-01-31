import streamlit as st
import pandas as pd


st.sidebar.title("About")
st.sidebar.info(
        "This streamlit web app shows a collection of python programming problems, including task description,\n" 
        "code solution & test cases. This consists around 1,000 crowd-sourced Python programming problems designed \n"
        "to be solvable by entry level   programmers.\n"
        "\n"
        "The data was downloaded from [google-research](https://github.com/google-research/google-research/tree/master/mbpp) github repo.\n"
        "\n Check the code behind this app [here](https://github.com/gafstar/google1000).\n\n"
)
class Paginate:
    def __init__(self):
        if 'page_number' not in st.session_state:
            st.session_state.page_number = 0
        if 'title' not in st.session_state:
            st.session_state.title = "Calculator"
        self.col1,_,_,_,_,_,_,self.col8 = st.columns(8)
        # self.col1,self.col2 = st.columns(2)
        self.N = 50

    def next_page_number(self):
        if st.session_state.page_number < 19:
            st.session_state.page_number += 1
        else:
            st.session_state.page_number = 19

    def previous_page_number(self):
        if st.session_state.page_number >= 0:
            st.session_state.page_number -= 1
        else:
            st.session_state.page_number = 0

    def _window(self):

        with self.col8:
            st.button("Next", on_click=self.next_page_number)
            # st.sidebar('Test')
            st.write(f'Page {st.session_state.page_number + 1}')
        # Load the  data from github
        data = pd.read_json('https://raw.githubusercontent.com/google-research/google-research/master/mbpp/mbpp.jsonl', lines=True)

        st.markdown(
            """
            <style>
            .main{
            background-color:#g5g5g5;
            }
            </style>
            """,unsafe_allow_html=True
        )

        last_page = len(data) // self.N
        start_idx = st.session_state.page_number * self.N 
        end_idx = (1 + st.session_state.page_number) * self.N
        
        # Check if pagination index overflows
        if start_idx < 0:
            st.write('No pages to show. Please click `Next`.')
            start_idx = 0
        elif end_idx > len(data):
            st.write('This is the last page.  Please click `Previous`.')
            end_idx = 974
        
        # Creating a task description expander
        for idx in range(start_idx, end_idx):
            text = data.loc[idx, 'text']
            with st.expander(f'{text}',expanded=False):
                code = data.loc[idx, 'code']
                st.code(code, language='python')
                
                # Creating a checkbox that expands and displays the test code when clicked
                if st.checkbox("Show Test", key={idx}):
                    test_list = data.loc[idx:, 'test_list'][idx][:]
                    for test in test_list:
                        st.code(test, language='python') 

        with self.col1:
            st.button("Previous", on_click=self.previous_page_number)

#############################

if __name__ == '__main__':
    ct = Paginate()
    ct._window()