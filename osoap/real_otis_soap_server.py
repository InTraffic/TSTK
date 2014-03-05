
from   osoap.otis_soap_server import OtisService
from   osoap.command_message  import CommandMessage
import logging
import zmq

class RealOtisService(OtisService):
    def __init__(self, id, **kw):
        OtisService.__init__(self, **kw)
        self.id = id
        self.logger = logging.getLogger('otis_soap.service')
        # ZeroMQ always needs a context
        self.context = zmq.Context(1)
        address = "tcp://*:9500"
        self.logger.info( "Publishing on "  + address )
        self.repeater_socket = self.context.socket( zmq.PUB )
        self.repeater_socket.bind( address )

    _wsdl = ""

    #ok response
    def result_ok(self, response):
        response._Code = "Done."
        return response 

    #not ok response
    def result_nok(self, response):
        response._Code = "Failure"
        return response

    def notify(self, message):
        pass

    def soap_StopTreinstel(self, ps, **kw):
        request, response = OtisService.soap_StopTreinstel(self, ps, **kw)
        response = self.result_ok(response)
        self.logger.info( "Stop Treinstel")
        message  = CommandMessage("stop")
        message.treinstel  = request.get_element_Treinstelnummer()
        self.repeater_socket.send_pyobj(message)
        return request, response

    def soap_StartTreinstel(self, ps, **kw):
        request, response = OtisService.soap_StartTreinstel(self, ps, **kw)
        response = self.result_ok(response)
        self.logger.info( "Start Treinstel")
        message  = CommandMessage("start")
        message.treinstel  = request.get_element_Treinstelnummer()
        message.plaats     = request.get_element_Plaats()
        message.bestemming = request.get_element_Bestemming()
        self.repeater_socket.send_pyobj(message)
        return request, response

#    def soap_StartTreinstelScript(self, ps, **kw):
#        request, response = OtisService.soap_StartTreinstelScript(self, ps, **kw)
#        response = self.result_ok(response)
#        return request, response

    def soap_PauzeerTreinstel(self, ps, **kw):
        request, response = OtisService.soap_PauzeerTreinstel(self, ps, **kw)
        response = self.result_ok(response)
        self.logger.info( "Pauzeer Treinstel")
        message  = CommandMessage("pauzeer")
        message.treinstel = request.get_element_Treinstelnummer()
        self.repeater_socket.send_pyobj(message)
        return request, response

    def soap_HervatTreinstel(self, ps, **kw):
        request, response = OtisService.soap_HervatTreinstel(self, ps, **kw)
        response = self.result_ok(response)
        self.logger.info( "Hervat Treinstel")
        message  = CommandMessage("hervat")
        message.treinstel = request.get_element_Treinstelnummer()
        self.repeater_socket.send_pyobj(message)
        return request, response

    def soap_PlaatsTreinstel(self, ps, **kw):
        request, response = OtisService.soap_PlaatsTreinstel(self, ps, **kw)
        response = self.result_ok(response)
        self.logger.info( "Plaats Treinstel")
        message  = CommandMessage("plaats")
        message.treinstel = request.get_element_Treinstelnummer()
        message.plaats    = request.get_element_Plaats()
        self.repeater_socket.send_pyobj(message)
        return request, response

    def soap_StopGPSDekking(self, ps, **kw):
        request, response = OtisService.soap_StopGPSDekking(self, ps, **kw)
        response = self.result_ok(response)
        self.logger.info( "Stop GPS")
        message  = CommandMessage("stop_gps")
        message.treinstel = request.get_element_Treinstelnummer()
        message.gedrag    = request.get_element_GewenstGedrag()
        self.repeater_socket.send_pyobj(message)
        return request, response

    def soap_HervatGPSDekking(self, ps, **kw):
        request, response = OtisService.soap_HervatGPSDekking(self, ps, **kw)
        response = self.result_ok(response)
        self.logger.info( "Hervat GPS")
        message  = CommandMessage("hervat_gps")
        message.treinstel = request.get_element_Treinstelnummer()
        self.repeater_socket.send_pyobj(message)
        return request, response

    def soap_MaakTestcases(self, ps, **kw):
        request, response = OtisService.soap_MaakTestcases(self, ps, **kw)
        response = self.result_ok(response)
        return request, response

    def soap_MaakXMLBronBestand(self, ps, **kw):
        request, response = OtisService.soap_MaakXMLBronBestand(self, ps, **kw)
        response = self.result_ok(response)
        return request, response

