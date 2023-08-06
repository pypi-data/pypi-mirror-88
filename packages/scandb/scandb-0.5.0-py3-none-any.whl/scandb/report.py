import argparse
import json
from docxtpl import DocxTemplate, RichText

from scandb.models import init_db
from scandb.models import Vuln, ReportVuln
from scandb.models import Host

from io import StringIO, BytesIO ## for Python 3

def dbvuln_to_reportvuln(v):
    """

    :param dbvuln: Vuln
    :return:
    """
    vuln = ReportVuln ( address =v.host.address, description =v.description, synopsis=v.synopsis, port=v.port,
                        protocol=v.protocol, service=v.service, solution=v.solution, severity=v.severity,
                        xref=v.xref, info=v.info, plugin_id=v.plugin_id, plugin_name=v.plugin_name, plugin=v.plugin,
                        plugin_family=v.plugin_family, plugin_output=v.plugin_output,  risk=v.risk)
    return vuln


def get_plugin_ids(min_severity = 0):
    ids = Vuln.select(Vuln.plugin_id).where(Vuln.severity >= min_severity).distinct()
    result = [i.plugin_id for i in ids]
    return result


def get_vulns_by_plugin(pid):
    result = Vuln.select().where(Vuln.plugin_id == pid)
    vulns = [dbvuln_to_reportvuln(v) for v in result]
    return vulns


def create_vuln_by_plugin_map(min_severity = 0):
    """
    This function creates a dictionary with plugin-ids as key. The values for each entry is a list of detected
    vulnerabilities.

    :param min_severity: minimum severity (default = 0)
    :type: int
    :return: dictonary with a list of vulnerabilites per plugin
    :rtype: dict
    """
    ids = get_plugin_ids(min_severity=min_severity)
    vulns_by_plugin = {k: [] for k in ids}

    for i in ids:
        vulns_by_plugin[i].append(get_vulns_by_plugin(i))
    return vulns_by_plugin


def get_ips(min_severity = 0):
    result = Vuln.select(Host.address).join(Host).where(Vuln.severity >= min_severity).distinct()
    ips = [i.host.address for i in result]
    return ips


def get_vuln_by_ip(ip, min_severity=0):
    result = Vuln.select(Vuln).join(Host).where(Host.address == ip and Vuln.severity >= min_severity )
    vulns = [dbvuln_to_reportvuln(v) for v in result]
    return vulns


def get_vulns(min_severity=0):
    result = Vuln.select(Vuln).join(Host).where(Vuln.severity >= min_severity)
    vulns = [dbvuln_to_reportvuln(v) for v in result]
    return vulns


def create_vuln_by_ip_map(min_severity=0):
    """
        This function creates a dictionary with ip addresses as key. The values for each entry is a list of detected
        vulnerabilities.

        :param min_severity: minimum severity (default = 0)
        :type: int
        :return: dictonary with a list of vulnerabilites per ip
        :rtype: dict
        """
    # creating a dict with ip addresses as key and an empty list as value
    ips = get_ips(min_severity=min_severity)
    vulns_by_host = {k: [] for k in ips}
    for ip in ips:
        vulns_by_host[ip].append(get_vuln_by_ip(ip, min_severity=min_severity))

    return vulns_by_host


def write_to_template(template, vulns, vulns_by_plugin, vulns_by_host):
    doc = DocxTemplate(template)
    context = {'port_statistics': [], 'vuln_statistics': [], 'host_portlist' : [], 'vulns' : vulns,
               'vulns_by_plugin': vulns_by_plugin, 'vulns_by_host': vulns_by_host}
    doc.render(context)
    doc.save("scandb-report.docx")


def report_cli():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--db", type=str, required=False, default="scandb.sqlite")
    parser.add_argument("--min-severity", type=int, required=False, default=0,
                        help="Minimum severity level (default: 0)")
    parser.add_argument("--template", type=str, required=False, default="scandb-template.docx",
                        help="Name of the template to render")
    args = parser.parse_args()

    # initialize the database
    database = init_db(args.db)

    vulns = get_vulns(args.min_severity)
    vulns_by_plugin = create_vuln_by_plugin_map(args.min_severity)
    vulns_by_host = create_vuln_by_ip_map(args.min_severity)

    write_to_template(args.template, vulns=vulns, vulns_by_plugin=vulns_by_plugin, vulns_by_host=vulns_by_host)