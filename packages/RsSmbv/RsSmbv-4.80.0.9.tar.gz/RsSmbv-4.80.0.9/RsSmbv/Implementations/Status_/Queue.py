from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Queue:
	"""Queue commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("queue", core, parent)

	def get_next(self) -> str:
		"""STATus:QUEue:[NEXT] \n
		Queries the oldest entry in the error queue and then deletes it. Positive error numbers denote device-specific errors,
		and negative error numbers denote error messages defined by SCPI. If the error queue is empty, 0 ('No error') is returned.
		The command is identical to SYSTem. \n
			:return: next_py: string
		"""
		response = self._core.io.query_str('STATus:QUEue:NEXT?')
		return trim_str_response(response)
