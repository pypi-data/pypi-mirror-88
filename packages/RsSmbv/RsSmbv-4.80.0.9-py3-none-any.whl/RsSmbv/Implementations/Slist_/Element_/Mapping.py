from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mapping:
	"""Mapping commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mapping", core, parent)

	def set(self, mapping: enums.ErFpowSensMapping, channel=repcap.Channel.Default) -> None:
		"""SLISt:ELEMent<CH>:MAPPing \n
		Assigns an entry from the :​SLISt[:​LIST]? to one of the four sensor channels. \n
			:param mapping: SENS1| SENSor1| SENS2| SENSor2| SENS3| SENSor3| SENS4| SENSor4| UNMapped Sensor channel.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slist')"""
		param = Conversions.enum_scalar_to_str(mapping, enums.ErFpowSensMapping)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SLISt:ELEMent{channel_cmd_val}:MAPPing {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.ErFpowSensMapping:
		"""SLISt:ELEMent<CH>:MAPPing \n
		Assigns an entry from the :​SLISt[:​LIST]? to one of the four sensor channels. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Slist')
			:return: mapping: SENS1| SENSor1| SENS2| SENSor2| SENS3| SENSor3| SENS4| SENSor4| UNMapped Sensor channel."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SLISt:ELEMent{channel_cmd_val}:MAPPing?')
		return Conversions.str_to_scalar_enum(response, enums.ErFpowSensMapping)
