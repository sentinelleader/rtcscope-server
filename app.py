from influxdb import InfluxDBClient
import json, time, os
from flask import Flask, request, Response, send_from_directory, abort
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


app = Flask(__name__, static_url_path='/static')
app.config['DEBUG'] = True

client = InfluxDBClient('localhost', 8086, 'test', 'test', 'mydb')

def collect_real_stats(graph_type, graph_dur, graph_int):
  json_arr = {}
  query = "SELECT mean(" + graph_type + ") FROM rtc_stats WHERE time > now() - " + graph_dur + " GROUP BY time(" + graph_int + "), id"
  result = client.query(query)
  for i in (result.keys()):
    json_id =  (i[1])['id']
    json_arr[json_id] = list(result.get_points(tags={"id": json_id}))
  return json.dumps(json_arr)

def collect_call_stats(graph_type, graph_id):
  json_arr = {}
  query = "SELECT (" + graph_type + ") FROM rtc_stats WHERE id ='" + graph_id + "'"
  print "query -> %s" %query
  result = client.query(query)

# NOTE
#
# Currently Adhoc query in InfluxDB cannot aggregate with out a time WHERE condition in the query
# Hence getting the start/end time of the call and then use that time interval for proper aggregation
#

  call_start_time = (list(result.get_points(measurement='rtc_stats'))[0])['time']
  call_end_time = (list(result.get_points(measurement='rtc_stats'))[-1])['time']
  agg_query = "SELECT MEAN(" + graph_type + ") FROM rtc_stats WHERE id ='" + graph_id + "' AND time >='" + call_start_time + "' AND time <='" + call_end_time + "' GROUP by time(1m)"
  print "query -> %s" %agg_query
  result = client.query(agg_query)
  json_arr = list(result.get_points(measurement='rtc_stats'))
  return json.dumps(json_arr)

def write_metrics(metric_array):
  data_points = {}
  data_points["tags"] = {}
  data_points["fields"] = {}
  data_points["measurement"] = "rtc_stats"
  data_points["tags"]["id"] = metric_array[0]
  data_points["times"] = metric_array[2]
  for i in metric_array[1].split(','):
    field_array = i.split("=")
    data_points["fields"][field_array[0]] = float(field_array[1])
  result = client.write_points([data_points])
  return result

@app.route('/v1/stats/write/', methods=['POST'])
#@crossdomain(origin='*')
def write_stats():
  data_array = (request.form['rtc_stats,id']).split(" ")
  resp = write_metrics(data_array)
  if resp == True:
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
  else:
    abort(500)

@app.route('/v1/stats/', methods=['GET'])
@crossdomain(origin='*')
def get_stats():
  graph_type = request.args['type']
  default_duration = "5m"
  default_interval = "10s"
  json_data = collect_real_stats(graph_type, default_duration, default_interval)
  return json_data, 200

@app.route("/v1/stats/<call_id>/", methods=['GET'])
@crossdomain(origin='*')
def get_results(call_id):
  arg = request.args['type']
  json_data = collect_call_stats(arg, call_id)
  return json_data, 200

@app.route("/graph/<graph_name>/")
def gen_graph(graph_name):
  file_name = graph_name + ".html"
  return app.send_static_file(file_name)

@app.route("/demo")
def load_demo():
  return app.send_static_file('demo.html')

@app.route("/dashboard")
def load_test():
  return app.send_static_file('dashboard.html')

@app.route('/dashboard/<filename>')
def serve_html_static(filename):
    root_dir = "/opt/rtcscope-server"
    return send_from_directory(os.path.join(root_dir, 'static', 'types'), filename)

@app.route('/js/<path:filename>')
def serve_js_static(filename):
    root_dir = "/opt/rtcscope-server"
    return send_from_directory(os.path.join(root_dir, 'static', 'js'), filename)

@app.route('/css/<path:filename>')
def serve_css_static(filename):
    root_dir = "/opt/rtcscope-server"
    return send_from_directory(os.path.join(root_dir, 'static', 'css'), filename)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)
