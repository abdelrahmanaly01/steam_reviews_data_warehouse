import configparser
import psycopg2


def check_reviews_table(conn,cur):
    '''checks if the reviews fact_table is loaded successfuly'''
    query = 'select count(*) from reviews'
    cur.execute(query)
    records_num = cur.fetchone()
    conn.commit()
    if records_num[0] <= 0 : 
        print('table is empty') 
    else:
       print('reviews table records loaded : ', records_num[0])


def check_joins(conn,cur):
    '''checks if tables from games table and reviews table are joinable'''
    query= '''
    select count(*) from 
    reviews r
    join games_dimenson g
    on g.appid = r.app_key 
    '''
    cur.execute(query)
    records_num =cur.fetchone()
    conn.commit()
    if records_num[0] <= 0 : 
        print('table is empty') 
    else:
        print('reviews joined with games table are : ', records_num[0])    

def main():
    '''establishs a connection and executes the data quality checks functions'''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    check_reviews_table(conn,cur)
    check_joins(conn,cur)

if __name__ == '__main__':
    
    main()
