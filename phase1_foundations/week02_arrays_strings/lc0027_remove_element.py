"""
LC 27 · Remove Element · Easy
Link: https://leetcode.com/problems/remove-element/
Pattern: Two pointers, same direction (slow writer i, fast reader j), same as LC 26
Approach: two pointers. j moves every step; if nums[j] == val it does nothing,
          otherwise nums[j] is written into slot i and i moves forward. So i only
          moves when a keeper is written.
Key insight: never move the vals anywhere. Copy every keeper into slot i; the
             leftovers past k are ignored. i ends up equal to k.
vs LC 26: j starts at 0, not 1, because nums[0] may itself be val. The write
          rule is "nums[j] != val" instead of "nums[j] != nums[i]".
Review note: first version also counted vals and returned len(nums) - count.
             Correct, but the count is redundant: i already equals k.
Brute force: build a new list of the non-val values, copy it back into nums:
             O(n) time, O(n) extra space.
Time: O(n)   Space: O(1)
Hints used: 3 (copy-keepers redirect, [3,2,2,3] trace table, j starts at 0)   Time taken: ~26 min
"""


class Solution:
    def removeElement(self, nums: list[int], val: int) -> int:
        i = 0

        for j in range(len(nums)):
            if nums[j] != val:
                nums[i] = nums[j]
                i += 1
        return i


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ([2, 0, 1, 2, 2, 3, 0, 4, 2], 2, [0, 1, 3, 0, 4]),
        ([3, 2, 2, 3], 3, [2, 2]),  # added in review: val at index 0
        ([], 1, []),  # added in review: empty input
        ([1], 1, []),  # added in review: single element, removed
        ([1], 2, [1]),  # added in review: single element, kept
        ([4, 4, 4], 4, []),  # added in review: everything removed
        ([1, 2, 3], 9, [1, 2, 3]),  # added in review: val not present
    ]
    for given, val, expected in cases:
        nums = given.copy()
        k = sol.removeElement(nums, val)
        assert k == len(expected), f"{given}, {val} returned {k}, want {len(expected)}"
        # added in review: LeetCode also checks the first k slots, not just k
        assert nums[:k] == expected, f"{given}, {val} left {nums[:k]}, want {expected}"
    print("all tests passed ✅")
