import streamlit as st

st.title('Criteria Manager')

st.write('This page allows you to manage criteria sets and criteria')

crit_set_form = st.form("Criteria Set Form", clear_on_submit=True)
crit_set_form.subheader("Add a Criteria Set")
crit_set_name = crit_set_form.text_input("Enter the name of the criteria set")
crit_set_description = crit_set_form.text_area("Enter a description of the criteria set")
crit_set_form.write('Once you have added the Criteria Set, you can add criteria in the tab "Manage Criteria Sets"')

if crit_set_form.form_submit_button('Submit'):
    crit_set = (crit_set_name, crit_set_description)
    st.write(crit_set)
else:
    crit_set = None

