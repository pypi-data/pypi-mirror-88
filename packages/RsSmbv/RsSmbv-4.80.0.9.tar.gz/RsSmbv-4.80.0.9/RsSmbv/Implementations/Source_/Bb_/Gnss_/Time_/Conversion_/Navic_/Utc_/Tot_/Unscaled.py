from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Unscaled:
	"""Unscaled commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("unscaled", core, parent)

	def set(self, tot: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:NAVic<ST>:UTC:TOT:UNSCaled \n
		Sets the UTC data reference time of week, tot. \n
			:param tot: integer Range: 0 to 255
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.decimal_value_to_str(tot)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:NAVic{stream_cmd_val}:UTC:TOT:UNSCaled {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:TIME:CONVersion:NAVic<ST>:UTC:TOT:UNSCaled \n
		Sets the UTC data reference time of week, tot. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: tot: integer Range: 0 to 255"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:TIME:CONVersion:NAVic{stream_cmd_val}:UTC:TOT:UNSCaled?')
		return Conversions.str_to_int(response)
