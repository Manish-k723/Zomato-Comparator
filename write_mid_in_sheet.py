import gspread, ast
from google.cloud import bigquery
from google.oauth2 import service_account

SHEET_ID = "1uEudlQ4iGqzIIWkGHkZqOc3VwnPQU8ohyH6vxdqwxII"
SHEET_NAME="locality_details"

def extract_ids_from_string(id_string):
    id_list = ast.literal_eval(id_string)
    return id_list

def run_query(z_ids):
    credential_path = "/opt/aryan/bigquery.json"

    credentials = service_account.Credentials.from_service_account_file(credential_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    bq_query = '''
                Select magic_id, name from `wallet_latest.zomato_store` where id in {0}
    '''

    bq_response = client.query(bq_query.format(z_ids))
    records = [dict(row) for row in bq_response]

    return records

def write_in_sheet(worksheet, m_ids, index):
    response_col = worksheet.find('merchant_info').col
    m_ids_str = str(m_ids)
    worksheet.update_cell(index, response_col, m_ids_str)

def bq_read():
    gs = gspread.service_account(filename="/etc/gspread/service_account.json")
    sh = gs.open_by_key(SHEET_ID)
    worksheet = sh.worksheet(SHEET_NAME)
    z_id_column_index = worksheet.find('top_merchants_zomato_id').col
    id_cells = worksheet.col_values(z_id_column_index)[1:]
    index = 2
    for id_cell in id_cells:
        m_ids = []
        if id_cell.strip():  # Check if the cell is not empty
            ids = extract_ids_from_string(id_cell)
            ids = tuple([str(id) for id in ids])
            m_ids = run_query(ids)
        write_in_sheet(worksheet, m_ids, index)
        index+=1
