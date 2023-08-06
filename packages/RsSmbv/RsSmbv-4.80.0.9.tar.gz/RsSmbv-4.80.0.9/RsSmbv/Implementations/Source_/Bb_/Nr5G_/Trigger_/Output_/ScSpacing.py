from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScSpacing:
	"""ScSpacing commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scSpacing", core, parent)

	def set(self, scs: enums.EidNr5GscsGeneral, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SCSPacing \n
		Defines the subcarrier spacing (SCS) value for a UL/DL pattern containing a marker. The available values depend on the
		set 'Deployment' value. \n
			:param scs: SCS15| SCS30| SCS60| SCS120| SCS240
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(scs, enums.EidNr5GscsGeneral)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:SCSPacing {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EidNr5GscsGeneral:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SCSPacing \n
		Defines the subcarrier spacing (SCS) value for a UL/DL pattern containing a marker. The available values depend on the
		set 'Deployment' value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: scs: SCS15| SCS30| SCS60| SCS120| SCS240"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:SCSPacing?')
		return Conversions.str_to_scalar_enum(response, enums.EidNr5GscsGeneral)
