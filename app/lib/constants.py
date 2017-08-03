'''
Contains all constants that need to be shared across multiple functions.
'''

# Maps search types to the number of users that a debate of that type should
# have -- e.g. "joinable" debates should have 1 user, debates that are
# "in-progress" should have 2, etc. (This isn't actually very true anymore,
# depending on whether you think an "archived" debate has 0 or 2 users. Either way,
# this will probably be refactored at some point in the future)
SEARCH_TYPES = {
    "joinable": 1,
    "in-progress": 2,
    "archived": 0
}

# Common words that need to be removed to reduce debates returned in a search
COMMON_WORDS = ["it", "the", "what", "who", "is", "a", "be", "at"]
