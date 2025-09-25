from flask import Flask, request, Response
import json

app = Flask(__name__)
events_by_epc = {}

@app.route("/epcis/capture", methods=["POST"])
def capture():
    doc = request.get_json(silent=True) or {}
    event_list = (doc.get("epcisBody") or {}).get("eventList") or []
    count = 0
    for ev in event_list:
        for epc in ev.get("epcList") or []:
            events_by_epc.setdefault(epc, []).append(ev)
            count += 1
    return Response(json.dumps({"status": "ok", "acceptedEvents": count}), status=201, mimetype="application/ld+json")

@app.route("/epcis/events", methods=["GET"])
def events():
    epc = request.args.get("EQ_epc")
    members = []
    if epc and epc in events_by_epc:
        for ev in events_by_epc[epc]:
            members.append({"epcisBody": {"eventList": [ev]}})
    return Response(json.dumps({"type": "Collection", "member": members}), mimetype="application/ld+json")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)