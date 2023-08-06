from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Request:
	"""Request commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("request", core, parent)

	def clone(self) -> 'Request':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Request(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def shared(self):
		"""shared commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_shared'):
			from .Request_.Shared import Shared
			self._shared = Shared(self._core, self._base)
		return self._shared

	def get_exclusive(self) -> int:
		"""SYSTem:LOCK:REQuest:[EXCLusive] \n
		Queries whether a lock for exclusive access to the instrument via ethernet exists. If successful, the query returns a 1,
		otherwise 0. \n
			:return: success: integer
		"""
		response = self._core.io.query_str('SYSTem:LOCK:REQuest:EXCLusive?')
		return Conversions.str_to_int(response)
