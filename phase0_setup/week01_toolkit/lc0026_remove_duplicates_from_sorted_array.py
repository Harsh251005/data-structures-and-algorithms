"""
LC 26 · Remove Duplicates from Sorted Array · Easy
Link: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
Pattern: Two pointers, same direction (slow writer i, fast reader j)
Approach: Used a two-pointer approach to check whether two values differ. If
          they do, write the jth value just after i and move i forward. If they
          are equal, keep moving j forward while i stays in its place.
Key insight: only the first k slots are checked, so never move duplicates out.
             Copy each new unique value in at i + 1 and ignore the rest.
Gotcha: a counter set only inside the loop (k = 0, then k = i + 1) stays 0
        when the loop body never runs ([7], [1, 1, 1]). nums[0] is always
        unique, so return i + 1.
Brute force: collect the unique values into a new list, copy them back into
             nums, return their count: O(n) time, O(n) extra space.
Time: O(n)   Space: O(1)
Hints used: 3 (write-unique reframe, i = j bug + one-if loop, crash debug)   Time taken: ~53 min
"""


class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        i = 0

        for j in range(1, len(nums)):
            if nums[i] != nums[j]:
                nums[i + 1] = nums[j]
                i += 1
        return i + 1


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ([1, 2, 2, 2, 2, 3, 4, 4, 5, 5], [1, 2, 3, 4, 5]),
        ([4, 5, 6, 6, 8, 10], [4, 5, 6, 8, 10]),
        ([0, 0, 1, 2, 3], [0, 1, 2, 3]),
        ([1, 1, 1], [1]),
        ([10], [10]),
        ([1, 2, 3], [1, 2, 3]),  # added in review: no duplicates, every write is a self-copy
        ([-3, -3, -1, 0, 0], [-3, -1, 0]),  # added in review: negatives and zero
    ]
    for given, expected in cases:
        nums = given.copy()
        k = sol.removeDuplicates(nums)
        assert k == len(expected), f"{given} returned {k}, want {len(expected)}"
        # added in review: LeetCode also checks the first k slots, not just k
        assert nums[:k] == expected, f"{given} left {nums[:k]}, want {expected}"
    print("all tests passed ✅")
