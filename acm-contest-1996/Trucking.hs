-- Tom Moertel <tom@moertel.com>
--
-- My solution to Problem G of the 20th Annual ACM International
-- Collegiate Programming Contents Finals.
--
-- https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
--
-- $Id: Trucking.hs,v 1.1 2002/02/27 19:46:17 thor Exp $

-- ASSUMPTION: No shipment destined for processing center r will ever
-- arrive at a processing center c that lacks a relay door for r.  In
-- other words, when a truck arrives at c, we know that each of the
-- truck's shipments is destined for c or a relay center for which c
-- has a relay door.  Thus, there is no need to compute routes through
-- intermediate relay centers.  The problem descripion implies this
-- because it never suggest that there might be 

module Main (main) where

import List

type CID                 =  Int -- Center ID
type ShipmentID          =  Int
type Volume              =  Int
type Time                =  Int
type Center              =  (CID, (Int, Int, [RelayDoor]))
type RelayDoor           =  (CID, (Volume, Time))
type Truck               =  (Time, CID, [Shipment])
type Shipment            =  (ShipmentID, CID, CID, Volume, Time)

type Problem             =  ([Center], [Truck])
type Solution            =  ([(CID, Double)], [Shipment]) -- waits & lates

type ShipState           =  (CID, [

main                     :: IO ()
main                     =  interact $ readSolveAndShow

readSolveAndShow         =  showResults . solve . readProblem

readProblem              :: String -> Problem
readProblem s            =  (centers, trucks)
    where
    centers              =  take numCenters . readCenters $ xs
    trucks               =  take numTrucks . readTrucks $ xs'
    (numCenters:xs)      =  (map read . words $ s) :: [Int]
    (numTrucks:xs')      =  drop (3 * (numCenters + totalRelayDoors)) xs
    totalRelayDoors      =  sum . map numRelays $ centers

readCenters              :: [Int] -> [Center]
readCenters []           =  []
readCenters (cid:s:d:xs) =  (cid, (s,d, take d . map g3toRD . groupsOf 3 $ xs))
                            : readCenters (drop (3*d) xs)
    where
    g3toRD [r,v,l]       =  (r, (v,l))

readTrucks               :: [Int] -> [Truck]
readTrucks []            =  []
readTrucks (ar:cid:s:xs) =  (ar, cid, take s . map g5toShpt . groupsOf 5 $ xs)
                            : readTrucks (drop (5*s) xs)
    where
    g5toShpt [i,o,r,v,t] =  (i,o,r,v,t)

groupsOf _ []            =  []     
groupsOf n xs            =  take n xs : groupsOf n (drop n xs)

numRelays                :: Center -> Int
numRelays (_,(_,r,_))    =  r

solve                    :: Problem -> Solution
solve                    =  solve' [] []

solve'                   :: Problem -> [(CID, Time)] -> [Shipment] -> Solution
solve' state (cs,ts)     =  

                             

showResults              :: Solution -> String
showResults              =  const "Solution!"

avg                      :: [Time] -> Double
avg []                   =  0.0
avg xs                   =  fromIntegral (sum xs) / fromIntegral (length xs)
