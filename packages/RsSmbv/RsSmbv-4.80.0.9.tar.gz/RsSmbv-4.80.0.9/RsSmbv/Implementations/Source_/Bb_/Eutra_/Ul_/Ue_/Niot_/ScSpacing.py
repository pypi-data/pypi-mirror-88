from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScSpacing:
	"""ScSpacing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scSpacing", core, parent)

	def set(self, subcarr_spacing: enums.EutraSubCarrierSpacing, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:SCSPacing \n
		Sets the subcarrier spacing. \n
			:param subcarr_spacing: S15| S375
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(subcarr_spacing, enums.EutraSubCarrierSpacing)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:SCSPacing {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraSubCarrierSpacing:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:NIOT:SCSPacing \n
		Sets the subcarrier spacing. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: subcarr_spacing: S15| S375"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:NIOT:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSubCarrierSpacing)
