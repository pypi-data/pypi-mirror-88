from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pow:
	"""Pow commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pow", core, parent)

	def set(self, power: float, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Nr1, group=repcap.Group.Default, userItem=repcap.UserItem.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:[CELL<CCIDX>]:GROup<GR>:ITEM<USER>:POW \n
		Sets the power of the individual PHICHs. \n
			:param power: float Range: -80 to 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param group: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param userItem: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.decimal_value_to_str(power)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		group_cmd_val = self._base.get_repcap_cmd_value(group, repcap.Group)
		userItem_cmd_val = self._base.get_repcap_cmd_value(userItem, repcap.UserItem)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:CELL{carrierComponent_cmd_val}:GROup{group_cmd_val}:ITEM{userItem_cmd_val}:POW {param}')

	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Nr1, group=repcap.Group.Default, userItem=repcap.UserItem.Default) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:[CELL<CCIDX>]:GROup<GR>:ITEM<USER>:POW \n
		Sets the power of the individual PHICHs. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1
			:param group: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Group')
			:param userItem: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: power: float Range: -80 to 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		group_cmd_val = self._base.get_repcap_cmd_value(group, repcap.Group)
		userItem_cmd_val = self._base.get_repcap_cmd_value(userItem, repcap.UserItem)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:CELL{carrierComponent_cmd_val}:GROup{group_cmd_val}:ITEM{userItem_cmd_val}:POW?')
		return Conversions.str_to_float(response)
