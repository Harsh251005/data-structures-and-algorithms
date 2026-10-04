"""
LC 217 · Contains Duplicate · Easy
Pattern: Hash set for seen-before lookup
Approach: Walk the list keeping a set of numbers already seen. If the current
          number is already in the set, it's a duplicate, so return True right away.
          Reaching the end means every number was unique.
Key insight: `x in set` is O(1), but `x in list` is O(n). The same code with a list
             would quietly become O(n^2).
Brute force: compare every pair (i, j > i): O(n^2) time, O(1) space.
Time: O(n)   Space: O(n)   (trades memory for speed)
Alt: len(set(nums)) != len(nums) is also O(n), but it can't stop early on a duplicate.
Hints used: 0   Time taken: ~10 min
"""


class Solution:
    # O(n^2) time, O(1) space
    def containsDuplicateBrute(self, nums: list[int]) -> bool:

        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] == nums[j]:
                    return True

        return False

    # O(n) time, O(n) space
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen: set[int] = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False


if __name__ == "__main__":
    s = Solution()

    for f in (s.containsDuplicateBrute, s.containsDuplicate):
        assert f([1, 1, 2, 3, 4])
        assert f([1, 2, 3, 4, 4])
        assert f([1, 2, 3, 4, 3])
        assert f([1, 2, 3, 4, 1])
        assert not f([1, 2, 3, 4, 5])
        assert not f([5, 4, 3, 2, 1, -5])
        assert not f([7])                    # added in review: single element, the smallest valid input
        assert f([0, 0])                     # added in review: zero is falsy in Python, so check it's still caught
        assert f([-3, 1, -3])                # added in review: negative duplicates
        assert not f([-1, 0, 1])             # added in review: negatives, zero and positives, all unique

    print("all tests passed ✅")
