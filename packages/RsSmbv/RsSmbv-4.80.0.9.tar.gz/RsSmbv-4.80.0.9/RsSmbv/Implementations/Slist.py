from typing import List

from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup
from ..Internal import Conversions
from ..Internal.RepeatedCapability import RepeatedCapability
from .. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slist:
	"""Slist commands group definition. 9 total commands, 4 Sub-groups, 2 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slist", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Slist':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Slist(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def clear(self):
		"""clear commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_clear'):
			from .Slist_.Clear import Clear
			self._clear = Clear(self._core, self._base)
		return self._clear

	@property
	def element(self):
		"""element commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_element'):
			from .Slist_.Element import Element
			self._element = Element(self._core, self._base)
		return self._element

	@property
	def scan(self):
		"""scan commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_scan'):
			from .Slist_.Scan import Scan
			self._scan = Scan(self._core, self._base)
		return self._scan

	@property
	def sensor(self):
		"""sensor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sensor'):
			from .Slist_.Sensor import Sensor
			self._sensor = Sensor(self._core, self._base)
		return self._sensor

	def clear_all(self) -> None:
		"""SLISt:CLEar:[ALL] \n
		Removes all R&S NRP power sensors from the list. \n
		"""
		self._core.io.write(f'SLISt:CLEar:ALL')

	def clear_all_with_opc(self) -> None:
		"""SLISt:CLEar:[ALL] \n
		Removes all R&S NRP power sensors from the list. \n
		Same as clear_all, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SLISt:CLEar:ALL')

	def get_list_py(self) -> List[str]:
		"""SLISt:[LIST] \n
		Returns a list of all detected sensors in a comma-separated string. \n
			:return: sensor_list: String of comma-separated entries Each entry contains information on the sensor type, serial number and interface. The order of the entries does not correspond to the order the sensors are displayed in the 'NRP Sensor Mapping' dialog.
		"""
		response = self._core.io.query_str('SLISt:LIST?')
		return Conversions.str_to_str_list(response)
