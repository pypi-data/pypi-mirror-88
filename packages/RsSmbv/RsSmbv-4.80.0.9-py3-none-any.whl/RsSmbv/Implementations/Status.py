from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from ..Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Status:
	"""Status commands group definition. 22 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("status", core, parent)

	def clone(self) -> 'Status':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Status(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def operation(self):
		"""operation commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_operation'):
			from .Status_.Operation import Operation
			self._operation = Operation(self._core, self._base)
		return self._operation

	@property
	def questionable(self):
		"""questionable commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_questionable'):
			from .Status_.Questionable import Questionable
			self._questionable = Questionable(self._core, self._base)
		return self._questionable

	@property
	def queue(self):
		"""queue commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_queue'):
			from .Status_.Queue import Queue
			self._queue = Queue(self._core, self._base)
		return self._queue

	def get_preset(self) -> str:
		"""STATus:PRESet \n
		Resets the status registers. All PTRansition parts are set to FFFFh (32767) , i.e. all transitions from 0 to 1 are
		detected. All NTRansition parts are set to 0, i.e. a transition from 1 to 0 in a CONDition bit is not detected.
		The ENABle parts of STATus:OPERation and STATus:QUEStionable are set to 0, i.e. all events in these registers are not
		passed on. \n
			:return: preset: string
		"""
		response = self._core.io.query_str('STATus:PRESet?')
		return trim_str_response(response)

	def set_preset(self, preset: str) -> None:
		"""STATus:PRESet \n
		Resets the status registers. All PTRansition parts are set to FFFFh (32767) , i.e. all transitions from 0 to 1 are
		detected. All NTRansition parts are set to 0, i.e. a transition from 1 to 0 in a CONDition bit is not detected.
		The ENABle parts of STATus:OPERation and STATus:QUEStionable are set to 0, i.e. all events in these registers are not
		passed on. \n
			:param preset: string
		"""
		param = Conversions.value_to_quoted_str(preset)
		self._core.io.write(f'STATus:PRESet {param}')
