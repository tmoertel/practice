-- Tom Moertel <tom@moertel.com>
--
-- My solution to Problem E of the 20th Annual ACM International
-- Collegiate Programming Contents Finals.
--
-- https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
--
-- $Id: PatMatch.hs,v 1.3 2002/02/11 06:33:29 thor Exp $

module Main (main) where

import List

type Problem             =  [[Double]] -- a matrix
type Solution            =  (Int, Int) -- row and column of "central gravity"

main                     :: IO ()
main                     =  interact $ readSolveAndShow

readSolveAndShow         =  showResults . map solve . readProblems . words

showResults              :: [Solution] -> String
showResults              =  unlines . map show1soln . zip [1..]
    where
    show1soln (n,soln)   =  "Case " ++ show n ++ ": center at " ++ show soln

solve                    :: Problem -> Solution
solve matrix             =  (solve' matrix, solve' (transpose matrix))

solve'                   :: Problem -> Int
solve' matrix            =  negate . snd . minimum $ lrdiffs
    where
    lrdiffs              =  [ (abs (l - r), i)
                              | (l,r,i) <- zip3 rampL (tail rampR) [-1,-2..] ]
    rampR                =  scanr (+) 0 totals
    rampL                =  scanl (+) 0 totals
    totals               =  map sum matrix

readProblems             :: [String] -> [Problem]
readProblems ("0":"0":_) =  []
readProblems (r:c:ws)    =  (take rows . groupsOf cols . map read0 $ ws)
                            : readProblems (drop (rows * cols) ws)
    where
    (rows, cols)         =  (read r, read c)

groupsOf _ []            =  []     
groupsOf n xs            =  take n xs : groupsOf n (drop n xs)

read0 ('.':xs)           =  read ("0." ++ xs)
read0 xs                 =  read xs
