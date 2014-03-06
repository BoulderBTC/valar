from celery import Celery
import datetime


import logging
import time
from valar.utils import db
from valar.utils import hosts, get_summaries, get_devices, hosts, send_mail
from valar.fabfile import restart
from valar import celeryconfig

app = Celery('tasks')

app.config_from_object(celeryconfig)


@app.task
def save_miner_stats():
    sums = get_summaries()
    devs = get_devices()
    payload = []

    for s in hosts:
        if s["name"] not in sums:
            sums[s["name"]] = {"SUMMARY": [{'MHS 5s': 0}]}

        logging.info(s['name'] + ': ' + str(sums[s['name']]['SUMMARY'][0]['MHS 5s']) + ' MH/s')
        now = datetime.datetime.now()
        payload.append({
            'hashrate': int(sums[s['name']]['SUMMARY'][0]['MHS 5s'] * 1000),
            'miner': s['_id'],
            'when': now.strftime('%a, %d %b %Y %X GMT'),
        })

    db.stat.insert(payload)

    if devs["err"]:
        for h in devs["err"]:
            restarted = db.restarts.find_one({"hostname": h["hostname"]})
            if restarted:
                if (time.time() - restarted["when"]) / 60 > 10:
                    restarted["when"] = time.time()
                    db.restarts.save(restarted)
                    restart(h["hostname"])
            elif not restarted:
                db.restarts.insert({"hostname": h["hostname"], "when": time.time()})
                restart(h["hostname"])

            send_mail(subject="Valar ERROR", message="Error\n\n{0}".format(", ".join([x["name"] for x in devs["err"]])))

    return True
