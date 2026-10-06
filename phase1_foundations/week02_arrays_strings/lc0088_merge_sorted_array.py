"""
LC 88 · Merge Sorted Array · Easy
Link: https://leetcode.com/problems/merge-sorted-array/
Pattern: Two pointers, one per sorted input (the "merge" step of merge sort)
Approach: walk both arrays with i and j, each pass append the smaller of
          nums1[i] / nums2[j] and move only that pointer. When one runs out,
          append the rest of the other. Copy the result back into nums1.
Key insight: exactly ONE value is taken per pass, so it is if/else (unlike
             LC 121, where both checks could fire on the same day).
Review notes: first versions used two independent ifs (second compare saw the
              already-moved i), put leftovers inside the loop with `if nums1:`
              (always true), and never wrote back into nums1.
Brute force: copy nums2 into the free slots and sort, O((m+n) log(m+n)).
Follow-up (re-solve challenge): O(1) extra space by filling nums1 from the
           BACK with three pointers, so nothing unread gets overwritten.
Time: O(m+n)   Space: O(m+n) for sorted_array
Hints used: 3 (15-min timebox hint, if/else + leftovers, write back + test format)
Time taken: 27 min (solved before the 30-min solution mark)
"""


class Solution:
    def mergeBrute(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        nums1[m:] = nums2[:n]
        nums1.sort()

    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        i = 0
        j = 0
        sorted_array = []

        while i < m and j < n:

            if nums1[i] <= nums2[j]:
                sorted_array.append(nums1[i])
                i += 1

            else:
                sorted_array.append(nums2[j])
                j += 1

        while i < m:
            sorted_array.append(nums1[i])
            i += 1

        while j < n:
            sorted_array.append(nums2[j])
            j += 1

        nums1[:] = sorted_array


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([1, 1, 2, 3, 4] + [0] * 6, 5, [2, 3, 3, 4, 4, 5], 6),  # his case, fixed to LeetCode's format in review
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3),  # added in review: LeetCode example 1
        ([1], 1, [], 0),  # added in review: nums2 empty
        ([0], 0, [1], 1),  # added in review: m = 0, all of nums1 is free space
        ([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3),  # added in review: all of nums2 is smaller
        ([2, 2, 0, 0], 2, [2, 2], 2),  # added in review: equal values
    ]
    for given, m, nums2, n in cases:
        expected = sorted(given[:m] + nums2)
        for method in (s.mergeBrute, s.merge):
            nums1 = given.copy()
            method(nums1, m, nums2, n)
            # added in review: check nums1 itself, it is what LeetCode judges
            assert nums1 == expected, f"{method.__name__}({given}, {m}, {nums2}, {n}) left {nums1}, want {expected}"
    print("all tests passed ✅")
