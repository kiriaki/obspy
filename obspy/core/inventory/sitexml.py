#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides the SiteCharacterization class.

:copyright:
    ORFEUS, 2025
:license:
    GNU Lesser General Public License, Version 3
    (https://www.gnu.org/copyleft/lesser.html)
"""
#import copy
#import fnmatch
#import warnings

#import numpy as np

#from obspy import UTCDateTime
from obspy.core.util.base import ComparingObject
#from obspy.core.util.obspy_types import (ObsPyException, ZeroSamplingRate,
#                                         FloatWithUncertaintiesAndUnit)
#from obspy.core.event import ResourceIdentifier
from obspy.core.inventory.sitexml_header import (TopographySchemaA, TopographySchemaB, 
                                                 _sitexml_check_type, _sitexml_check_enum)
#from obspy.geodetics import inside_geobounds

#from .util import (BaseNode, Equipment, Operator, Distance, Latitude,
#                   Longitude, Site, _unified_content_strings_expanded)


class SERASite(ComparingObject):
    """
    This is the parent class for the siteXML object tree.
    """
    def __init__(self, station_code, site_description=None, site_characterization_parameters=None, overall_quality_index=None):
        """
        :type station_code: str
        :param station_code: Not used in SiteXML, but is needed in order to correlate with the Station Object
        :type site_description: :class:`~obspy.core.inventory.sitexml.SiteDescription`
        :param analysis_publicID: The site description parameters (H800, Bedrock depth, EC8 class, geological unit, morphology, topology)
        :type site_characterization_parameters: :class:`~obspy.core.inventory.sitexml.SiteCharacterizationParameters`
        :param site_characterization_parameters: The site characterization parameters (VS30, resonance frequency, velocity profiles)
        :type overall_quality_index: float
        :param overall_quality_index: The overall quality index of the site characterization parameters.
        """
        self.station_code = station_code
        
        self.site_description = _sitexml_check_type(
            site_description, SiteDescription, "site_description", True)

        self.site_characterization_parameters = _sitexml_check_type(
            site_characterization_parameters, SiteCharacterizationParameters, "site_characterization_parameters", True)
        
        # TO CHECK: If this one is calculated it should be removed from the parameters 
        self.overall_quality_index = overall_quality_index
       
class SiteDescription(ComparingObject):
    def __init__(self, latitude, longitude, altitude=None, minDistanceFromStation=None, maxDistanceFromStation=None, 
                 EC8=None, bedrock_depth=None, H800=None, geological_unit=None, morphology=None, topologyA=None, topologyB=None):
        """
        :type latitude: :class:`~obspy.core.inventory.util.Latitude`
        :param latitude: The latitude of the site
        :type longitude: :class:`~obspy.core.inventory.util.Longitude`
        :param longitude: The longitude of the site
        :type altitude: float (maybe CustomFloat??)
        :param altitude: Elevation of ground with respect to sea level (m)
        :type minDistanceFromStation: float (maybe CustomFloat??)
        :param minDistanceFromStation: Minimum distance between the permanent seismological station and 
            site characterization measurement. Should be used only when representative latitude and longitude 
            of site characterization measurements cannot be provided.
        :type maxDistanceFromStation: float (maybe CustomFloat??)
        :param maxDistanceFromStation: Maximum distance between the permanent seismological station and 
            site characterization measurement. Should be used only when representative latitude and longitude 
            of site characterization measurements cannot be provided.
        :type EC8: :class:`~obspy.core.inventory.sitexml.EC8`
        :param EC8: Ground type according to Eurocode 8, based on the velocity S30 value and geotechnical description
        :type H800: :class:`~obspy.core.inventory.sitexml.H800`
        :param H800: Depth beyond which the shear-wave velocity Vs exceeds 800 m/s.
        :type bedrock_depth: :class:`~obspy.core.inventory.sitexml.BedrockDepth`
        :param bedrock_depth: 
        :type geological_unit: str
        :param geological_unit: Brief description of the surface geology (free text)
        :type morphology: str (Enum)
        :param morphology: Qualitative description of the shape of the earth's surface
        :type topologyA: str
        :param topologyA: Quantitative description of the surface according to the Italian Code 
            (detailed description of the scheme in SERA Deliverable D7.1 - Appendix I).
            See :class:`~obspy.core.inventory.sitexml_header.TopographySchemaA` for allowed values.
        :type topologyB: str
        :param topologyB: Quantitative description of the shape of the earth's surface according to 
            Burjanek et al, 2014 (detailed description of the scheme in SERA Deliverable D7.1 - Appendix I). 
            See :class:`~obspy.core.inventory.sitexml_header.TopographySchemaB` for allowed values.
        """
        # Topology and topography have the same meaning ?
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.minDistanceFromStation = minDistanceFromStation
        self.maxDistanceFromStation = maxDistanceFromStation

        self.EC8 = _sitexml_check_type(EC8, EC8_class, "EC8", True)
        self.bedrock_depth = _sitexml_check_type(bedrock_depth, BedrockDepth, "bedrock_depth", True)
        self.H800 = _sitexml_check_type(H800, H800_class, "H800", True)
        self.geological_unit = _sitexml_check_type(geological_unit, GeologicalUnit, "geological_unit", True)
        
        self.morphology = morphology
        
        self.topologyA = _sitexml_check_enum(topologyA, TopographySchemaA, "topologyA", True)
        self.topologyB = _sitexml_check_enum(topologyB, TopographySchemaB, "topologyB", True)

class SiteCharacterizationParameters(ComparingObject):
    def __init__(self, publicID=None, analysis_publicID=None, resonance_frequency=None, velocity_s30=None, 
                 velocity_profile_count=None, velocity_profile=None, spt_logs_count=None, cpt_logs_count=None, 
                 borehole_logs_count=None):
        """
        :type publicID: :class:`~obspy.core.event.resourceid.ResourceIdentifier`
        :param publicID: All channels belonging to this station.
        :type analysis_publicID: :class:`~obspy.core.event.resourceid.ResourceIdentifier`
        :param analysis_publicID: The lexical description of the site
        :type resonance_frequency: :class:`~obspy.core.inventory.sitexml.ResonanceFrequency`
        :param resonance_frequency: The Resonance frequency of the soil column 
        :type velocity_s30: :class:`~obspy.core.inventory.sitexml.velocityS30`
        :param velocity_s30: Average shear-wave velocity between 0 and 30 meters depth
        :type velocity_profile_count: int
        :param velocity_profile_count: Number of available velocity profiles
        :type velocity_profile: list of :class:`~obspy.core.inventory.sitexml.VelocityProfile`
        :param velocity_profile: List of velocity profiles
        :type spt_logs_count: int
        :param spt_logs_count: Number of available SPT profile(s)
        :type cpt_logs_count: int
        :param cpt_logs_count: Number of available CPT profile(s)
        :type borehole_logs_count: int
        :param borehole_logs_count: Number of available borehole log profile(s)
       """
        self.publicID = publicID        
        self.analysis_publicID = analysis_publicID   
        self.resonance_frequency = _sitexml_check_type(resonance_frequency, ResonanceFrequency, "resonance_frequency", True)
        self.velocity_s30 = _sitexml_check_type(velocity_s30, velocityS30, "velocity_s30", True)
        self.velocity_profile_count = velocity_profile_count
        self.velocity_profile = velocity_profile or []
        self.spt_logs_count = spt_logs_count
        self.cpt_logs_count = cpt_logs_count
        self.borehole_logs_count = borehole_logs_count
        
class VelocityProfile(ComparingObject):
    def __init__(self, layer_count, velocity_profile_data):
        self.layer_count = layer_count
        self.velocity_profile_data = velocity_profile_data
                 
class VelocityProfileData(ComparingObject):
    # parameters here are values with uncertainties
    # This could be modeled with a list of [name, value, uncertainty] where name is one of density, velocityS, etc.
    def __init__(self, density, velocityP, velocityS, layer_top_depth, layer_bottom_depth):
        self.density = density
        self.velocityP = velocityP
        self.velocityS = velocityS
        self.layerTopDepth = layer_top_depth
        self.layerBottomDepth = layer_bottom_depth

class SiteIndicator(ComparingObject):
    def __init__(self, name, value, uncertainty=None, methods=None, quality_index=None, literature_source=None, external_reference=None):
        self.name = name
        self.value = value
        self.uncertainty = uncertainty
        self.methods = methods or []
        self.quality_index = quality_index
        self.literature_source = literature_source
        self.external_reference = external_reference

class H800_class(SiteIndicator):
    def __init__(self, value, uncertainty=None, methods=None, 
                 quality_index=None, literature_source=None, 
                 external_reference=None):
        super(H800_class, self).__init__(
            name="H800", value=value, uncertainty=uncertainty, methods=methods, 
            quality_index=quality_index, literature_source=literature_source, 
            external_reference=external_reference)

class EC8_class(SiteIndicator):
    def __init__(self, value, uncertainty=None, methods=None, 
                 quality_index=None, literature_source=None, 
                 external_reference=None):
        super(EC8_class, self).__init__(
            name="EC8", value=value, uncertainty=uncertainty, methods=methods, 
            quality_index=quality_index, literature_source=literature_source, 
            external_reference=external_reference)

class BedrockDepth(SiteIndicator):
    def __init__(self, value, uncertainty=None, methods=None, 
                 quality_index=None, literature_source=None, 
                 external_reference=None):
        super(BedrockDepth, self).__init__(
            name="bedrock_depth", value=value, uncertainty=uncertainty, methods=methods, 
            quality_index=quality_index, literature_source=literature_source, 
            external_reference=external_reference)

class GeologicalUnit(SiteIndicator):
    def __init__(self, value, uncertainty=None, methods=None, 
                 quality_index=None, literature_source=None, 
                 external_reference=None, geological_map_scale=None, geological_unit_OGE=None):
        self.geological_map_scale = geological_map_scale
        self.geological_unit_OGE = geological_unit_OGE
        super(GeologicalUnit, self).__init__(
            name="geological_unit", value=value, uncertainty=uncertainty, methods=methods, 
            quality_index=quality_index, literature_source=literature_source, 
            external_reference=external_reference)
        
class ResonanceFrequency(SiteIndicator):
    def __init__(self, value, uncertainty=None, methods=None, 
                 quality_index=None, literature_source=None, 
                 external_reference=None):
        super(ResonanceFrequency, self).__init__(
            name="resonance_frequency", value=value, uncertainty=uncertainty, methods=methods, 
            quality_index=quality_index, literature_source=literature_source, 
            external_reference=external_reference)
        
class velocityS30(SiteIndicator):
    def __init__(self, value, uncertainty=None, methods=None, 
                 quality_index=None, literature_source=None, 
                 external_reference=None, method_combined_quality_index=None, manual_quality_index=None):
        self.method_combined_quality_index = method_combined_quality_index
        self.manual_quality_index = manual_quality_index
        super(velocityS30, self).__init__(
            name="velocity_s30", value=value, uncertainty=uncertainty, methods=methods, 
            quality_index=quality_index, literature_source=literature_source, 
            external_reference=external_reference)
        
class LiteratureSource(ComparingObject):
    def __init__(self, title, firstAuthor=None, secondaryAuthors=None, year=None, booktitle=None, language=None, DOI=None):
        self.title = title
        self.firstAuthor = firstAuthor
        self.secondaryAuthors = secondaryAuthors
        self.year = year
        self.booktitle = booktitle
        self.language = language
        self.DOI = DOI
        
if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
