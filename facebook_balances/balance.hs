{-

Haskell solution to Facebook "balance the balances" interview problem.
(See my Python solution in the same directory for a description of the
problem.)

Tom Moertel <tom@moertel.com>
2012-05-27

-}


import Data.Array


type Weight      = Int
type BalanceId   = Int
data Arm         = Arm !Weight [BalanceId]
data Balance     = Balance !Arm !Arm
data BalanceInfo = BalanceInfo { weight :: !Weight, adjustment :: !Weight }

main = interact readSolveAndShow

readSolveAndShow = showSoln . solve . readProblem

readProblem = readNBalances . map (map read . words) . lines

readNBalances ([n]:armspecs) =
  listArray (0, n - 1) . map readBalance . groupsOf 2 $ armspecs

readBalance :: [[Int]] -> Balance
readBalance [la, ra] = Balance (readArm la) (readArm ra)

readArm :: [Int] -> Arm
readArm (w:bis) = Arm w bis

groupsOf :: Int -> [a] -> [[a]]
groupsOf n [] = []
groupsOf n xs = take n xs : groupsOf n (drop n xs)


-- |Compute adjustments to bring an array of balances into perfect balance
solve :: Array Int Balance -> Array Int Weight
solve balances = fmap adjustment cache
  where
    (lo, hi) = bounds balances
    weigh (Arm w bis) = w + sum (map (weight . (cache!)) bis)
    -- memo table: (weight, adjustment) pair for each balance i
    cache = (`fmap` balances) $ \(Balance larm rarm) ->
      let lw = weigh larm
          rw = weigh rarm
          adjustment = rw - lw
          weight = 10 + lw + rw + abs adjustment
      in BalanceInfo weight adjustment

showSoln = unlines . map (uncurry showAdjustment) . assocs

showAdjustment i adjustment =
  unwords [ show i ++ ":",
            show (max 0 adjustment),
            show (max 0 (-adjustment))
          ]
