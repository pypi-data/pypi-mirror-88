from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Owner:
	"""Owner commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("owner", core, parent)

	def get_detailed(self) -> str:
		"""SYSTem:LOCK:OWNer:DETailed \n
		No command help available \n
			:return: details: No help available
		"""
		response = self._core.io.query_str('SYSTem:LOCK:OWNer:DETailed?')
		return trim_str_response(response)

	def get_value(self) -> str:
		"""SYSTem:LOCK:OWNer \n
		Queries the sessions that have locked the instrument currently. If an exclusive lock is set, the query returns the owner
		of this exclusive lock, otherwise it returns NONE. \n
			:return: owner: string
		"""
		response = self._core.io.query_str('SYSTem:LOCK:OWNer?')
		return trim_str_response(response)
