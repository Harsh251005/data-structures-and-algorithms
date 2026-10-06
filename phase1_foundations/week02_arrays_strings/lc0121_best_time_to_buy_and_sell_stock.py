"""
LC 121 · Best Time to Buy and Sell Stock · Easy
Link: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
Pattern: One pass with a running minimum ("best thing seen so far")
Approach: for each sell day, the best buy day is the cheapest day before it.
          Carry that cheapest price forward instead of looking back each time.
Key insight: the i pointer from the brute force becomes one variable,
             cheapest_price. Two independent checks per day: is today the new
             cheapest? does selling today beat the best profit?
Review notes: first one-pass attempt kept i/j from the brute force, moved i
              every step (so it compared neighbours), started cheapest at 0
              (never updates), and joined both updates with `and` (never true
              on the same day). Return type is int, not int | float: inf only
              ever lives in cheapest_price, never in the profit.
Brute force: every (buy, later sell) pair, O(n^2) time, O(1) space. Times out
             on LeetCode (n up to 10^5).
Time: O(n)   Space: O(1)
Hints used: 4 (min-so-far redirect, trace table, inf vs prices[0], separate ifs), then solution viewed
Time taken: ~54 min (gave up; pre-timebox)
"""


class Solution:
    def maxProfitBrute(self, prices: list[int]) -> int:
        profits = 0

        for i in range(len(prices)):
            for j in range(i + 1, len(prices)):  # review: sell strictly after buy
                current_profit = prices[j] - prices[i]
                if profits < current_profit:
                    profits = current_profit

        return profits

    def maxProfit(self, prices: list[int]) -> int:
        cheapest_price = float('inf')
        maximum_profit = 0

        for price in prices:
            if price < cheapest_price:
                cheapest_price = price
            if price - cheapest_price > maximum_profit:
                maximum_profit = price - cheapest_price

        return maximum_profit


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([7, 1, 5, 3, 6, 4], 5),
        ([3, 7, 1, 5, 3, 6, 4], 5),
        ([5, 4, 3, 2, 1], 0),
        ([10], 0),
        ([], 0),
        ([2, 4, 1], 2),  # added in review: new minimum AFTER the best sale must not erase it
        ([1, 2, 3, 4, 5], 4),  # added in review: rising prices, buy first day, sell last
        ([3, 3, 3], 0),  # added in review: flat prices
    ]
    for prices, expected in cases:
        for method in (s.maxProfitBrute, s.maxProfit):
            got = method(prices)
            assert got == expected, f"{method.__name__}({prices}) = {got}, want {expected}"
    print("all tests passed ✅")
