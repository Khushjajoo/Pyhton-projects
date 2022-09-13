### Longest Palindrome
test_cases = [
 "a", "abaab", "racecar", "bullet", "rarfile",
 "computer", "windows", "saippuakivikauppias",
 "aaaaaaaaaaaaaaaaadaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
 "kkkkkkkkkkkkkkkkkkkkkkdldkkkkkkkkkkkkkkkkkkkkkk",
 "ddddddddddddddddddddddddddddddddddddddddddddddddddks"
]

class Solution:
    def longestPalindrome(self, s: str) -> str:
        start = 0       # Start position of longest palindrome 
        end = 0      # End position of longest palindrome
        for i in range(0, len(s)):
            # Palindome can be centered around 1 character or 2 characteres.
            # example aba  -> center is a
            #         abba -> center is bb
            # Try both methods and see which one gives the longer palindome.
            l1 = self.expand_around(s,i,i)
            l2 = self.expand_around(s,i,i+1)
            l = max(l1,l2)
            if l>end-start:
                start = i - (l - 1)//2
                end = i + l//2    
        return s[start : end+1]
    
    def expand_around(self, s, left, right):
        while(left>=0 and right<len(s) and s[left]==s[right]):
            left-=1
            right+=1
        
        return right-left-1
        
if __name__ == "__main__":
    solution = Solution()
    
    for test_case in test_cases:
        print(solution.longestPalindrome(test_case))
    
code.py
