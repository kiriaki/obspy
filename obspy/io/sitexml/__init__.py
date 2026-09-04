# -*- coding: utf-8 -*-
"""
obspy.io.sitexml - SiteXML read and write support for ObsPy
=================================================================

:author:
    Kiriaki Konstantinidou (kiriaki@itsak.gr), Apr 2026
:copyright:
    ORFEUS, 2026
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""

from .sitexml import (read_sitexml, write_sitexml, validate_sitexml,
                      sitexml_to_sitedict, sitedict_to_sitexml,
                      add_sitexml_reference)
from .tabular import (csv_to_sera_site, excel_to_sera_site,
                      add_velocity_profiles)
from .util import (SiteXMLError, SiteXMLIOError, SiteXMLImportError,
                   SiteXMLValidationError)