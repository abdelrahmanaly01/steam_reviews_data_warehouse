
from pyspark import SparkConf, SparkContext
from pyspark.sql import functions as f
import configparser
import os
from pyspark.sql import SparkSession


def create_spark_session():
    print('initialize a spark session...')
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    print('spark session is initialized.')

    return spark


def process_game_tables(input_path, output_path, spark):
    """
    process the games table to extract games,genre,developer nad publisher dimensions
    """
    print('importing data...')
    games = spark.read.csv(input_path,
                           sep=',', multiLine=True, header=True)
    
    games = (games
             .withColumn('app_id', f.regexp_extract(f.col('url'), '([0-9]+)', 0).cast('long'))
             .withColumn('genres', f.split(f.col('genre'), ','))
             .withColumn('developers', f.split(f.col('developer'), ','))
             .withColumn('publishers', f.split(f.col('publisher'), ','))
             .withColumn('release_date_new', f.to_timestamp(f.concat(
                 f.col('release_date').substr(0, 3),
                 f.regexp_extract(f.col('release_date'), ' [0-9]+, [0-9]+', 0)), 'MMM d, yyyy'))
             )
    games = games.filter(~f.isnull(col('app_id')) )
    games_table = games.select(f.col('app_id'), f.col(
        'name'), f.col('release_date_new'))
    genre_table = games.select(games.app_id, f.explode('genres')).distinct()
    developer_table = games.select(
        games.app_id, f.explode('developers')).distinct()
    publisher_table = games.select(
        games.app_id, f.explode('publishers')).distinct()

    print('saving game tables output...')

    games_table.write.parquet(
        f'{output_path}/games_table')
    genre_table.write.parquet(
        f'{output_path}/genre_table')
    developer_table.write.parquet(
        f'{output_path}/developer_table')
    publisher_table.write.parquet(
        f'{output_path}/publisher_table')

    print('games tables is processed successfully.')


def process_reviews_tables(input_path, output_path, spark):
    """
    process the reviews table to extract user nad time dimensions also the fact table
    """
    reviews = spark.read.parquet(
        input_path)
    # reviews = spark.sparkContext.parallelize(reviews)
    print('reviews data is loaded.')
    
    reviews.createOrReplaceTempView('reviews')
    
    #this line automaticaly handles users table duplcates by the agg functions
    user_table = spark.sql(
        '''SELECT steamid, max(num_games_owned),max(num_reviews)
        from reviews
        group by steamid'''
    )
    reviews = reviews.withColumn(
        'time_created', f.from_unixtime('unix_timestamp_created').cast('date'))
    time_table = (reviews.selectExpr('unix_timestamp_created as id', 'time_created')
                  .withColumn('hour', f.hour(f.col('time_created')))
                  .withColumn('day', f.dayofmonth(f.col('time_created')))
                  .withColumn('week', f.weekofyear(f.col('time_created')))
                  .withColumn('month', f.month(f.col('time_created')))
                  .withColumn('year', f.year(f.col('time_created')))
                  .withColumn('weekday', f.dayofweek(f.col('time_created')))
                  )
    reviews_table = (reviews.withColumn('month', f.month(f.col('time_created')))
                                        .withColumn('year', f.year(f.col('time_created')))
                                        .selectExpr('appid as app_key',
                                       'steamid as user_key',
                                       'unix_timestamp_created as time_key',
                                       'voted_up as review',
                                       'playtime_at_review',
                                       'playtime_forever',
                                       'year',
                                       'month'
                                       ).orderBy('time_key').withColumn('review_id', f.monotonically_increasing_id())
                                       
                                       )

    print('saving reviews tables output...')

    time_table.write.partitionBy('year','month').parquet(
        f'{output_path}/time_table')
    reviews_table.write.partitionBy('year','month').parquet(
        f'{output_path}/reviews_table')
    user_table.write.parquet(f'{output_path}/users_table')
    print('reviews tables is processed successfully.')


if __name__ == '__main__':
    spark = create_spark_session()
    input = 's3://steamgamereviews/data/'
    output = 's3://steamgamereviews/output/'
    process_reviews_tables(f'{input}/reviews/', output, spark)
    process_game_tables(f'{input}/games/games.csv', output, spark)
