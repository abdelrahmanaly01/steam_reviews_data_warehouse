
# Steam Reviews Data Lake

This project is meant for people interested in games as well data
by using this data lake we can answer some interesting  Questions like what is most liked and most played games by  genres, publishers, developers and release dates as well understanding how user comments get effected by games user owned, hours played and the frequency of user reviews.

# Datasets

This project is based on two datasets sampled(scraped) from steam website and database.

_NOTE:_ dataset used in this project was sampled 2.4m from reviews dataset and
the format changed from csv to parquet because i faced alot of technical issues manipulating the data
from this file format.

## Steam Reviews Dataset
https://www.kaggle.com/datasets/forgemaster/steam-reviews-dataset


Rating data from 6M unique users, with 15M reviews over 8,183 games

Content:

Each row (review) contains information in the following order by column:

- steamid - the user's ID
- appid - the ID of the game being reviewed
- voted_up - true means it was a positive recommendation
- votes_up - the number of other users who found this review helpful
- votes_funny - the number of other users who found this review funny
- weighted_vote_score - helpfulness score
- playtime_forever - how many hours the user had played this game at retrieval
- playtime_at_review - how many hours the user had played the game when writing this review
- num_games_owned - the number of games this user owns
- num_reviews - the number of reviews this user has written
- review - the text of the written review
- unix_timestamp_created - date the review was created (unix timestamp)
- unix_timestamp_updated - date the review was last updated (unix timestamp)

### The dataset as a whole contains:
6,976,390 unique users
15,437,471 reviews
8,183 games reviewed

## Steam games complete dataset

https://www.kaggle.com/datasets/trolukovich/steam-games-complete-dataset

Content:

This dataset contains more than 40k games from steam shop with detailed data.

- url - the hyper link to the application page
- types - type of the product
- name - name of the game or application
- desc_snippet - game brieve description
- recent_reviews - the most recent reviews direction when the data scraped(positive to negative)
- all_reviews - overall reviews direction (positive to negative)
- release_date - product release date
- developer - game developers
- publisher - games publishers
- popular_tags - tags accossiated with the game
- game_details - details of the game EX: multiplayer/single
- languages - game languages
- achievements - number of achievments 
- genre - game genres
- game_description - game detailed description
- mature_content - whether the game have mature content or not
- minimum_requirements - minimum device requirements
- recommended_requirements - recommended requirments 
- original_price - game original price
- discount_price - discount when data was scraped



# Data model  

The chosen data model is galaxy schema sense i needed to make sub-dimensons from the games dimensions table so we can gain more information from the multivalued columns.

### Data dictionary 
![dictionary](https://drive.google.com/file/d/1-3axhAcb5E8mwpl1gAkaQbqPEOIp301d)
### galaxy schema

![galaxy_schema](https://drive.google.com/file/d/1-3ATgTlb6B9E92pZ3iqmuEm5UFTzTOzf)


# Logical scenario

The project contains to main processes and two tools  first we have elt which is the step for creating the spark data lake, as well the etl process to move the data to the data warehouse.

*spark* is used for fast and easy manipulation of the data as well for data exploration in development phase sense, not all cleaning and processing of the data can be done on redshift.

*Redshift* is used for easier access for normal users and easier integration with apps in development.

As mentioned the reviews data is about 15m reviews i used a sample of 2.4m only for the development of the project

_steps of development was:_
- defining the scope of the project and what is the final results
- searching for the appropriate datasets that at least have any common connection in between to be able to connect reviews to the games data, also searched the steamDB website and amazon datasets for games data but i couldn't find the required data,but finally i was able to find it on kaggle.
- data exploration, at this part the sampled data could have been explored using _pandas_ library but i chosed to explore it using my local spark environment
so i could discover the technical problems of spark earlier if existed.
- data model definition, as mentioned in model i chosed the galaxy schema.
- coding the project elt and testing it on local environment
- creating the cloud spark cluster and replacing any local variables with cloud variables
- submitting the elt script on the spark cluster
- creating redshift cluster and the needed tables
- run the etl process
- run the data quality checks



logical approach to this project under the following scenarios:

The data was increased by 100x?
- one way to go around this is increasing number nodes in the same cluster, another way is increasing the processing power of the existing nodes by using a higher tier of nodess like ds2.xlarg
The pipelines would be run on a daily basis by 7 am every day?
- i will use airflow schdular and set it in the dag configuration variables with @daily and set the start_time to  datetime(2023, 5, 18, 7, 0, 00) for example 
The database needed to be accessed by 100+ people?
- i would consider using one non relational(NoSql) solutions and Elastic Load Balancing (ELB) to handle this number of users requests 



# Excecution

to create your own data lake and data warehouse you should follow the next steps

1- upload the needed data to S3
2- create a EMR spark cluster on AWS
3- submit the elt_spark_submission.py using spark-submit
   >> ./spark-submit elt_spark_submission.py
4- open the dwh.cfg and edit the variables with your credientials
5- create a redshift cluster
6- open the query editor and use the queries in the create_tables_sql_queries.sql
7- run the etl_redshift.py
8- run the data_quality_check.py to make sure your files are loaded successfully 

# Future improvments
this project was planned to use airflow and schedule the elt based on the year and month variables
but i faced a lot of issues integrating airflow with spark and submitting the jobs, so the airflow tool will be added as soon as possible after solving this issues. 


## example for using the datawarehouse in analytics:

lets see the number of positive reviews on the top 5 game developers ?
select  d.developers,count(*) 
from 
reviews r 
join games_dimenson g on g.appid = r.app_key
join developers_subdimenson d on  d.app_fk = g.appid
where r.voted_up = true
group by 1
order by 2 desc
limit 5 

_the result_:
![result](https://drive.google.com/file/d/1MFUrd0ltRLr9M6AiGzU0Xd-a7OY1T6sV)
