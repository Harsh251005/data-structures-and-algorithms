"""
LC 1 · Two Sum · Easy
Pattern:
Approach:
Time: O(?)   Space: O(?)
Hints used: 0   Time taken: ? min
"""


class Solution:
    def twoSumBrute(self, nums: list[int], target: int) -> list[int]:

        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        j = 1

        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                


if __name__ == "__main__":
    s = Solution()
    assert s.twoSum([1, 2, 4, 8, 10], 12) == [1, 4]
    assert s.twoSum([1, 2, 4, 8, 10], 3) == [0, 1]
    assert s.twoSum([1, 2, 4, 8, 10], 10) == [1, 3]
    assert s.twoSum([1, 2, 4, 8, 10], 15) == []

    print("all tests passed ✅")
