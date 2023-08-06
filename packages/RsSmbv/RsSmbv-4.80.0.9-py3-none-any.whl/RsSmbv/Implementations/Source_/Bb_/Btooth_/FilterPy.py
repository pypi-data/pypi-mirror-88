from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 15 total commands, 3 Sub-groups, 3 group commands"""

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
	def osampling(self):
		"""osampling commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_osampling'):
			from .FilterPy_.Osampling import Osampling
			self._osampling = Osampling(self._core, self._base)
		return self._osampling

	@property
	def parameter(self):
		"""parameter commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_parameter'):
			from .FilterPy_.Parameter import Parameter
			self._parameter = Parameter(self._core, self._base)
		return self._parameter

	def get_mindex(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:MINDex \n
		Queries the modulation index resulting from the entered frequency deviation value. \n
			:return: mi_ndex: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:MINDex?')
		return trim_str_response(response)

	def get_mtype(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:MTYPe \n
		Queries the modulation type used for the current packet selection. \n
			:return: mtype: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:MTYPe?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.DmFilterBto:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:TYPE \n
		Selects the filters used for π/4 DQPSK and 8DPSK modulations. This opens a selection window containing all the filters
		available to the instrument. \n
			:return: type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DmFilterBto)

	def set_type_py(self, type_py: enums.DmFilterBto) -> None:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:TYPE \n
		Selects the filters used for π/4 DQPSK and 8DPSK modulations. This opens a selection window containing all the filters
		available to the instrument. \n
			:param type_py: RCOSine| COSine| GAUSs| LGAuss| CONE| COF705| COEQualizer| COFequalizer| C2K3x| APCO25| SPHase| RECTangle| PGAuss| LPASs| DIRac| ENPShape| EWPShape
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.DmFilterBto)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:FILTer:TYPE {param}')
