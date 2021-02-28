-- Tom Moertel <tom@moertel.com>
--
-- My solution to Problem B of the 20th Annual ACM International
-- Collegiate Programming Contents Finals.
--
-- https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
--
-- $Id: CallingCircles.hs,v 1.1 2002/02/10 07:09:48 thor Exp $

module Main (main) where

import List

import Graph   (mkUGraph) -- from Functional Graph Library
import DFS     (scc)

type Name                =  String
type Call                =  [Name] -- of length 2 [from, to]
type CallSet             =  [Call]
type CallingCircle       =  [Name]
type Solution            =  [CallingCircle]

main                     :: IO ()
main                     =  interact $ readSolveAndShow

readSolveAndShow         =  showResults . map solve . readSets

readSets                 :: String -> [CallSet]
readSets                 =  callSets . groupsOf 2 . words
    where
    callSets ([_,m]:cs)  =  case (read m :: Int) of
                                 0 -> []
                                 x -> take x cs : callSets (drop x cs)
       
showResults              :: [Solution] -> String
showResults              =  unlines . concatMap show1result . zip [1..]
    where
    show1result (n,soln) =  ("Calling circles for data set " ++ show n ++ ":")
                            : map (concat . intersperse ", ") (soln ++ [[]])

solve                    :: CallSet -> Solution
solve calls              =  map (map (callers!!)) $ scc callGraph
    where
    callGraph            =  mkUGraph (map snd ixCallers) edges
    edges                =  pairs . map (map callerIx) $ calls
    callerIx a           =  case lookup a ixCallers of Just ix -> ix
    ixCallers            =  zip callers [0..]
    callers              =  uniq . concat $ calls

pairs                    =  map ( \ [a,b] -> (a,b) )

groupsOf _ []            =  []     
groupsOf n xs            =  take n xs : groupsOf n (drop n xs)

uniq                     :: (Ord a) => [a] -> [a]
uniq                     =  map head . group . sort
