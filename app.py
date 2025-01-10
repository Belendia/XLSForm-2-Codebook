import pandas as pd
import os
import re


def xlsxform_to_markdown(xlsx_path, output_path):
    """
    Converts an XLSForm into a Markdown codebook, categorizing questions under groups and repeats, 
    with collapsible groups and consistent indentation.
    
    Args:
        xlsx_path (str): Path to the XLSForm (Excel file).
        output_path (str): Path to save the Markdown file.
    """
    # Load XLSForm
    try:
        xls = pd.ExcelFile(xlsx_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Load survey sheet
    try:
        survey_df = xls.parse('survey')
    except Exception as e:
        print(f"Error reading 'survey' sheet: {e}")
        return

    # Load choices sheet if it exists
    try:
        choices_df = xls.parse('choices', converters = {
            'name': lambda x: str(x) if pd.notnull(x) else None
            })
    except:
        choices_df = None

    # Start writing Markdown
    markdown_lines = ["# Codebook", ""]
    group_stack = []  # Stack to track groups and repeats

    for _, row in survey_df.iterrows():
        question_type = row.get('type', '')
        question_name = row.get('name', '')
        question_label = row.get('label::English (en)', '')
        question_relevant = row.get('relevant', '')
        question_calculate = row.get('calculation', '')

        if pd.isna(question_type):
            continue

        # Handle begin group or begin repeat
        if question_type.startswith('begin '):
            group_name = question_name or f"Unnamed {question_type.split(' ')[-1]}"
            group_label = question_label or group_name
            markdown_lines.append(f"<details>")
            markdown_lines.append(f"<summary><h2>{group_label} ({question_type.split(' ')[-1]})</h2></summary>")
            markdown_lines.append("")
            markdown_lines.append(f"- **Type**: {question_type}")
            if pd.isna(question_relevant) == False:
                relevant = question_relevant.replace(".", question_name)
                relevant = re.sub(r'[\$\{\}]', '', relevant)
                markdown_lines.append(f"- **Relevant**: {relevant}")
            group_stack.append(group_name)
            markdown_lines.append("")
            continue

        # Handle end group or end repeat
        if question_type.startswith('end '):
            if group_stack:
                group_stack.pop()
            markdown_lines.append(f"</details>")
            markdown_lines.append("")  # Add a blank line after ending a group
            continue

        # Handle regular questions
        if question_name and question_label:
            indent = "  " * 0 #if len(group_stack) == 0 else 2 #len(group_stack)  # Indent based on the depth of nesting
            markdown_lines.append(f"{indent}### {question_name}")
            markdown_lines.append(f"{indent}- **Label**: {question_label}")
            markdown_lines.append(f"{indent}- **Type**: {question_type}")
            if pd.isna(question_relevant) == False:
                relevant = question_relevant.replace(".", question_name)
                relevant = re.sub(r'[\$\{\}]', '', relevant)
                markdown_lines.append(f"{indent}- **Relevant**: {relevant}")
            if pd.isna(question_calculate) == False:
                calc = re.sub(r'[\$\{\}]', '', str(question_calculate))
                markdown_lines.append(f"{indent}- **Calculate**: {calc}")
            
            # Add choices for select_one or select_multiple questions
            if choices_df is not None and question_type.startswith(('select_one', 'select_multiple')):
                list_name = question_type.split(' ')[-1]
                choices = choices_df[choices_df['list_name'] == list_name]
                if not choices.empty:
                    markdown_lines.append(f"{indent}- **Choices**:")
                    for _, choice_row in choices.iterrows():
                        choice_name = choice_row.get('name', '')
                        choice_label = choice_row.get('label::English (en)', '')
                        markdown_lines.append(f"{indent}  - {choice_name}: {choice_label}")

            markdown_lines.append("")  # Add a blank line for readability

    # Save Markdown file
    try:
        with open(output_path, 'w') as f:
            f.write("\n".join(markdown_lines))
        print(f"Codebook saved to {output_path}")
    except Exception as e:
        print(f"Error saving Markdown file: {e}")


# Example usage
if __name__ == "__main__":
    input_file = "xlsxforms/TDA_travel.xlsx"  # Path to the XLSForm
    output_file = "codebooks/TDA_travel.md"  # Path to the output Markdown file

    if os.path.exists(input_file):
        xlsxform_to_markdown(input_file, output_file)
    else:
        print(f"Input file '{input_file}' does not exist.")
