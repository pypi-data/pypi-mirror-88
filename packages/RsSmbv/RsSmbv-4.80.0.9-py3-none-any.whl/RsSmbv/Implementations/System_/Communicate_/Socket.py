from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Socket:
	"""Socket commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("socket", core, parent)

	def get_resource(self) -> str:
		"""SYSTem:COMMunicate:SOCKet:RESource \n
		Queries the visa resource string for remote control via LAN interface, using TCP/IP socket protocol. \n
			:return: resource: string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:RESource?')
		return trim_str_response(response)
