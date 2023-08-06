from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 13 total commands, 3 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ilength(self):
		"""ilength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ilength'):
			from .FilterPy_.Ilength import Ilength
			self._ilength = Ilength(self._core, self._base)
		return self._ilength

	@property
	def osamplinng(self):
		"""osamplinng commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_osamplinng'):
			from .FilterPy_.Osamplinng import Osamplinng
			self._osamplinng = Osamplinng(self._core, self._base)
		return self._osamplinng

	@property
	def parameter(self):
		"""parameter commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_parameter'):
			from .FilterPy_.Parameter import Parameter
			self._parameter = Parameter(self._core, self._base)
		return self._parameter

	def get_osampling(self) -> int:
		"""[SOURce<HW>]:BB:EVDO:FILTer:OSAMpling \n
		No command help available \n
			:return: osampling: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:OSAMpling?')
		return Conversions.str_to_int(response)

	def set_osampling(self, osampling: int) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:OSAMpling \n
		No command help available \n
			:param osampling: No help available
		"""
		param = Conversions.decimal_value_to_str(osampling)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:OSAMpling {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilterA:
		"""[SOURce<HW>]:BB:EVDO:FILTer:TYPE \n
		The command selects the filter type. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LPASSEVM
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilterA)

	def set_type_py(self, type_py: enums.DmFilterA) -> None:
		"""[SOURce<HW>]:BB:EVDO:FILTer:TYPE \n
		The command selects the filter type. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LPASSEVM
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilterA)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:FILTer:TYPE {param}')
