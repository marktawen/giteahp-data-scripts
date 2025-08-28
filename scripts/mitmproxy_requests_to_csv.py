import mitmproxy
from datetime import datetime
import math

class RequestsToCSV: 
  def load(self, loader):
    
    self.file_handle = open("requests-" + datetime.now().isoformat().split(".")[0].replace(":", "_") + ".csv", "w")
    self.file_handle.write("Request,Start Time,EndTime,Source,User Agent,Request Method,Path,Status,Response Size Raw (bytes),Response Size Uncompressed (bytes),Duration (ms)\n")
    self.file_handle.flush()
    self.request_count = 0

  def done(self):
    self.file_handle.close()
  
  def response(self, flow: mitmproxy.http.HTTPFlow):
    start_time = datetime.fromtimestamp(flow.request.timestamp_start).isoformat()
    end_time = datetime.fromtimestamp(flow.response.timestamp_end).isoformat()
    duration = str((flow.response.timestamp_end - flow.request.timestamp_start) * 1000).split(".")[0]

    self.request_count += 1
    self.file_handle.write(str(self.request_count) + "," + start_time + "," + end_time + "," + flow.client_conn.address[0] + "," + flow.request.headers.get("User-Agent", "").replace(",", " ") + "," + flow.request.method + "," + flow.request.path + "," + str(flow.response.status_code) + "," + str(len(flow.response.raw_content)) + "," + str(len(flow.response.content)) + "," + str(duration) + "\n")
    self.file_handle.flush()


addons = [
  RequestsToCSV()
]