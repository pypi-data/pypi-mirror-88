#!/usr/bin/env python3
import json
import sys

from dwq import Job, Disque

def main():
    Disque.connect(["localhost:7711"])
    disque = Disque.get()
    queues = sys.argv[1:] or ["default"]
    try:
        while True:
            jobs = Job.get(queues, count=1024, nohang=True)
            if not jobs:
                return

            job_ids = []
            for job in jobs:
                job_ids.append(job.job_id)

            disque.fast_ack(*job_ids)
    except KeyboardInterrupt:
        pass

if __name__=="__main__":
    main()
