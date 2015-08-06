redis_host = 'dbredis'  
redis_port = 6379

red = redis.StrictRedis(host=config.redis_host, port=config.redis_port, db=config.jobqueue_db)


mongodb_host = 'dbredis'
#用mongodb控制jobqueue使用的db名称
mongo_queue_dbname = 'title'