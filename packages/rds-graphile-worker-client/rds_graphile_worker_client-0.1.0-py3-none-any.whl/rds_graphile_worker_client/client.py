import boto3
import psycopg2
import json
import os

class RdsGraphileWorkerClient():

    def __init__(self, aws_region, pg_username, pg_hostname, pg_port, pg_dbname):

        rds = boto3.client('rds', region_name=aws_region)

        token = rds.generate_db_auth_token(
          Region=aws_region,
          DBHostname=pg_hostname,
          Port=pg_port,
          DBUsername=pg_username
        );

        #TODO: attempt to replace this with connection pool psycopg2.pool.SimpleConnectionPool
        self.conn = psycopg2.connect(sslmode='verify-full', sslrootcert=os.path.join(os.path.dirname(__file__), 'rds-ca-2019-root.pem'), dbname=pg_dbname, user=pg_username, host=pg_hostname, port=pg_port, password=token)

    def __del__(self):
        #self.conn.close()
        pass

    def quick_add_job(self, task_name, task_data):
        assert type(task_name) is str
        cur = self.conn.cursor()
        cur.execute("SELECT graphile_worker.add_job(%s, %s)", (task_name, json.dumps(task_data)))
        response = cur.fetchone()
        self.conn.commit()
        cur.close()
        return response 

