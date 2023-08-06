from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Operation:
	"""Operation commands group definition. 10 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("operation", core, parent)

	def clone(self) -> 'Operation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Operation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bit(self):
		"""bit commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_bit'):
			from .Operation_.Bit import Bit
			self._bit = Bit(self._core, self._base)
		return self._bit

	def get_condition(self) -> str:
		"""STATus:OPERation:CONDition \n
		Quieries the content of the CONDition part of the STATus:OPERation register. This part contains information on the action
		currently being performed in the instrument. The content is not deleted after being read out because it indicates the
		current hardware status. \n
			:return: condition: string
		"""
		response = self._core.io.query_str('STATus:OPERation:CONDition?')
		return trim_str_response(response)

	def get_enable(self) -> str:
		"""STATus:OPERation:ENABle \n
		Sets the bits of the ENABle part of the STATus:OPERation register. This setting determines which events of the
		Status-Event part are forwarded to the sum bit in the status byte. These events can be used for a service request. \n
			:return: enable: string
		"""
		response = self._core.io.query_str('STATus:OPERation:ENABle?')
		return trim_str_response(response)

	def set_enable(self, enable: str) -> None:
		"""STATus:OPERation:ENABle \n
		Sets the bits of the ENABle part of the STATus:OPERation register. This setting determines which events of the
		Status-Event part are forwarded to the sum bit in the status byte. These events can be used for a service request. \n
			:param enable: string
		"""
		param = Conversions.value_to_quoted_str(enable)
		self._core.io.write(f'STATus:OPERation:ENABle {param}')

	def get_ntransition(self) -> str:
		"""STATus:OPERation:NTRansition \n
		Sets the bits of the NTRansition part of the STATus:OPERation register. If a bit is set, a transition from 1 to 0 in the
		condition part causes an entry to be made in the EVENt part of the register. The disappearance of an event in the
		hardware is thus registered, for example the end of an adjustment. \n
			:return: ntransition: string
		"""
		response = self._core.io.query_str('STATus:OPERation:NTRansition?')
		return trim_str_response(response)

	def set_ntransition(self, ntransition: str) -> None:
		"""STATus:OPERation:NTRansition \n
		Sets the bits of the NTRansition part of the STATus:OPERation register. If a bit is set, a transition from 1 to 0 in the
		condition part causes an entry to be made in the EVENt part of the register. The disappearance of an event in the
		hardware is thus registered, for example the end of an adjustment. \n
			:param ntransition: string
		"""
		param = Conversions.value_to_quoted_str(ntransition)
		self._core.io.write(f'STATus:OPERation:NTRansition {param}')

	def get_ptransition(self) -> str:
		"""STATus:OPERation:PTRansition \n
		Sets the bits of the PTRansition part of the STATus:OPERation register. If a bit is set, a transition from 0 to 1 in the
		condition part causes an entry to be made in the EVENt part of the register. A new event in the hardware is thus
		registered, for example the start of an adjustment. \n
			:return: ptransition: string
		"""
		response = self._core.io.query_str('STATus:OPERation:PTRansition?')
		return trim_str_response(response)

	def set_ptransition(self, ptransition: str) -> None:
		"""STATus:OPERation:PTRansition \n
		Sets the bits of the PTRansition part of the STATus:OPERation register. If a bit is set, a transition from 0 to 1 in the
		condition part causes an entry to be made in the EVENt part of the register. A new event in the hardware is thus
		registered, for example the start of an adjustment. \n
			:param ptransition: string
		"""
		param = Conversions.value_to_quoted_str(ptransition)
		self._core.io.write(f'STATus:OPERation:PTRansition {param}')

	def get_event(self) -> str:
		"""STATus:OPERation:[EVENt] \n
		Queries the content of the EVENt part of the STATus:OPERation register. This part contains information on the actions
		performed in the instrument since the last readout. The content of the EVENt part is deleted after being read out. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:OPERation:EVENt?')
		return trim_str_response(response)

	def set_event(self, value: str) -> None:
		"""STATus:OPERation:[EVENt] \n
		Queries the content of the EVENt part of the STATus:OPERation register. This part contains information on the actions
		performed in the instrument since the last readout. The content of the EVENt part is deleted after being read out. \n
			:param value: string
		"""
		param = Conversions.value_to_quoted_str(value)
		self._core.io.write(f'STATus:OPERation:EVENt {param}')
