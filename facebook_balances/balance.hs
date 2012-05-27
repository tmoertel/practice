{-

Haskell solution to Facebook "balance the balances" interview problem.
(See my Python solution in the same directory for a description of the
problem.)

Tom Moertel <tom@moertel.com>
2012-05-27

-}

import Data.Array

main = interact $ readSolveAndShow

readSolveAndShow = showSoln . solve . readProblem

type Weight = Int
type BalanceId = Int
data Arm = Arm Weight [BalanceId]
data Balance = Balance Arm Arm

readProblem = readNBalances . map (map read . words) . lines

readNBalances ([n]:armspecs) =
  listArray (0, n - 1) . map readBalance . groupsOf 2 $ armspecs

readBalance :: [[Int]] -> Balance
readBalance [al, ar] = Balance (readArm al) (readArm ar)

readArm :: [Int] -> Arm
readArm (w:bs) = Arm w bs

groupsOf :: Int -> [a] -> [[a]]
groupsOf n [] = []
groupsOf n xs = take n xs : groupsOf n (drop n xs)

solve :: Array Int Balance -> Array Int Weight
solve bs = fmap snd cache
  where
    (lo, hi) = bounds bs
    cache = listArray (lo, hi) [ (weight, adjustment)
                               | (i, Balance larm rarm) <- assocs bs,
                                 let l = weigh larm
                                     r = weigh rarm
                                     adjustment = r - l
                                     weight = 10 + l + r + abs adjustment
                               ]
    weigh (Arm w bs) = w + sum (map (\i -> fst (cache!i)) bs)

showSoln = unlines . map (uncurry showAdjustment) . assocs

showAdjustment i adjustment = unwords [ show i ++ ":",
                                        show (max 0 adjustment),
                                        show (max 0 (-adjustment))
                                      ]
