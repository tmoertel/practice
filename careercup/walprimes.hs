module Walprimes where

import qualified Data.Set as Set
import Data.List (foldl')

type Digit = Integer
type Digits = [Digit]

data Operator = Add | Sub | Glue deriving (Eq, Ord, Enum)

walcount :: Digits -> Int
walcount = length . filter walprime . uniq . exprs

walprime :: Integer -> Bool
walprime n = or [n `rem` i == 0 | i <- [2, 3, 5, 7]]

exprs :: Digits -> [Integer]
exprs [] = []
exprs ds = map (eval . (`zip` ds)) (cprod opss)
  where opss = [Add] : replicate (length ds - 1) [Add, Sub, Glue]

cprod :: [[a]] -> [[a]]
cprod = foldr times [[]] where times xs yss = [x:ys | x <- xs, ys <- yss]

eval :: [(Operator, Digit)] -> Integer
eval = app . foldl' step (0, Add, 0)
  where
    app (acc, op, term) = opfn op acc term
    step (acc, op, term) (Glue, d) = (acc, op, 10 * term + d)
    step state           (op, d)   = (app state, op, d)

opfn :: Num n => Operator -> n -> n -> n
opfn Add  = (+)
opfn Sub  = (-)
opfn Glue = \n d -> 10 * d + n

uniq :: Ord a => [a] -> [a]
uniq = Set.toList . Set.fromList
