drop table if exists developers_subdimenson;
drop table if exists publishers_subdimenson;
drop table if exists genres_subdimenson;
drop table if exists reviews;
drop table if exists games_dimenson;
drop table if exists time_dimenson;
drop table if exists user_dimenson;

CREATE TABLE games_dimenson
  (
     appid        BIGINT PRIMARY KEY,
     NAME         TEXT NOT NULL,
     release_date TIMESTAMP 
  );

CREATE TABLE developers_subdimenson
  (
     app_fk     BIGINT NOT NULL,
     developers TEXT NOT NULL,
     CONSTRAINT app_developers_fk FOREIGN KEY(app_fk) REFERENCES games_dimenson(
     appid)
  );

CREATE TABLE publishers_subdimenson
  (
     app_fk    BIGINT NOT NULL,
     publisher TEXT NOT NULL,
     CONSTRAINT app_publishers_fk FOREIGN KEY(app_fk) REFERENCES games_dimenson(
     appid)
  );

CREATE TABLE genres_subdimenson
  (
     app_fk BIGINT NOT NULL,
     genre  TEXT NOT NULL,
     CONSTRAINT app_genres_fk FOREIGN KEY(app_fk) REFERENCES games_dimenson(
     appid)
  );

CREATE TABLE time_dimenson
  (
     ts      BIGINT PRIMARY KEY,
     date    date NOT NULL,
     hour    BIGINT NOT NULL,
     day     BIGINT NOT NULL,
     week    BIGINT NOT NULL,
     weekday BIGINT NOT NULL
  );

CREATE TABLE user_dimenson
  (
     steam_id        BIGINT PRIMARY KEY,
     num_games_owned BIGINT ,
     num_reviews     BIGINT
  );

CREATE TABLE reviews
  (
     app_key       BIGINT NOT NULL,
     user_key      BIGINT NOT NULL,
     time_key      BIGINT NOT NULL,
     voted_up      BOOLEAN NOT NULL,
     num_at_review BIGINT,
     num_forever   BIGINT,
     review_id     BIGINT PRIMARY KEY,
     CONSTRAINT app_fk FOREIGN KEY(app_key) REFERENCES games_dimenson(appid),
     CONSTRAINT time_fk FOREIGN KEY(time_key) REFERENCES time_dimenson(ts),
     CONSTRAINT user_fk FOREIGN KEY(user_key) REFERENCES user_dimenson(steam_id)
  ); 




