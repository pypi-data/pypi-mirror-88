from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LogGen:
	"""LogGen commands group definition. 25 total commands, 2 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("logGen", core, parent)

	def clone(self) -> 'LogGen':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LogGen(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dl(self):
		"""dl commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_dl'):
			from .LogGen_.Dl import Dl
			self._dl = Dl(self._core, self._base)
		return self._dl

	@property
	def ul(self):
		"""ul commands group. 3 Sub-classes, 9 commands."""
		if not hasattr(self, '_ul'):
			from .LogGen_.Ul import Ul
			self._ul = Ul(self._core, self._base)
		return self._ul

	def get_gs_log_file(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:GSLogfile \n
		No command help available \n
			:return: gen_sum_log: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:GSLogfile?')
		return Conversions.str_to_bool(response)

	def set_gs_log_file(self, gen_sum_log: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:GSLogfile \n
		No command help available \n
			:param gen_sum_log: No help available
		"""
		param = Conversions.bool_to_str(gen_sum_log)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:GSLogfile {param}')

	def get_lfp(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:LFP \n
		No command help available \n
			:return: preamble: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:LFP?')
		return trim_str_response(response)

	def set_lfp(self, preamble: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:LFP \n
		No command help available \n
			:param preamble: No help available
		"""
		param = Conversions.value_to_quoted_str(preamble)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:LFP {param}')

	def get_output(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:OUTPut \n
		No command help available \n
			:return: output_path: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:OUTPut?')
		return trim_str_response(response)

	def set_output(self, output_path: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:OUTPut \n
		No command help available \n
			:param output_path: No help available
		"""
		param = Conversions.value_to_quoted_str(output_path)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:OUTPut {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:STATe \n
		No command help available \n
			:return: logging_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, logging_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:STATe \n
		No command help available \n
			:param logging_state: No help available
		"""
		param = Conversions.bool_to_str(logging_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:STATe {param}')
