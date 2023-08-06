from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vpp:
	"""Vpp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vpp", core, parent)

	def get_max(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VPP:[MAX] \n
		Set the maximum value of the driving voltage Vpp of the used external DC modulator. \n
			:return: vpp_max: float Range: -0.02V to 8V , Unit: V
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VPP:MAX?')
		return Conversions.str_to_float(response)

	def set_max(self, vpp_max: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:VPP:[MAX] \n
		Set the maximum value of the driving voltage Vpp of the used external DC modulator. \n
			:param vpp_max: float Range: -0.02V to 8V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(vpp_max)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:VPP:MAX {param}')
