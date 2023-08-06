from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Invert:
	"""Invert commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("invert", core, parent)

	def set(self, ipartnvert_values: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:[TABLe]:INVert \n
		Inverts the defined correction values. \n
			:param ipartnvert_values: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.bool_to_str(ipartnvert_values)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:TABLe:INVert {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:IQ:DPD<ST>:SHAPing:[TABLe]:INVert \n
		Inverts the defined correction values. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: ipartnvert_values: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:SHAPing:TABLe:INVert?')
		return Conversions.str_to_bool(response)
