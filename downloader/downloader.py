#!/usr/bin/env python
# encoding: utf-8
import sys
import threading
import sqlite3
import time
import urllib2
import os
import hashlib
import signal
import Queue
import pymongo
import logging

NUM_THREAD = 20
work_queue_lock = threading.Lock()
update_database_lock = threading.Lock()

class Downloader(threading.Thread):
    def __init__(self, work_queue, output_dir, dbip_port, db_doc):
        threading.Thread.__init__(self)
        self.exit_event = threading.Event()
        self.work_queue = work_queue
        self.proxies = None
        #Define proxy below
        #self.proxies = {"http": ""}
        self.output_dir = output_dir
        self.current_file_size = 0
        self.file_size = 0
        self.dbip_port = dbip_port
        self.db_doc = db_doc
        (self.host, self.port) = dbip_port.split(':')
        self.port = int(self.port)
        (self.dbName, self.docname) = db_doc.split(':')
        logging.info('host:%s', self.host)


    def exit(self):
        print("%s: asked to exit." % self.getName())
        self.exit_event.set()
        self.join()
        return self.report()

    def report(self):
        if self.file_size == 0:
            return 0
        return float(self.current_file_size) / self.file_size

    def run(self):
        while not self.exit_event.isSet():
            work_queue_lock.acquire()
            if not self.work_queue.empty():
                self.url = self.work_queue.get()
                work_queue_lock.release()
                try:
                    self.download()
                    self.save()
                    self.update_database()
                except urllib2.HTTPError:
                    self.update_database(-1)
            else:
                work_queue_lock.release()
        print("%s: received exit event." % self.getName())

    def download(self):
        print("%s: downloading %s" % (self.getName(), self.url))
        self.current_file_size = 0
        self.file_size = 0
        proxy_handler = urllib2.ProxyHandler()
        if (self.proxies):
            proxy_handler = urllib2.proxyHandler(self.proxies);
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [
            ('User-Agent', r"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 "
                "(KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11"),
            ('Referer', self.url)
        ]
        urllib2.install_opener(opener)
        opening = urllib2.urlopen(self.url)
        meta = opening.info()
        # get the downloaed file name
        downloadurl = opening.url
        download_file_name = os.path.basename(downloadurl)

        self.file_size = int(meta.getheaders("Content-Length")[0])
        # use the same downloaded file name provied by the website
        temp_file_name = download_file_name
        # temp_file_name = "%d.apk" % (time.time() * 1000000)
        temp_dir = self.output_dir + os.sep + "temp"
        self.temp_output_path = temp_dir + os.sep + temp_file_name
        with open(self.temp_output_path, 'wb') as fil:
            block_size = 10240
            while True:
                buf = opening.read(block_size)
                self.current_file_size += len(buf)
                fil.write(buf)
                if not buf:
                    break

    def save(self):
        with open(self.temp_output_path, 'r') as fil:
            m = hashlib.md5()
            m.update(fil.read())
            md5_digest = m.hexdigest()
        new_output_path = self.output_dir + os.sep + md5_digest + ".apk"
        if os.path.isfile(new_output_path):
            os.remove(new_output_path)
        os.rename(self.temp_output_path, new_output_path)
        print("%s: %s.apk is completed." % (self.getName(), md5_digest))

    def update_database(self, result=1):
        update_database_lock.acquire()
        try:
            client = pymongo.MongoClient(host=self.host, port=self.port)
            tdb = client[self.dbName]
            tdbdoc = tdb[self.docname]
            tdbdoc.update({'url':self.url}, {'$set':{'downloaded':result}})
        except pymongo.errors.ConnectionFailure, e:
            print("%s: Operational Error" % e)
        finally:
            client.close()
            update_database_lock.release()

class Monitor(threading.Thread):
    def __init__(self, threads):
        threading.Thread.__init__(self)
        self.threads = threads
        self.exit_event = threading.Event()
    def exit(self):
        self.exit_event.set()
        self.join()
    def run(self):
        while not self.exit_event.isSet():
            for t in self.threads:
                if t.report() == 0:
                    print(" new"),
                else:
                    print("%3.0f%%" % (t.report()*100)),
            print("")
            time.sleep(1)

def get_undownloaded_url(dbip_port, db_doc):
    undownloaded_urls = []
    (host, port) = dbip_port.split(':')
    port = int(port)
    (dbName, docname) = db_doc.split(':')

    try:
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        tdbdoc = tdb[docname]
        # need to change to list from cursor type
        records = list(tdbdoc.find({'downloaded':{'$ne':1}}))
        undownloaded_urls = [r['url'] for r in records] 
    except pymongo.errors.ConnectionFailure, e:
        print("%s: get_undownloaded_url() Operational Error" % e)
    finally:
        client.close()

    return undownloaded_urls

def fill_work_queue(work_queue, undownloaded_urls):
    for u in undownloaded_urls:
        work_queue.put(u)

def import_work(work_queue, dbip_port, db_doc):
    undownloaded_urls = get_undownloaded_url(dbip_port, db_doc)
    fill_work_queue(work_queue, undownloaded_urls)
    return len(undownloaded_urls)

class Watcher:
    """this class solves two problems with multithreaded
    programs in Python, (1) a signal might be delivered
    to any thread (which is just a malfeature) and (2) if
    the thread that gets the signal is waiting, the signal
    is ignored (which is a bug).

    The watcher is a concurrent process (not thread) that
    waits for a signal and the process that contains the
    threads.  See Appendix A of The Little Book of Semaphores.
    http://greenteapress.com/semaphores/

    I have only tested this on Linux.  I would expect it to
    work on the Macintosh and not work on Windows.

    Refer to: http://code.activestate.com/recipes/496735-workaround-for-missed-sigint-in-multithreaded-prog/
    """

    def __init__(self):
        """ Creates a child thread, which returns.  The parent
            thread waits for a KeyboardInterrupt and then kills
            the child thread.
        """
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.watch()

    def watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            # I put the capital B in KeyBoardInterrupt so I can
            # tell when the Watcher gets the SIGINT
            print("KeyBoardInterrupt")
            self.kill()
        sys.exit()

    def kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError: pass

def main():
    if len(sys.argv) < 3:
        print("Usage: %s <MongoDB_ip:port> <dbname:docname> <output directory>" % (sys.argv[0]))
        sys.exit(1)
    else:
        dbip_port = sys.argv[1]
        db_doc = sys.argv[2]
        output_dir = sys.argv[3]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    temp_dir = output_dir + os.sep + "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    Watcher()
    threads = []
    work_queue = Queue.Queue()
    for i in range(NUM_THREAD):
        t = Downloader(work_queue, output_dir, dbip_port, db_doc)
        t.daemon = True
        t.start()
        threads.append(t)
    monitor_thread = Monitor(threads)
    monitor_thread.daemon = True
    monitor_thread.start()

    exit_flag = 0
    while exit_flag < 2:
        import_work(work_queue, dbip_port, db_doc)
        if work_queue.empty():
            exit_flag += 1
        else:
            exit_flag = 0
        while not work_queue.empty():
            time.sleep(10)
    for t in threads:
        t.exit()
    monitor_thread.exit()

if __name__ == '__main__':
    main()
