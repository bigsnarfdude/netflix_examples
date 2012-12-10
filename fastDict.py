import array
import collections
import itertools
import pprint

# Placeholder constants
FREE = -1
DUMMY = -2
UNUSED = ':UNUSED:'          # In C, be sure to use a unique object

class Dict(collections.MutableMapping):
    '''Space efficient dictionary with fast iteration
       and cheap resizes (minimum data movement)
    '''

    @staticmethod
    def _gen_probes(hashvalue, n):
        'Same sequence of probes used in the current dictionary design'
        PERTURB_SHIFT = 5
        if hashvalue < 0:
            hashvalue = int(2 ** 64 - hashvalue)
        i = hashvalue % n     # When n is a power-of-two, binary-and is faster
        yield int(i)
        perturb = hashvalue
        while True:
            i = ((i << 2) + i + perturb + 1)
            yield int(i % n)
            perturb >>= PERTURB_SHIFT

    def _lookup(self, key, hashvalue):
        'Same lookup logic as currently used in real dicts'
        assert len(self.keylist) < len(self.indices)   # At least one open slot
        freeslot = None
        for i in self._gen_probes(hashvalue, len(self.indices)):
            if self.indices[i] is FREE:
                if freeslot is not None:
                    i = freeslot
                return (False, i)
            elif self.indices[i] is DUMMY:
                freeslot = i
            else:
                index = self.indices[i]
                if (self.keylist[index] is key or
                    self.hashlist[index] == hashvalue
                    and self.keylist[index] == key):
                    return (True, i)

    def _next_open_index(self):
        '''New logic:  Store hash/key/value entries in a dense list.
           If an unused entry is available, re-use it; otherwise,
           append a new entry to the end of the list. '''
        if self.size == len(self.keylist):
            index = len(self.keylist)
            self.hashlist.append(None)
            self.keylist.append(None)
            self.valuelist.append(None)
            return index
        # Least common case.  Can make fast in C with a pointer chain.
        return self.keylist.index(UNUSED)

    def _make_index(self, n):
        'New sequence of indices using the smallest possible datatype'
        typecode = 'b' if n <= 128 else 'h' if n <= 65536 else 'l'
        return array.array(typecode, itertools.repeat(FREE, n))

    def _resize(self, n):
        '''Reindex the existing hash/key/value entries
           and compact the entry list.

           No calls are made to hash() or __eq__().
           No hash/key/value entries get moved except
           to fill-in an UNUSED slot in the entry sequence.

        '''
        self.indices = self._make_index(n)
        for index, hashvalue in enumerate(self.hashlist):
            while hashvalue is UNUSED:
                hashvalue = self.hashlist.pop()
                key = self.keylist.pop()
                value = self.valuelist.pop()
                if index >= len(self.hashlist):
                    return
                self.hashlist[index] = hashvalue
                self.keylist[index] = key
                self.valuelist[index] = value
            for i in Dict._gen_probes(hashvalue, n):
                if self.indices[i] is FREE:
                    break
            self.indices[i] = index

    def __init__(self, *args, **kwds):
        self.indices = self._make_index(8)
        self.hashlist = []
        self.keylist = []
        self.valuelist = []
        self.size = 0
        self.update(*args, **kwds)

    def __setitem__(self, key, value):
        hashvalue = hash(key)
        found, i = self._lookup(key, hashvalue)
        if found:
            index = self.indices[i]
            self.valuelist[index] = value
        else:
            index = self._next_open_index()
            self.indices[i] = index
            self.hashlist[index] = hashvalue
            self.keylist[index] = key
            self.valuelist[index] = value
            self.size += 1
            if len(self) * 3 >= len(self.indices) * 2:
                self._resize(2 * len(self.indices))

    def __getitem__(self, key):
        hashvalue = hash(key)
        found, i = self._lookup(key, hashvalue)
        if found:
            index = self.indices[i]
            return self.valuelist[index]
        else:
            raise KeyError(key)

    def __delitem__(self, key, hashvalue=None):
        if hashvalue is None:
            hashvalue = hash(key)
        found, i = self._lookup(key, hashvalue)
        if found:
            index = self.indices[i]
            self.indices[i] = DUMMY
            self.hashlist[index] = UNUSED
            self.keylist[index] = UNUSED
            self.valuelist[index] = UNUSED
            self.size -= 1
        else:
            raise KeyError(key)

    def __iter__(self):
        for key in self.keylist:
            if key is not UNUSED:
                yield key

    def __len__(self):
        return self.size

    def __repr__(self):
        return 'Dict(%r)' % self.items()

    ###### Diagnostic methods.  Not part of the API ##############

    def show_structure(self):
        print '=' * 50
        print 'Dict:', self
        print 'Size in bytes:', self.memory()
        print 'Indices:', self.indices
        entries = itertools.izip_longest(
                        xrange(len(self.hashlist)), self.hashlist, self.keylist, self.valuelist,
                        fillvalue = ':ERROR:')
        pprint.pprint(list(entries))
        print '-' * 50

    def memory(self):
        'Size in bytes assuming a 64-bit build'
        return (len(self.indices) * self.indices.itemsize
                + len(self.hashlist) * 8 * 3)

if __name__ == '__main__':

    d = Dict([('timmy', 'red'), ('barry', 'green'), ('guido', 'blue')])
    d.show_structure()
