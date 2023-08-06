"""Compare data structures containing matching CIDs of different versions and encoding"""

import collections.abc

import cid


__version__ = "1.1.1"


def normalize(obj):
	# Text or binary string with a least a length of 7 characters may be a CID
	if isinstance(obj, (str, bytes)) and len(obj) >= 7:
		# Try to decode string as CID
		try:
			obj = cid.make_cid(obj)
		except ValueError:
			pass
	
	# Convert all CIDs to their version 1 representation
	if isinstance(obj, cid.cid.BaseCID):
		if obj.version != 1:
			obj = obj.to_v1()
	
	# Sequences (tuples, lists, …) and sets may contain CID values
	if isinstance(obj, (collections.abc.Sequence, collections.abc.Set)) \
	   and not isinstance(obj, (str, bytes)):  # ← these are handled above
		# Try to substitute CID values in all sequence items
		mutated = False
		items   = []
		for item in obj:
			item_new = normalize(item)
			mutated |= (item is not item_new)
			items.append(item_new)
		
		# Recreate sequence/set object with new values
		# NOTE: Recreating sequences in this way may not work for custom types!
		if mutated:
			obj = obj.__class__(items)
		items = None
	
	# Mappings (dict, OrderedDict, …), may also contain CID values
	if isinstance(obj, collections.abc.Mapping):
		# Try to substitute CID values in all sequence items
		mutated = False
		items   = []
		for key, value in obj.items():
			key_new   = normalize(key)
			value_new = normalize(value)
			mutated |= (key is not key_new) or (value is not value_new)
			items.append((key_new, value_new))
		
		# Recreate mapping object with new values
		# NOTE: Recreating mappings in this way may not work for custom types!
		if mutated:
			obj = obj.__class__(dict(items))
		items = None
	
	return obj


class match(object):
	def __init__(self, obj):
		self.obj = obj
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			other = other.obj
		return normalize(self.obj) == normalize(other)
