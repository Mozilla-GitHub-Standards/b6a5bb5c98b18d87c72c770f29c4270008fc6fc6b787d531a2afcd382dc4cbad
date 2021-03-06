from gettext import gettext as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from mozdns.soa.models import SOA
from mozdns.view.models import View
from mozdns.mozbind.zone_builder import build_zone_data

import simplejson as json


def build_debug_soa(request, soa_pk):
    soa = get_object_or_404(SOA, pk=soa_pk)
    # DEBUG_BUILD_STRING = build_zone(soa, root_domain)
    # Figure out what sort of domains are in this zone.
    try:
        private_view = View.objects.get(name='private')
        public_view = View.objects.get(name='public')

        private_data = build_zone_data(private_view, soa.root_domain, soa)
        private_data = private_data.format(serial=soa.serial)

        public_data = build_zone_data(public_view, soa.root_domain, soa)
        public_data = public_data.format(serial=soa.serial)

        output = _(
            """
;======= Private Data =======
{0}

;======= Public Data =======
{1}
        """.format(private_data, public_data))
    except Exception:
        return HttpResponse(json.dumps(
            {"error": "HOLY SHIT SOMETHING WENT WRONG!!!"}))
    return render(request, 'mozbind/sample_build.html',
                  {'data': output, 'soa': soa})
