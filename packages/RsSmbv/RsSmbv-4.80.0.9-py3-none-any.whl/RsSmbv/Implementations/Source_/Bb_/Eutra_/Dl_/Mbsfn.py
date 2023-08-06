from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mbsfn:
	"""Mbsfn commands group definition. 37 total commands, 4 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mbsfn", core, parent)

	def clone(self) -> 'Mbsfn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mbsfn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ai(self):
		"""ai commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_ai'):
			from .Mbsfn_.Ai import Ai
			self._ai = Ai(self._core, self._base)
		return self._ai

	@property
	def mtch(self):
		"""mtch commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mtch'):
			from .Mbsfn_.Mtch import Mtch
			self._mtch = Mtch(self._core, self._base)
		return self._mtch

	@property
	def pmch(self):
		"""pmch commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_pmch'):
			from .Mbsfn_.Pmch import Pmch
			self._pmch = Pmch(self._core, self._base)
		return self._pmch

	@property
	def sc(self):
		"""sc commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_sc'):
			from .Mbsfn_.Sc import Sc
			self._sc = Sc(self._core, self._base)
		return self._sc

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EutraMbsfnType:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:MODE \n
		Enables the MBSFN transmission and selects a mixed MBSFN Mode. \n
			:return: mbsfn_mode: OFF| MIXed
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMbsfnType)

	def set_mode(self, mbsfn_mode: enums.EutraMbsfnType) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:MODE \n
		Enables the MBSFN transmission and selects a mixed MBSFN Mode. \n
			:param mbsfn_mode: OFF| MIXed
		"""
		param = Conversions.enum_scalar_to_str(mbsfn_mode, enums.EutraMbsfnType)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:MODE {param}')

	def get_rhoa(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:RHOA \n
		Defines the power of the MBSFN channels relative to the common Reference Signals. \n
			:return: rho_a: float Range: -80 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:RHOA?')
		return Conversions.str_to_float(response)

	def set_rhoa(self, rho_a: float) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:RHOA \n
		Defines the power of the MBSFN channels relative to the common Reference Signals. \n
			:param rho_a: float Range: -80 to 10
		"""
		param = Conversions.decimal_value_to_str(rho_a)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:RHOA {param}')

	# noinspection PyTypeChecker
	def get_uec(self) -> enums.EutraMbsfnUeCat:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:UEC \n
		Defines the UE category as defined in . \n
			:return: ue_category: C1| C2| C3| C4| C5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:UEC?')
		return Conversions.str_to_scalar_enum(response, enums.EutraMbsfnUeCat)

	def set_uec(self, ue_category: enums.EutraMbsfnUeCat) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:UEC \n
		Defines the UE category as defined in . \n
			:param ue_category: C1| C2| C3| C4| C5
		"""
		param = Conversions.enum_scalar_to_str(ue_category, enums.EutraMbsfnUeCat)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:UEC {param}')
