from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Selection:
	"""Selection commands group definition. 33 total commands, 10 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("selection", core, parent)

	def clone(self) -> 'Selection':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Selection(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def beidou(self):
		"""beidou commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_beidou'):
			from .Selection_.Beidou import Beidou
			self._beidou = Beidou(self._core, self._base)
		return self._beidou

	@property
	def channels(self):
		"""channels commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_channels'):
			from .Selection_.Channels import Channels
			self._channels = Channels(self._core, self._base)
		return self._channels

	@property
	def eobscuration(self):
		"""eobscuration commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_eobscuration'):
			from .Selection_.Eobscuration import Eobscuration
			self._eobscuration = Eobscuration(self._core, self._base)
		return self._eobscuration

	@property
	def galileo(self):
		"""galileo commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_galileo'):
			from .Selection_.Galileo import Galileo
			self._galileo = Galileo(self._core, self._base)
		return self._galileo

	@property
	def glonass(self):
		"""glonass commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_glonass'):
			from .Selection_.Glonass import Glonass
			self._glonass = Glonass(self._core, self._base)
		return self._glonass

	@property
	def gps(self):
		"""gps commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_gps'):
			from .Selection_.Gps import Gps
			self._gps = Gps(self._core, self._base)
		return self._gps

	@property
	def navic(self):
		"""navic commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_navic'):
			from .Selection_.Navic import Navic
			self._navic = Navic(self._core, self._base)
		return self._navic

	@property
	def qzss(self):
		"""qzss commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_qzss'):
			from .Selection_.Qzss import Qzss
			self._qzss = Qzss(self._core, self._base)
		return self._qzss

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Selection_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	@property
	def sbas(self):
		"""sbas commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_sbas'):
			from .Selection_.Sbas import Sbas
			self._sbas = Sbas(self._core, self._base)
		return self._sbas

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SelCriteria:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:MODE \n
		Sets the criteria used to define the initial satellite constellation. \n
			:return: selection_mode: MANual| ELEVation| VISibility
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SV:SELection:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SelCriteria)

	def set_mode(self, selection_mode: enums.SelCriteria) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:MODE \n
		Sets the criteria used to define the initial satellite constellation. \n
			:param selection_mode: MANual| ELEVation| VISibility
		"""
		param = Conversions.enum_scalar_to_str(selection_mode, enums.SelCriteria)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:MODE {param}')
