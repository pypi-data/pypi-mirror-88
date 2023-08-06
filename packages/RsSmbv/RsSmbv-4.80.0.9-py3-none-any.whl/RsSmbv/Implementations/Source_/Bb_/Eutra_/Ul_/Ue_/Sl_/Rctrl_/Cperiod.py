from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cperiod:
	"""Cperiod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cperiod", core, parent)

	def set(self, control_period: enums.EutraSlCommControlPeriod, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RCTRl:CPERiod \n
		Sets the period over which resources are allocated for sidelink control period (SC period) . \n
			:param control_period: 40| 60| 70| 80| 120| 140| 160| 240| 280| 320
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(control_period, enums.EutraSlCommControlPeriod)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:RCTRl:CPERiod {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraSlCommControlPeriod:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:SL:RCTRl:CPERiod \n
		Sets the period over which resources are allocated for sidelink control period (SC period) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: control_period: 40| 60| 70| 80| 120| 140| 160| 240| 280| 320"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:SL:RCTRl:CPERiod?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSlCommControlPeriod)
