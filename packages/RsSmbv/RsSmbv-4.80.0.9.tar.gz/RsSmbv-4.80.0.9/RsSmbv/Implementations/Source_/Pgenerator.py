from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pgenerator:
	"""Pgenerator commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pgenerator", core, parent)

	def clone(self) -> 'Pgenerator':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pgenerator(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_output'):
			from .Pgenerator_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	def get_state(self) -> bool:
		"""[SOURce<HW>]:PGENerator:STATe \n
		Enables the output of the video/sync signal. If the pulse generator is the current modulation source, activating the
		pulse modulation automatically activates the signal output and the pulse generator. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:PGENerator:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:PGENerator:STATe \n
		Enables the output of the video/sync signal. If the pulse generator is the current modulation source, activating the
		pulse modulation automatically activates the signal output and the pulse generator. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:PGENerator:STATe {param}')
