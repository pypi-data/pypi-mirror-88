from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 9 total commands, 1 Sub-groups, 1 group commands"""

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
	def parameter(self):
		"""parameter commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_parameter'):
			from .FilterPy_.Parameter import Parameter
			self._parameter = Parameter(self._core, self._base)
		return self._parameter

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilterA:
		"""[SOURce<HW>]:BB:C2K:FILTer:TYPe \n
		The command selects the filter type. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LPASSEVM
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:FILTer:TYPe?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilterA)

	def set_type_py(self, type_py: enums.DmFilterA) -> None:
		"""[SOURce<HW>]:BB:C2K:FILTer:TYPe \n
		The command selects the filter type. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape| LPASSEVM
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilterA)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:FILTer:TYPe {param}')
