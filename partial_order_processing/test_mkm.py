import os

from django.conf import settings
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.objects.log.importer.xes import importer
from pm4py.visualization.petrinet import visualizer as pn_vis


def execute_script():
    event_logs_path = os.path.join(settings.MEDIA_ROOT, "event_logs")
    event_log = os.path.join(event_logs_path, 'repairExample.xes')
    log = importer.apply(event_log)

    net, i_m, f_m = alpha_miner.apply(log)

    gviz = pn_vis.apply(net, i_m, f_m,
                        parameters={pn_vis.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg",
                                    pn_vis.Variants.WO_DECORATION.value.Parameters.DEBUG: False})
    pn_vis.view(gviz)

    if __name__ == "__main__":
        execute_script()
