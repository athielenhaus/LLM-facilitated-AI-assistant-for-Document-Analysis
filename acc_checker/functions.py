import json
import streamlit as st

def load_json(file_path):
    file = open(file_path, encoding="utf-8")   # specifying encoding necessary to display German characters
    criteria_sets = json.load(file)
    return criteria_sets

def create_sub_crit_layout(crit_container, subcriterion):
    crit_container.write(subcriterion["text"])
    crit_col1, crit_col2 = crit_container.columns(2)

    # note: for streamlit, each text area must have unique key
    crit_col1.text_area(f'{subcriterion["name"]} Retrieved Text')
    crit_col2.text_area(f'{subcriterion["name"]} Suggested Response')
