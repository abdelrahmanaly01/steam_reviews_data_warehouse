import configparser
import psycopg2


def load_data_to_tables(cur,conn,tables,output_path,role):
    '''
    executes the copying queries on Amazon redshift 
    cluster
    '''   
    for table in tables:
        path = "'"+output_path+tables[table]+"'"
        cur.execute('''COPY {}
                FROM {}
                IAM_ROLE {}
                FORMAT AS PARQUET;'''.format(table,path,role))
        conn.commit()
        

def main(tables):  
    '''
    creating connection and executing the load_data function
    '''     
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    load_data_to_tables(cur,conn,tables,config['S3']['OUTPUT_PUCKET'],config['IAM_ROLE']['ARN'])
    conn.close()
        
if __name__ == '__main__':
    tables_dict = {
            'games_dimenson': '/games_table/',
            'developers_subdimenson':'/developer_table/',
            'publishers_subdimenson':'/publisher_table/',
            'genres_subdimenson':'/genres_table/',
            'time_dimenson':'/time_table/',
            'reviews' : '/reviews_table/',
            'user_dimenson' : '/users_table/'
    }

    main(tables_dict)
