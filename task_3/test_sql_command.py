import time

from setting import get_engine

engine = get_engine()
with engine.connect() as connection:
    select_test = """
        SELECT * FROM events
        WHERE event_time >= '2017-06-22 00:00:00'
          AND event_time < '2017-06-23 00:00:00';
    """
    t = time.time()
    result = connection.execute(select_test)
    print(result)
    print(time.time() - t)

    print("INDEX")
    create_index = """
        CREATE INDEX idx_event_time ON events(event_time);
    """
    connection.execute(create_index)

    t = time.time()
    result = connection.execute(select_test)
    print(result)
    print(time.time() - t)