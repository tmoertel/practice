-- Tom Moertel <tom@moertel.com>
--
-- My solution to Problem F of the 20th Annual ACM International
-- Collegiate Programming Contents Finals.
--
-- https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
--
-- $Id: Trellis.hs,v 1.2 2002/02/12 00:14:50 thor Exp $

module Main (main) where

import List

type State               =  Char
type TransMatrix         =  [[ [State] ]] -- square matrix of state lists
type NTA                 =  (TransMatrix, [State]) -- tt, accepting states
type Input               =  [State]
type Problem             =  (NTA, [Input])
type Solution            =  [String]  -- accepted/rejected and input

main                     :: IO ()
main                     =  interact $ readSolveAndShow

readSolveAndShow         =  showResults . map solve . readProblems . words

readProblems             :: [String] -> [Problem]
readProblems ("0":"0":_) =  []
readProblems (n:a:ws)    =  ((txMatrix, final numAcpt states), inputs)
                            : readProblems rest
    where
    txMatrix             =  take numStates . groupsOf numStates $ ws
    states               =  take numStates ['a'..]
    (inputs, _:rest)     =  break ("#"==) . drop (numStates^2) $ ws
    (numStates, numAcpt) =  (read n, read a)

solve                    :: Problem -> Solution
solve ((txM, acs), inps) =  zipWith (++) (map solve' inps) inps
    where
    solve' xs            =  if accept xs then "accept  " else "reject  "
    accept [x]           =  x `elem` acs
    accept xs            =  any accept . transitions $ xs
    transitions xs       =  combinations . map (mx txM) $ zip xs (tail xs)

final                    :: Int -> [a] -> [a]
final n                  =  reverse . take n . reverse

groupsOf _ []            =  []     
groupsOf n xs            =  take n xs : groupsOf n (drop n xs)

mx                       :: TransMatrix -> (State, State) -> [State]
mx txM (stL,stR)         =  txM !! spos stL !! spos stR

spos                     :: State -> Int
spos s                   =  fromEnum s - fromEnum 'a'

combinations             :: [[a]] -> [[a]]
combinations             =  foldr outer [[]]
xs `outer` yss           =  [ x:ys | x <- xs, ys <- yss ] 

showResults              :: [Solution] -> String
showResults              =  unlines . map show1soln . zip [1..]
    where
    show1soln (n,soln)   =  unlines . concat $ 
                            [ ["NTA " ++ show n]
                            , soln
                            , []
                            ]
