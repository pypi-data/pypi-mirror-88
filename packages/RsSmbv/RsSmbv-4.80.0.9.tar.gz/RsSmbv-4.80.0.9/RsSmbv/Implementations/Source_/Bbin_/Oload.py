from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Oload:
	"""Oload commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("oload", core, parent)

	def clone(self) -> 'Oload':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Oload(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def hold(self):
		"""hold commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_hold'):
			from .Oload_.Hold import Hold
			self._hold = Hold(self._core, self._base)
		return self._hold

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BBIN:OLOad:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BBIN:OLOad:STATe?')
		return Conversions.str_to_bool(response)
