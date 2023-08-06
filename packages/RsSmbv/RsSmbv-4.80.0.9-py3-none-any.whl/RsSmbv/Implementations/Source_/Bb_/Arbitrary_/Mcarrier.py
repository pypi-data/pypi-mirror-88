from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcarrier:
	"""Mcarrier commands group definition. 37 total commands, 9 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcarrier", core, parent)

	def clone(self) -> 'Mcarrier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mcarrier(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def carrier(self):
		"""carrier commands group. 7 Sub-classes, 3 commands."""
		if not hasattr(self, '_carrier'):
			from .Mcarrier_.Carrier import Carrier
			self._carrier = Carrier(self._core, self._base)
		return self._carrier

	@property
	def cfactor(self):
		"""cfactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfactor'):
			from .Mcarrier_.Cfactor import Cfactor
			self._cfactor = Cfactor(self._core, self._base)
		return self._cfactor

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Mcarrier_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def cload(self):
		"""cload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cload'):
			from .Mcarrier_.Cload import Cload
			self._cload = Cload(self._core, self._base)
		return self._cload

	@property
	def create(self):
		"""create commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_create'):
			from .Mcarrier_.Create import Create
			self._create = Create(self._core, self._base)
		return self._create

	@property
	def edit(self):
		"""edit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_edit'):
			from .Mcarrier_.Edit import Edit
			self._edit = Edit(self._core, self._base)
		return self._edit

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Mcarrier_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Mcarrier_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_time'):
			from .Mcarrier_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time

	def get_clock(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CLOCk \n
		Queries the resulting sample rate at which the multi-carrier waveform is output by the arbitrary waveform generator. The
		output clock rate depends on the number of carriers, carrier spacing, and input sample rate of the leftmost or rightmost
		carriers. \n
			:return: clock: float Range: 400 to Max
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:CLOCk?')
		return Conversions.str_to_float(response)

	def get_ofile(self) -> str:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:OFILe \n
		Defines the output file name for the multi-carrier waveform (file extension *.wv) . This file name is required to
		calculate the waveform with the commands method RsSmbv.Source.Bb.Arbitrary.Mcarrier.Cload.set or method RsSmbv.Source.Bb.
		Arbitrary.Mcarrier.Create.set. \n
			:return: ofile: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:OFILe?')
		return trim_str_response(response)

	def set_ofile(self, ofile: str) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:OFILe \n
		Defines the output file name for the multi-carrier waveform (file extension *.wv) . This file name is required to
		calculate the waveform with the commands method RsSmbv.Source.Bb.Arbitrary.Mcarrier.Cload.set or method RsSmbv.Source.Bb.
		Arbitrary.Mcarrier.Create.set. \n
			:param ofile: string
		"""
		param = Conversions.value_to_quoted_str(ofile)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:OFILe {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:PRESet \n
		Sets all the multi-carrier parameters to their default values. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:PRESet \n
		Sets all the multi-carrier parameters to their default values. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:PRESet')

	def get_samples(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:SAMPles \n
		Queries the resulting file size. \n
			:return: samples: integer Range: 0 to INT_MAX, Unit: samples
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:MCARrier:SAMPles?')
		return Conversions.str_to_int(response)
