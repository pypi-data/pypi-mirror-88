from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ul:
	"""Ul commands group definition. 12 total commands, 3 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ul", core, parent)

	def clone(self) -> 'Ul':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ul(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dall(self):
		"""dall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dall'):
			from .Ul_.Dall import Dall
			self._dall = Dall(self._core, self._base)
		return self._dall

	@property
	def eall(self):
		"""eall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eall'):
			from .Ul_.Eall import Eall
			self._eall = Eall(self._core, self._base)
		return self._eall

	@property
	def logPoint(self):
		"""logPoint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logPoint'):
			from .Ul_.LogPoint import LogPoint
			self._logPoint = LogPoint(self._core, self._base)
		return self._logPoint

	def get_eu_logging(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:EULogging \n
		No command help available \n
			:return: ext_uci_log: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:EULogging?')
		return Conversions.str_to_bool(response)

	def set_eu_logging(self, ext_uci_log: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:EULogging \n
		No command help available \n
			:param ext_uci_log: No help available
		"""
		param = Conversions.bool_to_str(ext_uci_log)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:EULogging {param}')

	def get_prach(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PRACh \n
		No command help available \n
			:return: prach_log_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PRACh?')
		return Conversions.str_to_bool(response)

	def set_prach(self, prach_log_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PRACh \n
		No command help available \n
			:param prach_log_state: No help available
		"""
		param = Conversions.bool_to_str(prach_log_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PRACh {param}')

	def get_pucch(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUCCh \n
		No command help available \n
			:return: pucch_log_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUCCh?')
		return Conversions.str_to_bool(response)

	def set_pucch(self, pucch_log_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUCCh \n
		No command help available \n
			:param pucch_log_state: No help available
		"""
		param = Conversions.bool_to_str(pucch_log_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUCCh {param}')

	def get_pucdrs(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUCDrs \n
		No command help available \n
			:return: pusch_drs_log: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUCDrs?')
		return Conversions.str_to_bool(response)

	def set_pucdrs(self, pusch_drs_log: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUCDrs \n
		No command help available \n
			:param pusch_drs_log: No help available
		"""
		param = Conversions.bool_to_str(pusch_drs_log)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUCDrs {param}')

	def get_pusch(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUSCh \n
		No command help available \n
			:return: pusch_log_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUSCh?')
		return Conversions.str_to_bool(response)

	def set_pusch(self, pusch_log_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUSCh \n
		No command help available \n
			:param pusch_log_state: No help available
		"""
		param = Conversions.bool_to_str(pusch_log_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUSCh {param}')

	def get_pusdrs(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUSDrs \n
		No command help available \n
			:return: pusch_drs_log: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUSDrs?')
		return Conversions.str_to_bool(response)

	def set_pusdrs(self, pusch_drs_log: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:PUSDrs \n
		No command help available \n
			:param pusch_drs_log: No help available
		"""
		param = Conversions.bool_to_str(pusch_drs_log)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:PUSDrs {param}')

	def get_sl(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:SL \n
		No command help available \n
			:return: log_sidelink: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:SL?')
		return Conversions.str_to_bool(response)

	def set_sl(self, log_sidelink: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:SL \n
		No command help available \n
			:param log_sidelink: No help available
		"""
		param = Conversions.bool_to_str(log_sidelink)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:SL {param}')

	def get_sld(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:SLD \n
		No command help available \n
			:return: log_sidelink_drs: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:SLD?')
		return Conversions.str_to_bool(response)

	def set_sld(self, log_sidelink_drs: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:SLD \n
		No command help available \n
			:param log_sidelink_drs: No help available
		"""
		param = Conversions.bool_to_str(log_sidelink_drs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:SLD {param}')

	def get_srs(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:SRS \n
		No command help available \n
			:return: srs_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:SRS?')
		return Conversions.str_to_bool(response)

	def set_srs(self, srs_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LOGGen:UL:SRS \n
		No command help available \n
			:param srs_state: No help available
		"""
		param = Conversions.bool_to_str(srs_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LOGGen:UL:SRS {param}')
