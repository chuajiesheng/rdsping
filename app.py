import boto3
import logging
import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'ok'


@app.route('/test')
def test():
    # Get configuration from environment variables
    endpoint = os.environ.get('DB_ENDPOINT')
    port = os.environ.get('DB_PORT', '5432')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    region = os.environ.get('AWS_REGION', 'us-east-1')
    dbname = request.args.get('connect_to', os.environ.get('DB_NAME', 'mydb'))
    aws_profile = os.environ.get('AWS_PROFILE', 'default')
    ssl_cert = os.environ.get('SSL_CERTIFICATE', 'SSLCERTIFICATE')

    # Validate required environment variables
    if not all([endpoint, user, dbname]):
        logging.error('Missing required environment variables: DB_ENDPOINT, DB_USER, DB_NAME')
        return jsonify({
            'status': 'error',
            'message': 'Error 1'
        }), 500

    try:
        if not password:
            logging.info('Attempting IAM authentication')

            session = boto3.Session(profile_name=aws_profile)
            client = session.client('rds')
            token = client.generate_db_auth_token(
                DBHostname=endpoint,
                Port=port,
                DBUsername=user,
                Region=region
            )
        else:
            logging.info('Using password authentication')

        # Attempt database connection
        conn = psycopg2.connect(
            host=endpoint,
            port=port,
            database=dbname,
            user=user,
            password=password or token,
            sslrootcert=ssl_cert
        )
        cur = conn.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()

        # Close connections
        cur.close()
        conn.close()

        return jsonify({
            'status': 'success',
            'timestamp': str(query_results[0][0]) if query_results else None
        }), 200

    except Exception as e:
        logging.error(f'Database connection failed: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'Error 2'
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
