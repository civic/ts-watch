# -*- coding: utf-8 -*-

import argparse
import SimpleHTTPServer
import SocketServer
import threading
import time
import os


class WatchingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.detected_ts_files_timestamp = {}

    def is_typescript(self, filename):
        return filename[-3:] == ".ts" and filename[-5:] != ".d.ts"

    def is_updated(self, path, timestamp):
        update = False
        if path in self.detected_ts_files_timestamp:
            last_modified = self.detected_ts_files_timestamp[path]
            update = last_modified < timestamp
        else:
            update = True     #new file

        self.detected_ts_files_timestamp[path] = timestamp

        return update

    def ts_compile(self, target_ts_files):
        with open(".tscargs", "w") as f:
            f.writelines([s+"\n" for s in target_ts_files])
        os.system("tsc @.tscargs")


    def run(self):

        while self.running:
            target_ts_files = []
            updated_files = []

            for dirname, dirnames, filenames in os.walk("."):
                for filename in filter(self.is_typescript, filenames):

                    path = os.path.join(dirname, filename)

                    target_ts_files.append(path)
                    timestamp = os.stat(path).st_mtime

                    if self.is_updated(path, timestamp):
                        updated_files.append(path)

            if len(updated_files) > 0:
                print "Update files: " + (",".join(updated_files))
                self.ts_compile(target_ts_files)
                updated_files = []

            time.sleep(1)
        print "watcher thread shutdown"



def main():
    #filewatching thread
    t = WatchingThread()
    t.start()

    parser = argparse.ArgumentParser(description="typescript filewatche server")
    parser.add_argument('--port', default=8000, type=int, help="server port number (default:8000)")
    args = parser.parse_args()

    httpd = SocketServer.TCPServer(("", args.port), SimpleHTTPServer.SimpleHTTPRequestHandler);

    print "Start HTTPServer port {0} ...".format(args.port)
    try:
        httpd.serve_forever()
    finally:
        print "http server shutdown"
        t.running = False

if __name__ == '__main__':
    main();
