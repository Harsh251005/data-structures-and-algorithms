"""
LC 1 · Two Sum · Easy
Link: https://leetcode.com/problems/two-sum/
Pattern: Hash map of complements (value -> index), one pass
Approach: Walk the list once. For each number, its complement is target - num.
          If the complement is already in the dict, return [its index, current index].
          Otherwise store num -> index so a later number can find it.
Key insight: check BEFORE adding. That stops a number pairing with itself
             ([3, 2, 4], 6), and duplicates like [3, 3] still work.
Brute force: try every pair (i, j > i): O(n^2) time, O(1) space.
Rejected: two pointers needs sorted input, and sorting loses the original indices
          (O(n log n) and fiddly).
Time: O(n)   Space: O(n)
Hints used: 3 (nudge, pattern, skeleton)   Time taken: ~53 min
"""


class Solution:
    def twoSumBrute(self, nums: list[int], target: int) -> list[int]:

        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

    def twoSum(self, nums: list[int], target: int):
        positions = {}

        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in positions:
                return [positions[diff], i]
            positions[nums[i]] = i
        return []


if __name__ == "__main__":
    s = Solution()

    # Each input has exactly one valid pair, as LeetCode guarantees.
    # sorted() makes the check order-independent: LeetCode accepts [i, j] or [j, i].
    for f in (s.twoSumBrute, s.twoSum):
        assert sorted(f([2, 7, 11, 15], 9)) == [0, 1]       # LeetCode example 1
        assert sorted(f([3, 2, 4], 6)) == [1, 2]            # self-match trap: 3 + 3 must not reuse index 0
        assert sorted(f([3, 3], 6)) == [0, 1]               # duplicate values are two different elements
        assert sorted(f([-3, 4, 3, 90], 0)) == [0, 2]       # negatives, target 0
        assert sorted(f([0, 4, 3, 0], 0)) == [0, 3]         # zeros: falsy, but still valid keys
        assert sorted(f([1, 5, 9, 14], 23)) == [2, 3]       # pair at the very end

    print("all tests passed ✅")
