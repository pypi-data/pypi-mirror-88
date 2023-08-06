from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 10 total commands, 8 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bbConf(self):
		"""bbConf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bbConf'):
			from .Power_.BbConf import BbConf
			self._bbConf = BbConf(self._core, self._base)
		return self._bbConf

	@property
	def bwRef(self):
		"""bwRef commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bwRef'):
			from .Power_.BwRef import BwRef
			self._bwRef = BwRef(self._core, self._base)
		return self._bwRef

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Power_.Info import Info
			self._info = Info(self._core, self._base)
		return self._info

	@property
	def s120K(self):
		"""s120K commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_s120K'):
			from .Power_.S120K import S120K
			self._s120K = S120K(self._core, self._base)
		return self._s120K

	@property
	def s15K(self):
		"""s15K commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_s15K'):
			from .Power_.S15K import S15K
			self._s15K = S15K(self._core, self._base)
		return self._s15K

	@property
	def s240K(self):
		"""s240K commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_s240K'):
			from .Power_.S240K import S240K
			self._s240K = S240K(self._core, self._base)
		return self._s240K

	@property
	def s30K(self):
		"""s30K commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_s30K'):
			from .Power_.S30K import S30K
			self._s30K = S30K(self._core, self._base)
		return self._s30K

	@property
	def s60K(self):
		"""s60K commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_s60K'):
			from .Power_.S60K import S60K
			self._s60K = S60K(self._core, self._base)
		return self._s60K

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PowerModeAll:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:POWer:MODE \n
		Sets how the first output is leveled. \n
			:return: power_mode: AVG | ACTvsf| PSDConst AVG Average RMS power ACTvsf Average power in the active subframes PSDConst The absolute power of a particular allocation is set by multiplying the configured power spectral density (PSD) with the bandwidth of the particular allocation. Burst The 'Burst' mode is a special case of the “Constant PSD” mode in the sense that it computes automatically a reference bandwidth based on the chosen allocation.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PowerModeAll)

	def set_mode(self, power_mode: enums.PowerModeAll) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:POWer:MODE \n
		Sets how the first output is leveled. \n
			:param power_mode: AVG | ACTvsf| PSDConst AVG Average RMS power ACTvsf Average power in the active subframes PSDConst The absolute power of a particular allocation is set by multiplying the configured power spectral density (PSD) with the bandwidth of the particular allocation. Burst The 'Burst' mode is a special case of the “Constant PSD” mode in the sense that it computes automatically a reference bandwidth based on the chosen allocation.
		"""
		param = Conversions.enum_scalar_to_str(power_mode, enums.PowerModeAll)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:MODE {param}')

	def get_rsbw(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:POWer:RSBW \n
		Sets the reference bandwidth used by the leveling of the output signal at the first output. \n
			:return: ref_system_bw: float Range: 15E3 to 400E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:RSBW?')
		return Conversions.str_to_float(response)

	def set_rsbw(self, ref_system_bw: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:POWer:RSBW \n
		Sets the reference bandwidth used by the leveling of the output signal at the first output. \n
			:param ref_system_bw: float Range: 15E3 to 400E6
		"""
		param = Conversions.decimal_value_to_str(ref_system_bw)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:POWer:RSBW {param}')
