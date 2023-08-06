from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uradius:
	"""Uradius commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uradius", core, parent)

	def set(self, radius: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:LOCation:URADius \n
		Sets the Uncertainty Radius, i.e. sets the maximum radius of the area within which the two-dimensional location of the UE
		is bounded. \n
			:param radius: integer Range: 0 to 1.E6
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')"""
		param = Conversions.decimal_value_to_str(radius)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:LOCation:URADius {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:ADGeneration:GALileo<ST>:LOCation:URADius \n
		Sets the Uncertainty Radius, i.e. sets the maximum radius of the area within which the two-dimensional location of the UE
		is bounded. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Galileo')
			:return: radius: integer Range: 0 to 1.E6"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:ADGeneration:GALileo{stream_cmd_val}:LOCation:URADius?')
		return Conversions.str_to_int(response)
