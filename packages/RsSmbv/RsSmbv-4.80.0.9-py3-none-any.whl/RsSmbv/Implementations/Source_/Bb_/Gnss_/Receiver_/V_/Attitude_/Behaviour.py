from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Behaviour:
	"""Behaviour commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("behaviour", core, parent)

	def set(self, atitude_behaviou: enums.AttitMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ATTitude:[BEHaviour] \n
		Defines how the attitude information is defined. \n
			:param atitude_behaviou: CONStant| FILE| MOTion| SPINning| REMote FILE enabled if smoothing is not used.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(atitude_behaviou, enums.AttitMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ATTitude:BEHaviour {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.AttitMode:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ATTitude:[BEHaviour] \n
		Defines how the attitude information is defined. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: atitude_behaviou: CONStant| FILE| MOTion| SPINning| REMote FILE enabled if smoothing is not used."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ATTitude:BEHaviour?')
		return Conversions.str_to_scalar_enum(response, enums.AttitMode)
