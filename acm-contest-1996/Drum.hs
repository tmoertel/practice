-- Tom Moertel <tom@moertel.com>
--
-- My solution to Problem D of the 20th Annual ACM International
-- Collegiate Programming Contents Finals.
--
-- https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
--
-- $Id: Drum.hs,v 1.1 2002/02/11 04:14:59 thor Exp $

module Main (main) where

import List
import Numeric (showFFloat)

type Adr                 =  Int
type Instruction         =  (Adr, [Adr]) -- (instr addr, [next addr(s)])
type Case                =  (Int, Int, [Instruction]) -- n, t, program
type Solution            =  Double

main                     :: IO ()
main                     =  interact $ readSolveAndShow

readSolveAndShow         =  showResults . map (solve 1 1) . readCases

showResults              :: [Solution] -> String
showResults              =  unlines . map show1result . zip [1..]
    where
    show1result (n,soln) =  "Case " ++ show n ++ ". Execution time = "
                            ++ showFFloat (Just 4) soln ""

-- dp = "drum pointer" (addr under read head); a = desired address to execute
-- n = number of instruction slots on the drum, t = tExecute 1 instruction
                            
solve                    :: Adr -> Adr -> Case -> Solution
solve dp a (n,t,prog)    =  solve' dp a 
    where
    solve' dp a          =  (fromIntegral (tSeekAndRead + t)) + tRest
        where
        tSeekAndRead     =  1 + ((a - dp) `mod` n)
        tRest            =  avg . map (solve' (a + 1 + t)) $
                            case lookup a prog of Just instrs -> instrs

avg                      :: [Double] -> Double
avg []                   =  0.0
avg xs                   =  sum xs / (fromIntegral $ length xs)

readCases                :: String -> [Case]
readCases                =  concatMap mkCase . caseGroup . lines
       
mkCase                   :: [String] -> [Case]
mkCase lines             =  case map (map read . words) lines of
                                ([0,0]:_)      -> [] -- terminator case
                                ([n,t]:instrs) -> [(n, t, map mkInstr instrs)]

mkInstr                  :: [Int] -> Instruction
mkInstr (addr:_:rest)    =  (addr, rest)

caseGroup                :: [String] -> [[String]]
caseGroup xs             =  case break ("0"==) xs of
                                (g,_:gs) -> g : caseGroup gs
                                (g,_)    -> [g]
