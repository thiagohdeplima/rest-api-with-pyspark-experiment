import os
import pickle

import redis
import workers

from flask import Flask, jsonify, request

app = Flask(__name__)
rconn = redis.Redis.from_url(os.environ['REDIS_URL'])

@app.route('/v1/stats', methods=['GET'])
def get_v1_stats():
  stats = rconn.get('stats')

  if stats is None:
    return 404, jsonify({
      'error': 'not_found'
    })

  return jsonify(pickle.loads(stats))

@app.route('/v1/files', methods=['POST'])
def post_v1_stats():
  url = request.json.get('url')

  if url is None:
    raise ValidationException(
      status_code=422,
      payload={'errors': {'url': 'is missing'}}
    )

  workers.perform_file_operations.delay(url)

  return jsonify({'url': url})

class ValidationException(Exception):
  status_code = 400

  def __init__(self, status_code=None, payload=None):
    Exception.__init__(self)

    if status_code is not None:
      self.status_code = status_code

    self.payload = payload

  def to_dict(self):
    return self.payload

@app.errorhandler(ValidationException)
def handle_invalid_usage(error):
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  
  return response