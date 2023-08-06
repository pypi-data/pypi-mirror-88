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

	def set(self, prs_numerology: enums.NumerologyPrs, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:SCSPacing \n
		Sets the combination of the subcarrier spacing (SCS) and the cyclic prefix (CP) for the DL PRS frequency layer. Set the
		value according to the configured 'Deployment'. \n
			:param prs_numerology: N15| N30| N60| N120| X60 N15 Sets the SCS to 15 kHz and the CP to normal. N30 Sets the SCS to 30 kHz and the CP to normal. N60 Sets the SCS to 60 kHz and the CP to normal. N120 Sets the SCS to 120 kHz and the CP to normal. X60 Sets the SCS to 60 kHz and the CP to extended.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(prs_numerology, enums.NumerologyPrs)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:SCSPacing {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NumerologyPrs:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:SCSPacing \n
		Sets the combination of the subcarrier spacing (SCS) and the cyclic prefix (CP) for the DL PRS frequency layer. Set the
		value according to the configured 'Deployment'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: prs_numerology: N15| N30| N60| N120| X60 N15 Sets the SCS to 15 kHz and the CP to normal. N30 Sets the SCS to 30 kHz and the CP to normal. N60 Sets the SCS to 60 kHz and the CP to normal. N120 Sets the SCS to 120 kHz and the CP to normal. X60 Sets the SCS to 60 kHz and the CP to extended."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.NumerologyPrs)
