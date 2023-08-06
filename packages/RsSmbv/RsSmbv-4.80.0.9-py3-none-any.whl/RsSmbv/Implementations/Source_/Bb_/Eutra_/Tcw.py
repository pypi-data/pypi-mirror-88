from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tcw:
	"""Tcw commands group definition. 91 total commands, 11 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tcw", core, parent)

	def clone(self) -> 'Tcw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tcw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def applySettings(self):
		"""applySettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_applySettings'):
			from .Tcw_.ApplySettings import ApplySettings
			self._applySettings = ApplySettings(self._core, self._base)
		return self._applySettings

	@property
	def awgn(self):
		"""awgn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_awgn'):
			from .Tcw_.Awgn import Awgn
			self._awgn = Awgn(self._core, self._base)
		return self._awgn

	@property
	def fa(self):
		"""fa commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fa'):
			from .Tcw_.Fa import Fa
			self._fa = Fa(self._core, self._base)
		return self._fa

	@property
	def gs(self):
		"""gs commands group. 0 Sub-classes, 14 commands."""
		if not hasattr(self, '_gs'):
			from .Tcw_.Gs import Gs
			self._gs = Gs(self._core, self._base)
		return self._gs

	@property
	def is2(self):
		"""is2 commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_is2'):
			from .Tcw_.Is2 import Is2
			self._is2 = Is2(self._core, self._base)
		return self._is2

	@property
	def is3(self):
		"""is3 commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_is3'):
			from .Tcw_.Is3 import Is3
			self._is3 = Is3(self._core, self._base)
		return self._is3

	@property
	def isPy(self):
		"""isPy commands group. 0 Sub-classes, 19 commands."""
		if not hasattr(self, '_isPy'):
			from .Tcw_.IsPy import IsPy
			self._isPy = IsPy(self._core, self._base)
		return self._isPy

	@property
	def mue(self):
		"""mue commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_mue'):
			from .Tcw_.Mue import Mue
			self._mue = Mue(self._core, self._base)
		return self._mue

	@property
	def rtf(self):
		"""rtf commands group. 0 Sub-classes, 10 commands."""
		if not hasattr(self, '_rtf'):
			from .Tcw_.Rtf import Rtf
			self._rtf = Rtf(self._core, self._base)
		return self._rtf

	@property
	def sue(self):
		"""sue commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_sue'):
			from .Tcw_.Sue import Sue
			self._sue = Sue(self._core, self._base)
		return self._sue

	@property
	def ws(self):
		"""ws commands group. 2 Sub-classes, 25 commands."""
		if not hasattr(self, '_ws'):
			from .Tcw_.Ws import Ws
			self._ws = Ws(self._core, self._base)
		return self._ws

	# noinspection PyTypeChecker
	def get_tc(self) -> enums.EutraTestCaseTs36141:
		"""[SOURce<HW>]:BB:EUTRa:TCW:TC \n
		Selects the test case. \n
			:return: test_case: TS36141_TC839| TS36141_TC834| TS36141_TC835| TS36141_TC836| TS36141_TC67| TS36141_TC72| TS36141_TC73| TS36141_TC74| TS36141_TC75A| TS36141_TC75B| TS36141_TC76| TS36141_TC78| TS36141_TC821| TS36141_TC822| TS36141_TC823| TS36141_TC824| TS36141_TC831| TS36141_TC832| TS36141_TC833| TS36141_TC841| TS36141_TC838| TS36141_TC837
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:TC?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTestCaseTs36141)

	def set_tc(self, test_case: enums.EutraTestCaseTs36141) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:TC \n
		Selects the test case. \n
			:param test_case: TS36141_TC839| TS36141_TC834| TS36141_TC835| TS36141_TC836| TS36141_TC67| TS36141_TC72| TS36141_TC73| TS36141_TC74| TS36141_TC75A| TS36141_TC75B| TS36141_TC76| TS36141_TC78| TS36141_TC821| TS36141_TC822| TS36141_TC823| TS36141_TC824| TS36141_TC831| TS36141_TC832| TS36141_TC833| TS36141_TC841| TS36141_TC838| TS36141_TC837
		"""
		param = Conversions.enum_scalar_to_str(test_case, enums.EutraTestCaseTs36141)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:TC {param}')
