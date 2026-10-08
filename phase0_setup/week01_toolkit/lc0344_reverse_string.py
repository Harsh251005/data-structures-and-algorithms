"""
LC 344 · Reverse String · Easy
Link: https://leetcode.com/problems/reverse-string/
Pattern: Two pointers converging from both ends
Approach: Put i at the start and j at the end. Swap s[i] and s[j], then move
          both inward. Stop when they meet; every pair has been swapped once.
Key insight: in-place means mutate the list you were given. `s = s[::-1]`
             only rebinds the local name, so the caller's list never changes.
Brute force: copy s reversed (s[::-1]) and write it back element by element:
             O(n) time, O(n) space for the copy.
Alt: swap through a temp variable (temp = s[i]; s[i] = s[j]; s[j] = temp). The first
     version did this; the tuple swap is the Python idiom.
Note: `i <= j` also works (the first version used it), but `i < j` is enough. When
      i == j it would only swap the middle element with itself.
Time: O(n)   Space: O(1)
Hints used: 3 (ChatGPT "how to reverse", in-place fix, two-pointer nudge)   Time taken: ~42 min
"""


class Solution:
    def reverseStringBrute(self, s: list[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        j = 0

        for i in s[::-1]:
            s[j] = i
            j += 1

    def reverseString(self, s: list[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        i = 0
        j = len(s) - 1

        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1


if __name__ == "__main__":
    sol = Solution()
    cases = [
        (["h", "e", "l", "l", "o"], ["o", "l", "l", "e", "h"]),
        (["H", "a", "n", "n", "a", "h"], ["h", "a", "n", "n", "a", "H"]),
        (["a"], ["a"]),  # edge: single element
        (["a", "b"], ["b", "a"]),  # edge: two elements, one swap
        (["a", "b", "c"], ["c", "b", "a"]),  # edge: odd length, middle stays put
        (["a", "a", "a"], ["a", "a", "a"]),  # edge: all the same
    ]
    for method in (sol.reverseStringBrute, sol.reverseString):
        for given, expected in cases:
            s = given.copy()  # in-place: each method gets a fresh list
            assert method(s) is None, f"{method.__name__} should return None"
            assert s == expected, f"{method.__name__}({given}) left {s}, want {expected}"
    print("all tests passed ✅")
