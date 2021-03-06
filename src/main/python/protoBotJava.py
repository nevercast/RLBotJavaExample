import os

from py4j.java_gateway import GatewayParameters
from py4j.java_gateway import JavaGateway

from RLBotFramework.agents.base_independent_agent import BaseIndependentAgent
from RLBotFramework.utils.logging_utils import get_logger


class ProtoJava(BaseIndependentAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.gateway = None
        self.javaAgent = None
        self.logger = get_logger('protoBotJava' + str(self.index))
        self.port = self.read_port_from_file()

    def read_port_from_file(self):
        try:
            # Look for a port.cfg file in the same directory as THIS python file.
            location = os.path.realpath(
                os.path.join(os.getcwd(), os.path.dirname(__file__)))

            with open(os.path.join(location, "port.cfg"), "r") as portFile:
                return int(portFile.readline().rstrip())

        except ValueError:
            self.logger.warn("Failed to parse port file!")
            raise

    def run_independently(self):
        self.init_py4j_stuff()
        self.javaAgent.registerBot(self.index, self.name)
        self.javaAgent.startup()
        print()

    def get_extra_pids(self):
        """
        Gets the list of process ids that should be marked as high priority.
        :return: A list of process ids that are used by this bot in addition to the ones inside the python process.
        """
        return []

    def retire(self):
        self.javaAgent.shutdown()

    def init_py4j_stuff(self):
        self.logger.info("Connecting to Java Gateway on port " + str(self.port))
        self.gateway = JavaGateway(gateway_parameters=GatewayParameters(auto_convert=True, port=self.port))
        self.javaAgent = self.gateway.entry_point
        self.logger.info("Connection to Java successful!")
