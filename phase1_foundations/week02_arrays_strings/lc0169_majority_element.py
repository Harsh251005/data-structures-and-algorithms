"""
LC 169 · Majority Element · Easy
Link: https://leetcode.com/problems/majority-element/
Pattern: Boyer-Moore voting (cancel pairs); hash-map counting as the O(n)-space step
Approach: Use the candidate-vote based approach, wherein a candidate get's vote for each
          of the same number appeared, and looses the vote if another candidate appears.
          If it's 0, then the current number is assigned as the candidate and the last
          standing candidate is considered as the winner
Key insight: pair each vote for the leader with one vote against and drop both. A value
             with more than n/2 votes can't be fully cancelled, so the survivor is the
             winner. The vote that empties the stage is used up; the NEXT vote takes it.
Review notes: brute v1 compared a count with a value (`count > majority_element`), so
              [-1, -1, 2] gave 2. Brute v2 counted only j > i, so every count was one
              short and [5] gave 0. The first "optimal" never moved i (only ever counted
              nums[0]) and used >= n // 2; every test had the winner first, so it passed
              them all. The Boyer-Moore attempt checked `candidate == 0` instead of
              `count == 0` (a value of 0 isn't "nobody") and had no return.
Brute force: count every element against the whole list, O(n^2) time, O(1) space.
Hash map: one pass, num -> count, return once a count passes n // 2, O(n) time, O(n) space.
Time: O(n)   Space: O(1)   (Boyer-Moore)
Hints used: 4 (count-vs-value nudge, hash-map pattern, cancelling votes, rules + trace
            table), then Boyer-Moore solution viewed
Time taken: ~36 min (30 timeboxed + ~6 on the brute before the clock started)
"""


class Solution:
    def majorityElementBrute(self, nums: list[int]) -> int:
        majority_element = 0
        counter = 0

        for i in range(len(nums)):
            count = 0

            for j in range(len(nums)):
                if nums[i] == nums[j]:
                    count += 1
            if count > counter:
                counter = count
                majority_element = nums[i]

        return majority_element

    def majorityElement(self, nums: list[int]) -> int:
        seen = {}

        for num in nums:
            seen[num] = seen.get(num, 0) + 1

            if seen[num] > len(nums) // 2:
                return num
        return 0

    def majorityElementOptimal(self, nums: list[int]) -> int:
        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num

            if candidate == num:
                count += 1
            else:
                count -= 1

        return candidate


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 1, 2, 1, 1], 1),
        ([1, 1, 1], 1),
        ([3, 3, 1, 2, 3], 3),
        ([10, 10], 10),
        ([-1, -1, 2], -1),
        ([5], 5),
        ([1, 3, 3], 3),
        ([6, 5, 5], 5),
        ([0, 0, 1], 0),
        ([2, 2, 1, 1, 1, 2, 2], 2),  # added in review: leader changes twice mid-way
        ([1, 2, 1, 2, 1], 1),  # added in review: alternating, winner by exactly one vote
    ]
    for nums, expected in cases:
        for method in (s.majorityElementBrute, s.majorityElement, s.majorityElementOptimal):
            got = method(nums)
            assert got == expected, f"{method.__name__}({nums}) = {got}, want {expected}"
    print("all tests passed ✅")
