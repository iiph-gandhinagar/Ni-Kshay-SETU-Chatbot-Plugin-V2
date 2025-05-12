import pandas as pd
import os
import boto3

from app.ordering.first_ordering import first_ordering
from app.ordering.second_ordering import second_ordering

from app.tasks.short_to_full_form import get_short_forms, match_full_form_with_node_id
from app.tasks.vector_search import vectors_search
from app.slack_alerts.error_via_slack_alerts import send_slack_alert

from dotenv import load_dotenv
load_dotenv()



environment = os.getenv('APP_ENV')

def find_node_ids_ntep(query, mode, option_cadre, lang):

    try:
        mode = "both" # default mode for now
        unique_node_ids = []

        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        AWS_BUCKET = os.environ.get('AWS_BUCKET')
        AWS_REGION = os.environ.get('AWS_REGION')

        object_key = "training_data/merged.csv"
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

        # Reading CSV file from S3
        response = s3.get_object(Bucket=AWS_BUCKET, Key=object_key)
        df = pd.read_csv(response['Body'])

        df = df.rename(columns={
            'cpageid': 'node_id',
            'node_title':  'linked_node_title',
            'cpage_title': 'node_title',
            'nodeid': 'linked_node_id',
            'page_status': 'page_status',
            'field_target_audience': 'cadre_id',
            'field_subnodes' : 'subnode_id',
            'field_h5content': 'h5_content_id'
        })
        short_forms = get_short_forms(query)
        if short_forms != []:
            full_form_node_id = match_full_form_with_node_id(short_forms,df)
            full_form_node_id_short= match_full_form_with_node_id([query],df)
            full_form_node_ids = full_form_node_id + [node_id for node_id in full_form_node_id_short if node_id not in full_form_node_id]
            full_form_node_ids = sorted(list(set(full_form_node_ids)))
            
            unique_node_ids = list(set(unique_node_ids))  # Remove duplicates within directly matched node IDs
            # Prioritize full form node IDs
            unique_node_ids = full_form_node_ids + [node_id for node_id in unique_node_ids if node_id not in full_form_node_ids]
            if unique_node_ids == []:
            
                #convert list of str to str
                short_forms = short_forms[0]
                unique_node_ids = vectors_search(short_forms)
            
            
        else: 

            unique_node_ids = vectors_search(query)     

        match mode:
            case 'input_phrase':
                unique_node_ids = first_ordering(unique_node_ids,query,df)
            case 'cadre':
                unique_node_ids = second_ordering(unique_node_ids, option_cadre,df)
            case 'both':
                unique_node_ids = first_ordering(unique_node_ids,query,df)
                unique_node_ids = second_ordering(unique_node_ids, option_cadre,df)
            case 'none':
                unique_node_ids = unique_node_ids
            case _:
                print("No specific ordering applied")
        
        langcode = ""
        match lang:
            case 'en':
                langcode = "English"
            case 'hi':
                langcode = "Hindi"
            case 'gu':
                langcode = "Gujarati"
            case 'mr':
                langcode = "Marathi"
            case 'kn':
                langcode = "Kannada"
            case 'tm':
                langcode = "Tamil"
            case 'te':
                langcode = "Telugu"
                
                
                
        node_details = []
     

        all_h5p_ids =[]
        if "burden" in query.lower():
            global_burden_tb_id_set = set(df.loc[df['node_title'] == "Global Burden of TB", 'node_id'])

            if global_burden_tb_id_set:
                global_burden_tb_id = next(iter(global_burden_tb_id_set))  # Extract the single ID

                if global_burden_tb_id in unique_node_ids:
                    unique_node_ids.remove(global_burden_tb_id)  # Remove from set
                    unique_node_ids.insert(0, global_burden_tb_id)
            for node_id in unique_node_ids:
            # Get the subnode_id string for the current node_id
                subnode_ids_str = df[df['node_id'] == node_id]['subnode_id'].iloc[0]  # This will return the subnode_id string
                h5p_ids = df[(df['node_id'] == node_id) & (df['langcode'] == langcode)]
                h5p_id = []
                if not h5p_ids.empty:
                # Get the first matching h5_content_id
                    h5p_id = h5p_ids['h5_content_id'].iloc[0]
                    if pd.notna(h5p_id):
                        h5p_id = int(h5p_id)  # Convert to integer
                        all_h5p_ids.append(h5p_id)
                    else:
                        h5p_id = []  # Handle case where h5p_id is NaN


                
                node_title = df[df['node_id'] == node_id]['node_title'].iloc[0] if not df[df['node_id'] == node_id]['node_title'].empty else None
                page_status = df[df['node_id'] == node_id]['page_status'].iloc[0] if not df[df['node_id'] == node_id]['page_status'].empty else None
                # Check if subnode_ids_str is not NaN or empty
                if pd.notna(subnode_ids_str) and subnode_ids_str.strip() != '':
                    # Convert the subnode_id string into a list of integers
                    processed_subnodes = [int(x.strip()) for x in subnode_ids_str.split(',') if x.strip()]
                    matched_node_ids = df[df['linked_node_id'].isin(processed_subnodes)]['node_id'].drop_duplicates().tolist()
                else:
                    # Handle case where there are no subnodes or it's NaN
                    matched_node_ids = []
                
                if h5p_id:
                # Append the node_id and its corresponding processed subnode_ids
                    node_details.append({'nid': node_id,'title':node_title,'H5P-id':h5p_id,'Content_status':page_status,'langcode':lang,'sub_node': matched_node_ids})

            
        else:
            for node_id in unique_node_ids:
            # Get the subnode_id string for the current node_id
                subnode_ids_str = df[df['node_id'] == node_id]['subnode_id'].iloc[0]  # This will return the subnode_id string
                h5p_ids = df[(df['node_id'] == node_id) & (df['langcode'] == langcode)]
                h5p_id = []
                if not h5p_ids.empty:
                # Get the first matching h5_content_id
                    h5p_id = h5p_ids['h5_content_id'].iloc[0]
                    if pd.notna(h5p_id):
                        h5p_id = int(h5p_id)  # Convert to integer
                        all_h5p_ids.append(h5p_id)
                    else:
                        h5p_id = []  # Handle case where h5p_id is NaN

                
                node_title = df[df['node_id'] == node_id]['node_title'].iloc[0] if not df[df['node_id'] == node_id]['node_title'].empty else None
                page_status = df[df['node_id'] == node_id]['page_status'].iloc[0] if not df[df['node_id'] == node_id]['page_status'].empty else None
                # Check if subnode_ids_str is not NaN or empty
                if pd.notna(subnode_ids_str) and subnode_ids_str.strip() != '':
                    # Convert the subnode_id string into a list of integers
                    processed_subnodes = [int(x.strip()) for x in subnode_ids_str.split(',') if x.strip()]
                    matched_node_ids = df[df['linked_node_id'].isin(processed_subnodes)]['node_id'].drop_duplicates().tolist()
                else:
                    # Handle case where there are no subnodes or it's NaN
                    matched_node_ids = []
                if h5p_id:
                # Append the node_id and its corresponding processed subnode_ids
                    node_details.append({'nid': node_id,'title':node_title,'H5P-id':h5p_id,'Content_status':page_status,'langcode':lang,'sub_node': matched_node_ids})


        if all_h5p_ids == []:
            return {lang:["\bOops!\nIt looks like I couldn't find the information you were looking for. Please try rephrasing your question, or let me know if there's something else I can assist you with!"]}
        else:
            return node_details
    except Exception as e:
        print("Error:", e)
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot\n"
            f"ENV: {environment}\n"
            f"file:pinecone_testing.py\n"
            f"Error: {e}\n"

        )
        send_slack_alert(error_message)




