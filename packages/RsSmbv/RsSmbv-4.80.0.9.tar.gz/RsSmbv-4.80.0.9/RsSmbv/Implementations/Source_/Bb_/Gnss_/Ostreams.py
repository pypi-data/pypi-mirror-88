from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ostreams:
	"""Ostreams commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ostreams", core, parent)

	def clone(self) -> 'Ostreams':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ostreams(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def output(self):
		"""output commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_output'):
			from .Ostreams_.Output import Output
			self._output = Output(self._core, self._base)
		return self._output

	def get_conflict(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:OSTReams:CONFlict \n
		No command help available \n
			:return: conflict_status: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:OSTReams:CONFlict?')
		return Conversions.str_to_bool(response)

	# noinspection PyTypeChecker
	def get_count(self) -> enums.NumberA:
		"""[SOURce<HW>]:BB:GNSS:OSTReams:COUNt \n
		No command help available \n
			:return: output_streams: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:OSTReams:COUNt?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)

	def set_count(self, output_streams: enums.NumberA) -> None:
		"""[SOURce<HW>]:BB:GNSS:OSTReams:COUNt \n
		No command help available \n
			:param output_streams: No help available
		"""
		param = Conversions.enum_scalar_to_str(output_streams, enums.NumberA)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:OSTReams:COUNt {param}')

	def get_lock(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:OSTReams:LOCK \n
		No command help available \n
			:return: lock_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:OSTReams:LOCK?')
		return Conversions.str_to_bool(response)

	def set_lock(self, lock_state: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:OSTReams:LOCK \n
		No command help available \n
			:param lock_state: No help available
		"""
		param = Conversions.bool_to_str(lock_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:OSTReams:LOCK {param}')
