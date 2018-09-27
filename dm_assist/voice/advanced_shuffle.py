from collections import Sequence, Iterator

from dm_assist import util

class Shuffle(Sequence, Iterator):

    def __init__(self, items):
        self._items = items
        self._played_items = list()

        # This is used for the iterator
        self._cleared = False
    
    # Inherited functions

    def __contains__(self, item):
        return item in self._items

    def __getitem__(self, index):
        """
        This will select only previously unselected items until every item has been selected.
        Because of this, the size decreases every time you index an item.
        """
        curr_index = 0
        for i, item in enumerate(self._items):
            if i not in self._played_items:
                if curr_index is index:
                    self.__play_item(i)
                    return item
                curr_index += 1
        raise IndexError
    
    def __len__(self):
        return len(self._items) - len(self._played_items)
    
    def __iter__(self):
        self.clear_played()
        self._cleared = False
        return self

    def __next__(self):
        if self._cleared:
            raise StopIteration
        return self.get_next_item()

    # Custom functions

    def __play_item(self, index):
        self._played_items.append(index)
        if len(self._played_items) is len(self._items):
            self.clear_played()
    
    def get_next_item(self):
        """
        Selects the next item to play

        This item will never be selected again until every item has been selected once.

        This uses the roll_die function, because the random algorithmn may change,
        and I want it to use program's algorythmn
        """
        return self[util.roll_die(len(self), False) - 1]
    
    def clear_played(self):
        """
        Clear the played list.  This will allow previously selected items to be
        selectable again.
        """
        self._played_items.clear()
        self._cleared = True
