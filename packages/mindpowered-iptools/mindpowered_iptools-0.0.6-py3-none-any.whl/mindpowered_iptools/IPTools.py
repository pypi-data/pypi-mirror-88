import maglev
import iptools

from typing import Any, List, Callable

class IPTools:
	"""
	IP Address Conversion and CIDR calculator
	"""
	def __init__(self):
		bus = maglev.maglev_MagLev.getInstance("default")
		lib = iptools.iptools_IPTools(bus)

	def SubnetMaskToCIDR(self, subnet_mask: str) -> object:
		"""		Convert a subnet mask to CIDR notation
		Args:
			subnet_mask (str):A subnet mask eg. 255.255.0.0
		Returns:
			object containing information about subnet including CIDR prefix
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [subnet_mask]
		ret = None
		def SubnetMaskToCIDR_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.SubnetMaskToCIDR', args, SubnetMaskToCIDR_Ret)
		return ret

	def CalcCIDR(self, ip_addr: str) -> List[Any]:
		"""		Given an IP address or IP address with CIDR notation, provides information about an IP address range
		Args:
			ip_addr (str):An IP address with or without CIDR notation
		Returns:
			a list of objects containing information about the IP address range
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ip_addr]
		ret = None
		def CalcCIDR_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.CalcCIDR', args, CalcCIDR_Ret)
		return ret

	def IPToDecimal(self, ip_addr: str) -> str:
		"""		Convert an IP address to a Decimal representation
		Args:
			ip_addr (str):An IP address
		Returns:
			Decimal representation of the provided IP address
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ip_addr]
		ret = None
		def IPToDecimal_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.IPToDecimal', args, IPToDecimal_Ret)
		return ret

	def IP4FromDecimal(self, ip4_number: str) -> str:
		"""		Convert from a Decimal representationan of an IP address
		Args:
			ip4_number (str):Decimal representation of an IP address
		Returns:
			The IP address
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ip4_number]
		ret = None
		def IP4FromDecimal_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.IP4FromDecimal', args, IP4FromDecimal_Ret)
		return ret

	def IP6FromDecimal(self, ip6_number: str) -> str:
		"""		Convert from a Decimal representationan of an IP address
		Args:
			ip6_number (str):Decimal representation of an IP address
		Returns:
			The IP address
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ip6_number]
		ret = None
		def IP6FromDecimal_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.IP6FromDecimal', args, IP6FromDecimal_Ret)
		return ret

	def IPv4ToIPv6(self, ip_addr: str) -> object:
		"""		Convert an IPv4 address to an IPv6 address
		Args:
			ip_addr (str):An IPv4 address
		Returns:
			An object containing IPv6 representations of the provided IPv4 address
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ip_addr]
		ret = None
		def IPv4ToIPv6_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.IPv4ToIPv6', args, IPv4ToIPv6_Ret)
		return ret

	def ExpandIPv6(self, ip6_addr: str) -> object:
		"""		Expand the zeros in an IPv6 address
		Args:
			ip6_addr (str):An IPv6 address
		Returns:
			The same IPv6 address with zeros expanded
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ip6_addr]
		ret = None
		def ExpandIPv6_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.ExpandIPv6', args, ExpandIPv6_Ret)
		return ret

	def CompressIPv6(self, ip6_addr: str) -> object:
		"""		Compress the zeros in an IPv6 address
		Args:
			ip6_addr (str):An IPv6 address
		Returns:
			The same IPv6 address with zeros compressed
		"""
		pybus = maglev.maglev_MagLevPy.getInstance("default")
		args = [ip6_addr]
		ret = None
		def CompressIPv6_Ret(async_ret):
			nonlocal ret
			ret = async_ret
		pybus.call('IPTools.CompressIPv6', args, CompressIPv6_Ret)
		return ret



