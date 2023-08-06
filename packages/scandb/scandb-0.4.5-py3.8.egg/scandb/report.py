import argparse
import json
from docxtpl import DocxTemplate, RichText

from scandb.models import init_db
from scandb.models import Vuln



def report_cli():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--db", type=str, required=False, default="scandb.sqlite")
    args = parser.parse_args()

    # initialize the database
    database = init_db(args.db)

    ids = Vuln.select(Vuln.plugin_id).where(Vuln.severity >= 3).distinct()
    vulns_by_plugin = {k: [] for k in ids}

    for i in ids:
        count = 1
        vulns = Vuln.select().where(Vuln.plugin_id== i.plugin_id)

        for v in vulns:
            if count ==1:
                print("Plugin-ID: {0}".format(vulns[0].plugin_id))
                print("Plugin-Name: {0}".format(vulns[0].plugin_name))
                print("Plugin-Desc: {0}".format(vulns[0].description))
                print("Plugin-Solution: {0}".format(vulns[0].solution))
                count += 1
            temp = v.plugin
            try:
                plugin = json.loads(temp)
                if plugin['plugin_output']:
                    output = plugin['plugin_output']
                else:
                    output = ""
            except:
                x = temp.find("plugin_output")
                if x > -1:
                    output = temp[x+13:]
                else:
                    output = ""
            print(v.host.address, v.port, v.protocol, v.service)#, output)
