##################################################
# file: otis_soap_server.py
#
# skeleton generated by "ZSI.generate.wsdl2dispatch.ServiceModuleWriter"
#      /usr/bin/wsdl2py --complexType OTIS_testinterface_v003.wsdl
#
##################################################

from ZSI.schema import GED, GTD
from ZSI.TCcompound import ComplexType, Struct
from otis_soap_types import *
from ZSI.ServiceContainer import ServiceSOAPBinding

# Messages  
StartTreinstelOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "StartTreinstelOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

StopTreinstelOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "StopTreinstelOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

PauzeerTreinstelOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "PauzeerTreinstelOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

HervatTreinstelOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "HervatTreinstelOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

PlaatsTreinstelOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "PlaatsTreinstelOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

StopGPSDekkingOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "StopGPSDekkingOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

HervatGPSDekkingOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "HervatGPSDekkingOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

MaakTestcasesOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "MaakTestcasesOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass

MaakXMLBronBestandOpdrachtInput = GED("http://www.ns.nl/schemas/testinterface.xsd", "MaakXMLBronBestandOpdracht").pyclass

OpdrachtOutput = GED("http://www.ns.nl/schemas/testinterface.xsd", "Status").pyclass


# Service Skeletons
class OtisService(ServiceSOAPBinding):
    soapAction = {}
    root = {}

    def __init__(self, post='/otis_soap', **kw):
        ServiceSOAPBinding.__init__(self, post)

    def soap_StartTreinstel(self, ps, **kw):
        request = ps.Parse(StartTreinstelOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/foo'] = 'soap_StartTreinstel'
    root[(StartTreinstelOpdrachtInput.typecode.nspname,StartTreinstelOpdrachtInput.typecode.pname)] = 'soap_StartTreinstel'

    def soap_StopTreinstel(self, ps, **kw):
        request = ps.Parse(StopTreinstelOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/stoptrein'] = 'soap_StopTreinstel'
    root[(StopTreinstelOpdrachtInput.typecode.nspname,StopTreinstelOpdrachtInput.typecode.pname)] = 'soap_StopTreinstel'

    def soap_PauzeerTreinstel(self, ps, **kw):
        request = ps.Parse(PauzeerTreinstelOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/pauzeertrein'] = 'soap_PauzeerTreinstel'
    root[(PauzeerTreinstelOpdrachtInput.typecode.nspname,PauzeerTreinstelOpdrachtInput.typecode.pname)] = 'soap_PauzeerTreinstel'

    def soap_HervatTreinstel(self, ps, **kw):
        request = ps.Parse(HervatTreinstelOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/hervattrein'] = 'soap_HervatTreinstel'
    root[(HervatTreinstelOpdrachtInput.typecode.nspname,HervatTreinstelOpdrachtInput.typecode.pname)] = 'soap_HervatTreinstel'

    def soap_PlaatsTreinstel(self, ps, **kw):
        request = ps.Parse(PlaatsTreinstelOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/plaatstrein'] = 'soap_PlaatsTreinstel'
    root[(PlaatsTreinstelOpdrachtInput.typecode.nspname,PlaatsTreinstelOpdrachtInput.typecode.pname)] = 'soap_PlaatsTreinstel'

    def soap_StopGPSDekking(self, ps, **kw):
        request = ps.Parse(StopGPSDekkingOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/stopgpsdekking'] = 'soap_StopGPSDekking'
    root[(StopGPSDekkingOpdrachtInput.typecode.nspname,StopGPSDekkingOpdrachtInput.typecode.pname)] = 'soap_StopGPSDekking'

    def soap_HervatGPSDekking(self, ps, **kw):
        request = ps.Parse(HervatGPSDekkingOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/hervatgpsdekking'] = 'soap_HervatGPSDekking'
    root[(HervatGPSDekkingOpdrachtInput.typecode.nspname,HervatGPSDekkingOpdrachtInput.typecode.pname)] = 'soap_HervatGPSDekking'

    def soap_MaakTestcases(self, ps, **kw):
        request = ps.Parse(MaakTestcasesOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/maaktestcases'] = 'soap_MaakTestcases'
    root[(MaakTestcasesOpdrachtInput.typecode.nspname,MaakTestcasesOpdrachtInput.typecode.pname)] = 'soap_MaakTestcases'

    def soap_MaakXMLBronBestand(self, ps, **kw):
        request = ps.Parse(MaakXMLBronBestandOpdrachtInput.typecode)
        return request,OpdrachtOutput()

    soapAction['http://otis.ns.nl/maakxmlbronbestand'] = 'soap_MaakXMLBronBestand'
    root[(MaakXMLBronBestandOpdrachtInput.typecode.nspname,MaakXMLBronBestandOpdrachtInput.typecode.pname)] = 'soap_MaakXMLBronBestand'

