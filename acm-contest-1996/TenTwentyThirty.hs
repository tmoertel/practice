-- Tom Moertel <tom@moertel.com>
--
-- My solution to Problem A of the 20th Annual ACM International
-- Collegiate Programming Contents Finals.
--
-- https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
--
-- $Id: TenTwentyThirty.hs,v 1.7 2002/02/08 22:14:30 thor Exp $

module Main (main) where

import List

type Card              =  Int        
type Pile              =  [Card]
type Deck              =  Pile
type GameState         =  ( [Pile]   -- non-empty piles in play
                          , Deck     -- player's deck
                          )

main                   =  interact $ unlines . map playGame . readDecks

readDecks              :: String -> [Deck]
readDecks              =  groupsOf 52 . takeWhile (>0) . map read . words

groupsOf _ []          =  []     
groupsOf n xs          =  take n xs : groupsOf n (drop n xs)

playGame               :: Deck -> String
playGame               =  determineResult . playTurns . initializeGame

initializeGame deck    =  (transpose [deal0], deck')
    where
    (deal0, deck')     =  splitAt 7 deck

playTurns              :: GameState -> [GameState]
playTurns (p:ps, d:ds) =  state' : playTurns state'
    where
    state'             =  (ps ++ filter (not . null) [p'], deck')
    (p', deck')        =  reducePile (d:p) ds
playTurns _            =  [] -- win or loss

reducePile [b,a] ds    = ([b,a], ds) -- corner case, might falsely match below
reducePile pile ds     = case (reverse pile, pile) of
                             (a:b:_, c:_) | ttt a b c -> pickup 2 1 [a,b,c]
                             (a:_, c:b:_) | ttt a b c -> pickup 1 2 [a,b,c]
                             (_, c:b:a:_) | ttt a b c -> pickup 0 3 [a,b,c]
                             _                        -> (pile, ds)
    where
    pickup f l picks   = reducePile (bidrop f l) (ds ++ picks)
    bidrop f l         = let cs = drop l pile in reverse (drop f (reverse cs))
                         -- drop first f cards and last l cards from pile
                         -- note: the head of a pile is its *last* card

ttt a b c              = let s = a+b+c in s==10 || s==20 || s==30

determineResult        :: [GameState] -> String
determineResult states =  result ++ show (7 + length states')
    where
    states'            =  trimCycle [] states
    result             =  case last states' of
                              ([], _) -> "Win : "
                              (_, []) -> "Loss: "
                              _       -> "Draw: "

trimCycle acc []       =  reverse acc
trimCycle acc (x:xs)   =  trimCycle (x:acc) (if x `elem` acc then [] else xs)
