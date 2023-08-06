from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gain:
	"""Gain commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gain", core, parent)

	def get_post(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:GAIN:POST \n
		Sets a post-gain. \n
			:return: post_gain: float Range: -3 to 20
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:GAIN:POST?')
		return Conversions.str_to_float(response)

	def set_post(self, post_gain: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:GAIN:POST \n
		Sets a post-gain. \n
			:param post_gain: float Range: -3 to 20
		"""
		param = Conversions.decimal_value_to_str(post_gain)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:GAIN:POST {param}')

	def get_pre(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:GAIN:PRE \n
		Sets a post-gain. \n
			:return: pre_gain: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:GAIN:PRE?')
		return Conversions.str_to_float(response)

	def set_pre(self, pre_gain: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:GAIN:PRE \n
		Sets a post-gain. \n
			:param pre_gain: float Range: -3 to 20
		"""
		param = Conversions.decimal_value_to_str(pre_gain)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:GAIN:PRE {param}')
