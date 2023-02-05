# get configration templete
from tableau_api_lib import sample_config 
print(sample_config)

from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import get_groups_dataframe
from tableau_api_lib.utils import querying
import tableau_api_lib
import numpy as np
import pandas as pd


#Signin to server
tableau_config = {
        'tableau_test_info': {
                'server': 'https://10ax.online.tableau.com/',
                'api_version': '3.19',
                #'username': '',
               # 'password': '',
            "personal_access_token_name": "",
            "personal_access_token_secret": ""
                'site_name': '',
                'site_url': ''
        }
}
conn = TableauServerConnection(config_json=tableau_config, env='tableau_test_info')
response = conn.sign_in()
print(response.json())


# get users list 
users_list = querying.get_users_dataframe(conn)
display(users_list)

# filter users by siteRole 
users_filter = users_df.query("siteRole=='ServerAdministrator'")
display(users_filter)

# get users details on csv file
users_column=['email','name','fullName',"siteRole","lastLogin","id"]
users_list[users_column].to_csv('users.csv', index=False)

# function to change users site role to Unlicensed (csv only id column)
def unlicense_users(conn:TableauServerConnection,
                   users_to_unlicense_df: pd.DataFrame) -> list:
    responses = []
    for index, row in users_to_unlicense_df.iterrows():
        response = conn.update_user(user_id=row['id'], new_site_role='Unlicensed')
        responses.append(response)
    return responses

users_to_df = pd.read_csv(r"path\users.csv", delimiter=';')
responses = unlicense_users(conn=conn,users_to_unlicense_df=users_to_df)


# get site groups to csv file
groups_df = querying.get_groups_dataframe(conn)
type(groups_df)
#groups_df.head()
groups_df.to_csv('groups.csv', index=False)
