from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiInstrument:
	"""MultiInstrument commands group definition. 5 total commands, 2 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiInstrument", core, parent)

	def clone(self) -> 'MultiInstrument':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiInstrument(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def connector(self):
		"""connector commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_connector'):
			from .MultiInstrument_.Connector import Connector
			self._connector = Connector(self._core, self._base)
		return self._connector

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .MultiInstrument_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PriorityRole:
		"""SCONfiguration:MULTiinstrument:MODE \n
		Sets if the instrument works as master or as slave. \n
			:return: ms_mode: SLAVe| MASTer
		"""
		response = self._core.io.query_str('SCONfiguration:MULTiinstrument:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PriorityRole)

	def set_mode(self, ms_mode: enums.PriorityRole) -> None:
		"""SCONfiguration:MULTiinstrument:MODE \n
		Sets if the instrument works as master or as slave. \n
			:param ms_mode: SLAVe| MASTer
		"""
		param = Conversions.enum_scalar_to_str(ms_mode, enums.PriorityRole)
		self._core.io.write(f'SCONfiguration:MULTiinstrument:MODE {param}')

	def get_state(self) -> bool:
		"""SCONfiguration:MULTiinstrument:STATe \n
		Activates the selected mode. \n
			:return: trigger_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SCONfiguration:MULTiinstrument:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, trigger_state: bool) -> None:
		"""SCONfiguration:MULTiinstrument:STATe \n
		Activates the selected mode. \n
			:param trigger_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(trigger_state)
		self._core.io.write(f'SCONfiguration:MULTiinstrument:STATe {param}')
