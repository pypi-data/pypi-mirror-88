from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Emtc:
	"""Emtc commands group definition. 105 total commands, 5 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("emtc", core, parent)

	def clone(self) -> 'Emtc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Emtc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def alloc(self):
		"""alloc commands group. 19 Sub-classes, 0 commands."""
		if not hasattr(self, '_alloc'):
			from .Emtc_.Alloc import Alloc
			self._alloc = Alloc(self._core, self._base)
		return self._alloc

	@property
	def bmp(self):
		"""bmp commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_bmp'):
			from .Emtc_.Bmp import Bmp
			self._bmp = Bmp(self._core, self._base)
		return self._bmp

	@property
	def dci(self):
		"""dci commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_dci'):
			from .Emtc_.Dci import Dci
			self._dci = Dci(self._core, self._base)
		return self._dci

	@property
	def nb(self):
		"""nb commands group. 0 Sub-classes, 9 commands."""
		if not hasattr(self, '_nb'):
			from .Emtc_.Nb import Nb
			self._nb = Nb(self._core, self._base)
		return self._nb

	@property
	def ssp(self):
		"""ssp commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_ssp'):
			from .Emtc_.Ssp import Ssp
			self._ssp = Ssp(self._core, self._base)
		return self._ssp

	def get_nalloc(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NALLoc \n
		Queries the number of automatically configured allocations. \n
			:return: no_alloc: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NALLoc?')
		return Conversions.str_to_int(response)

	def get_nn_bands(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NNBands \n
		No command help available \n
			:return: num_narrowbands: integer Range: 0 to 18
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NNBands?')
		return Conversions.str_to_int(response)

	def get_nw_bands(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:NWBands \n
		Queries the number of widebands. \n
			:return: num_wide_bands: integer Range: 0 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:NWBands?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_wbcfg(self) -> enums.EutraEmtcPdschWideBand:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:WBCFg \n
		If enabled, the available channel bandwidth is split into eMTC widebands with the selected bandwidth. \n
			:return: wide_band_cfg: OFF| BW5_00| BW20_00
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:EMTC:WBCFg?')
		return Conversions.str_to_scalar_enum(response, enums.EutraEmtcPdschWideBand)

	def set_wbcfg(self, wide_band_cfg: enums.EutraEmtcPdschWideBand) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:EMTC:WBCFg \n
		If enabled, the available channel bandwidth is split into eMTC widebands with the selected bandwidth. \n
			:param wide_band_cfg: OFF| BW5_00| BW20_00
		"""
		param = Conversions.enum_scalar_to_str(wide_band_cfg, enums.EutraEmtcPdschWideBand)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:EMTC:WBCFg {param}')
