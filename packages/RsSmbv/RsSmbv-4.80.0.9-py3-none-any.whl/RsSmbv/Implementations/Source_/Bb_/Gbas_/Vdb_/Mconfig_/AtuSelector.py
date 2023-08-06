from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AtuSelector:
	"""AtuSelector commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("atuSelector", core, parent)

	def set(self, tch_unit: enums.GbasAppTchUnitSel, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:ATUSelector \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the units for the approach TCH, see method RsSmbv.Source.Bb.Gbas.
		Vdb.Mconfig.AtcHeight.set. \n
			:param tch_unit: FEET| MET
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		param = Conversions.enum_scalar_to_str(tch_unit, enums.GbasAppTchUnitSel)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:ATUSelector {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.GbasAppTchUnitSel:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:MCONfig:ATUSelector \n
		Requires 'Mode > GBAS' (LAAS) header information. Sets the units for the approach TCH, see method RsSmbv.Source.Bb.Gbas.
		Vdb.Mconfig.AtcHeight.set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')
			:return: tch_unit: FEET| MET"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:MCONfig:ATUSelector?')
		return Conversions.str_to_scalar_enum(response, enums.GbasAppTchUnitSel)
