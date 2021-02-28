-- Tom Moertel <tom@moertel.com>
--
-- My solution to Problem C of the 20th Annual ACM International
-- Collegiate Programming Contents Finals.
--
-- https://icpc.global/newcms/community/history-icpc-1996/1996WorldFinalProblemSet.pdf
--
-- $Id: CuttingCorners.hs,v 1.9 2002/02/10 07:09:28 thor Exp $

module Main (main) where

import List
import Numeric (showFFloat)

import Graph   ((&), empty) -- from Functional Graph Library
import SP      (sp, spLength)

import IO
import IOExts

type Coord               =  Double
type Point               =  (Coord, Coord)
type Vector              =  Point
type Line                =  (Point, Point)
type Rect                =  [Point] -- of length 4

data Scenario            =  Scenario { start, finish :: Point
                                     , buildings     :: [Rect]
                                     }
                                     deriving Show

main                     :: IO ()
main                     =  interact $ readSolveAndShow

readSolveAndShow         =  showResults . map solve . readScenarios

readScenarios            :: String -> [Scenario]
readScenarios            =  mkScenarios . words
    where
    mkScenarios ("-1":_) =  []
    mkScenarios (w:ws)   =  Scenario (sx,sy) (fx,fy) bldgs : mkScenarios ws'
        where
        (scWords, ws')   =  splitAt (4 + 6 * read w) ws
        coords           =  map read scWords
        [sx,sy,fx,fy]    =  take 4 coords
        bldgs            =  map (mkRect . mkPts) $ groupsOf 6 $ drop 4 coords
    mkScenarios ws       =  error $ concat ("not scenario input: " : ws)
                                           
showResults              :: [Coord] -> String
showResults              =  unlines . concatMap show1 . zip [1..] 
    where
    show1 (i, d)         =  ["Scenario #" ++ show i
                            ,"   route distance: " ++ showFFloat (Just 2) d ""]

solve                    :: Scenario -> Coord
solve                    =  spLength 0 1 . mkGrph -- 0 is start, 1 is finish

-- replace the above definition with the one below to generate
-- Mathematica Graphics (in InputForm) on stderr
--
-- solve s                  =  diagnostic s `seq` spLength 0 1 $ mkGrph s

mkGrph (Scenario s f bs) =  foldr (&) empty contexts
    where
    contexts             =  [let e = edges i a in (e,i,i,e) | (i,a) <- ixNavVs]
    edges i a            =  [(dist a b, j) | (j,b) <- ixNavVs, i < j
                                           , none (cuts (a,b)) bldgDiags]
    ixNavVs              =  zip [0..] navVs
    navVs                =  s : f : filter (`notElem`[s,f]) nonInteriorBldgPts
    bldgDiags            =  concatMap diagonals bs
    nonInteriorBldgPts   =  [p | p <- uniq (concat bs), none (ptInRect p) bs]

vec                      :: Point -> Point -> Vector
vec (x0, y0) (x1, y1)    =  (x1 - x0, y1 - y0)

vadd                     :: Vector -> Vector -> Vector
vadd (x0, y0) (x1, y1)   =  (x0 + x1, y0 + y1)

dist                     :: Point -> Point -> Coord
dist a b                 =  let (dx,dy) = vec a b in sqrt (dx*dx + dy*dy)

mkRect                   :: [Point] -> Rect -- 3 corner points to 4
mkRect cs                =  [a, rightCorner, b, b `vadd` vec rightCorner a]
    where
    (_, hyp@[a, b])      =  maximum [(dist u v, [u,v]) | u <- cs, v <- cs, u<v]
    [rightCorner]        =  filter (not . (`elem` hyp)) cs

mkPts                    :: [Coord] -> [Point]
mkPts coords             =  [(x,y) | [x,y] <- groupsOf 2 coords]

groupsOf _ []            =  []     
groupsOf n xs            =  take n xs : groupsOf n (drop n xs)

uniq                     :: (Ord a) => [a] -> [a]
uniq                     =  map head . group . sort

none                     =  (not.) . any

-- elementery geometric methods 

ptInRect                 :: Point -> Rect -> Bool
ptInRect p rect@(c:cs)   =  length ccwGroups == 1
    where
    ccwGroups            =  group $ zipWith (flip ccw p) rect (cs ++ [c])

diagonals                :: Rect -> [Line]
diagonals [a,b,c,d]      =  [(a,c),(b,d)]

-- cuts is stronger than isect: a line segment "cuts" another when it
-- intersects the other *and* they don't share a single endpoint

cuts l1@(a,b) l2@(u,v)   =  isect l1 l2 && numShared /= 1
    where
    numShared            =  length . filter (`elem`[a,b]) $ [u,v]

-- the following two are based on Sedgewick's "Algorithms in C", 1990

isect                    :: Line -> Line -> Bool
isect (a,b) (u,v)        =  ccw a b u * ccw a b v <= 0
                            && ccw u v a * ccw u v b <= 0

ccw                      :: Point -> Point -> Point -> Int
ccw p0 p1 p2
    | dx1*dy2 > dy1*dx2  =  1
    | dx1*dy2 < dy1*dx2  = -1
    | dx1*dx2 < 0        = -1
    | dy1*dy2 < 0        = -1
    | dx1*dx1+dy1*dy1 
      < dx2*dx2+dy2*dy2  =  1
    | otherwise          =  0
    where
    (dx1, dy1)           =  vec p0 p1
    (dx2, dy2)           =  vec p1 p2

-- DIAGNOSTICS: extra code to generate Mathematica graphics of solutions

diagnostic s = unsafePerformIO $ hPutStrLn stderr $ mkMmaGraphic s

mkMmaGraphic             :: Scenario -> String
mkMmaGraphic scn@(Scenario s f bs)
                         =  "Graphics[{AbsolutePointSize[4]," 
                            ++ scnStr ++ "," ++ solnStr ++ "}]"
    where
    scnStr               =  mmaList $ concat [map mmaPt [s,f], map mmaPoly bs]
    solnStr              =  mmaList [ "RGBColor[1,0,0]"
                                    , "AbsoluteThickness[2]"
                                    , mmaLine solnPts
                                    , mmaList $ map mmaPt solnPts
                                    ]
    solnPts              =  map (grPts !!) $ sp 0 1 (mkGrph scn)
    grPts                =  s : f : filter (`notElem`[s,f]) nonInteriorBldgPts
    bldgDiags            =  concatMap diagonals bs
    nonInteriorBldgPts   =  [p | p <- uniq (concat bs), none (ptInRect p) bs]

mmaCoords (x,y)          =  "{" ++ show x ++ "," ++ show y ++ "}"
mmaPt p                  =  "Point[" ++ mmaCoords p ++ "]"
mmaPoly cs               =  "{GrayLevel[.5],Polygon[" 
                            ++ mmaList (map mmaCoords cs) ++ "]}"
mmaList ss               =  "{" ++ concat (intersperse "," ss) ++ "}"
mmaLine ps               =  "Line[" ++ mmaList (map mmaCoords ps) ++ "]"
