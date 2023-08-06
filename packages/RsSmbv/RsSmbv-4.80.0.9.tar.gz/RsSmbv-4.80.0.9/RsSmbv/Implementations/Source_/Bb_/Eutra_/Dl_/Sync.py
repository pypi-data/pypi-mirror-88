from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sync:
	"""Sync commands group definition. 10 total commands, 1 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sync", core, parent)

	def clone(self) -> 'Sync':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sync(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def niot(self):
		"""niot commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_niot'):
			from .Sync_.Niot import Niot
			self._niot = Niot(self._core, self._base)
		return self._niot

	def get_ppower(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:PPOWer \n
		Sets the power of the primary synchronization signal (P-SYNC) . \n
			:return: ppower: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SYNC:PPOWer?')
		return Conversions.str_to_float(response)

	def set_ppower(self, ppower: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:PPOWer \n
		Sets the power of the primary synchronization signal (P-SYNC) . \n
			:param ppower: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(ppower)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SYNC:PPOWer {param}')

	def get_psequence(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:PSEQuence \n
		No command help available \n
			:return: psequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SYNC:PSEQuence?')
		return trim_str_response(response)

	def set_psequence(self, psequence: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:PSEQuence \n
		No command help available \n
			:param psequence: No help available
		"""
		param = Conversions.value_to_quoted_str(psequence)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SYNC:PSEQuence {param}')

	def get_pstate(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:PSTate \n
		No command help available \n
			:return: ps_ync_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SYNC:PSTate?')
		return Conversions.str_to_bool(response)

	def set_pstate(self, ps_ync_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:PSTate \n
		No command help available \n
			:param ps_ync_state: No help available
		"""
		param = Conversions.bool_to_str(ps_ync_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SYNC:PSTate {param}')

	def get_spower(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:SPOWer \n
		Sets the power of the secondary synchronization signal (S-SYNC) . \n
			:return: spower: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SYNC:SPOWer?')
		return Conversions.str_to_float(response)

	def set_spower(self, spower: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:SPOWer \n
		Sets the power of the secondary synchronization signal (S-SYNC) . \n
			:param spower: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(spower)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SYNC:SPOWer {param}')

	def get_ssequence(self) -> str:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:SSEQuence \n
		No command help available \n
			:return: ssequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SYNC:SSEQuence?')
		return trim_str_response(response)

	def set_ssequence(self, ssequence: str) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:SSEQuence \n
		No command help available \n
			:param ssequence: No help available
		"""
		param = Conversions.value_to_quoted_str(ssequence)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SYNC:SSEQuence {param}')

	def get_sstate(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:SSTate \n
		No command help available \n
			:return: ss_ync_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SYNC:SSTate?')
		return Conversions.str_to_bool(response)

	def set_sstate(self, ss_ync_state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:SSTate \n
		No command help available \n
			:param ss_ync_state: No help available
		"""
		param = Conversions.bool_to_str(ss_ync_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SYNC:SSTate {param}')

	# noinspection PyTypeChecker
	def get_tx_antenna(self) -> enums.TxAntennaGnss:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:TXANtenna \n
		Defines on which antenna port the P-/S-SYNC is transmitted. The available values depend on the number of configured
		antennas. \n
			:return: tx_antenna: NONE| ANT1| ANT2| ANT3| ANT4| ALL
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SYNC:TXANtenna?')
		return Conversions.str_to_scalar_enum(response, enums.TxAntennaGnss)

	def set_tx_antenna(self, tx_antenna: enums.TxAntennaGnss) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SYNC:TXANtenna \n
		Defines on which antenna port the P-/S-SYNC is transmitted. The available values depend on the number of configured
		antennas. \n
			:param tx_antenna: NONE| ANT1| ANT2| ANT3| ANT4| ALL
		"""
		param = Conversions.enum_scalar_to_str(tx_antenna, enums.TxAntennaGnss)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SYNC:TXANtenna {param}')
