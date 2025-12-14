import psycopg2

try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    conn.autocommit = True
    cur = conn.cursor()
    
    # Terminate existing connections
    cur.execute('SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s AND pid <> pg_backend_pid()', ('govfunds',))
    
    # Drop and recreate database
    cur.execute('DROP DATABASE IF EXISTS govfunds')
    cur.execute('CREATE DATABASE govfunds')
    cur.close()
    conn.close()
    print('✓ Database reset successfully')
except Exception as e:
    print(f'Error: {e}')
