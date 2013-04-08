{-# LANGUAGE ScopedTypeVariables #-}
{-

Solution to maze problem presented in http://neil.fraser.name/news/2013/03/16/.

Tom Moertel <tom@moertel.com>
2012-03-26

-}

module Main where

import Control.Applicative
import Control.Monad.State
import Data.Array
import Data.Char (chr, ord)
import Data.List (group, sort)
import qualified Data.Map as M
import qualified Data.Set as S



type CellLoc  = (Int, Int)       -- ^ (row, col)
type GraphLoc = (Int, Int, Int)  -- ^ (row, col, half) where half in [0, 1]

data Cell = TRBL -- ^ splits cell into top-right/bottom-left halves
          | TLBR -- ^ splits cell into top-left/bottom-right halves
          deriving (Eq, Ord, Show)

data AreaSet = OpenSet             -- ^ open to the outside
             | ClosedSet GraphLoc  -- ^ not known to be open to the outside
             deriving (Eq, Ord, Show)

data Solution = Solution { solnClosedCount   :: Int
                         , solnMaxClosedArea :: Int
                         , solnAreas         :: GraphSets
                         }
                deriving Show

type Neighbors = [GraphLoc]

newtype Maze      = Maze      (Array CellLoc Cell) deriving Show
newtype MazeGraph = MazeGraph (M.Map GraphLoc Neighbors) deriving Show

type GraphSets = M.Map GraphLoc AreaSet


main :: IO ()
main = interact $ \input ->
  let maze = readMaze input
      soln = solve maze
  in showSoln maze soln


readMaze :: String -> Maze
readMaze s = Maze . listArray ((0, 0), (nrows - 1, ncols - 1)) $ cells
  where
    rows  = lines s
    nrows = length rows
    ncols = case rows of [] -> 0; l:ls -> length l
    cells = map parseCell (concat rows)


parseCell :: Char -> Cell
parseCell '0'  = TRBL
parseCell '1'  = TLBR
parseCell '\\' = TRBL
parseCell '/'  = TLBR
parseCell c    = error $ "bad cell spec " ++ [c]


solve :: Maze -> Solution
solve maze = extractSolution (unionConnectedSets graph sets)
  where
    graph = cellGraph maze
    sets  = graphSets graph


cellGraph :: Maze -> MazeGraph
cellGraph (Maze maze) = MazeGraph . M.fromListWith (++) $ elists
  where
    elists = concat . flip map (assocs maze) $ \((r, c), slash) ->
      let toplink = ((r, c, 0), [(r - 1, c, 1)])
          botlink = ((r, c, 1), [(r + 1, c, 0)])
          leftlink = case (slash, c == 0, maze ! (r, c - 1)) of
            (TLBR, True, _) -> ((r, c, 0), [(r, c - 1, 0)])
            (TLBR, _, TRBL) -> ((r, c, 0), [(r, c - 1, 0)])
            (TLBR, _, TLBR) -> ((r, c, 0), [(r, c - 1, 1)])
            (TRBL, True, _) -> ((r, c, 1), [(r, c - 1, 0)])
            (TRBL, _, TRBL) -> ((r, c, 1), [(r, c - 1, 0)])
            (TRBL, _, TLBR) -> ((r, c, 1), [(r, c - 1, 1)])
          rightlink = case (slash, c == cmax, maze ! (r, c + 1)) of
            (TLBR, True, _) -> ((r, c, 1), [(r, c + 1, 1)])
            (TLBR, _, TRBL) -> ((r, c, 1), [(r, c + 1, 1)])
            (TLBR, _, TLBR) -> ((r, c, 1), [(r, c + 1, 0)])
            (TRBL, True, _) -> ((r, c, 0), [(r, c + 1, 1)])
            (TRBL, _, TRBL) -> ((r, c, 0), [(r, c + 1, 1)])
            (TRBL, _, TLBR) -> ((r, c, 0), [(r, c + 1, 0)])
      in [toplink, botlink, leftlink, rightlink]
    (_, (rmax, cmax)) = bounds maze


graphSets :: MazeGraph -> GraphSets
graphSets (MazeGraph gr) = M.mapWithKey mkSet gr
  where
    mkSet v es = if any (`M.notMember` gr) es then OpenSet else ClosedSet v


unionConnectedSets :: MazeGraph -> GraphSets -> GraphSets
unionConnectedSets (MazeGraph gr) sets = M.foldlWithKey unionNeighbors sets gr
  where
    unionNeighbors sets v es = foldl (union v) sets es
    union v sets u = execState (unionM v u) sets
    unionM :: GraphLoc -> GraphLoc -> State GraphSets ()
    unionM v u = do vrep <- rep v
                    urep <- rep u
                    case (vrep, urep) of
                      (OpenSet, ClosedSet u') -> modify $ M.insert u' vrep
                      (ClosedSet v', _)       -> modify $ M.insert v' urep
                      _                       -> return ()

-- | Given an element, find the representative element of the set containing it
rep :: GraphLoc -> State GraphSets AreaSet
rep v = do
  sets <- get
  case M.lookup v sets of
    Just OpenSet                     -> return OpenSet
    Just s@(ClosedSet u) | u == v    -> return s
                         | otherwise -> do r <- rep u
                                           put $ M.insert v r sets
                                           return r
    _                                -> return OpenSet


extractSolution :: GraphSets -> Solution
extractSolution sets = Solution closedCount maxClosedArea areaReps
  where
    reps = evalState (mapM rep $ M.keys sets) sets
    areas = M.fromListWith (+) [(rep, 1) | (ClosedSet rep) <- reps]
    closedCount = M.size areas
    maxClosedArea = maximum (0 : M.elems areas) `div` 2  -- units are 1/2 cell
    areaReps = M.fromList (zip (M.keys sets) reps)


viz :: Solution -> Maze -> String
viz Solution{solnAreas = areaReps} (Maze maze) = unlines $
  concat . flip map [0..rmax] $ \r ->
  flip map [0..1] $ \topbot ->
  concat . flip map [0..cmax] $ \c ->
  let loc = (r, c, topbot)
      Just areaName = (`M.lookup` areaNames) =<< M.lookup loc areaReps
      label = sym areaName
  in case (topbot, maze ! (r, c)) of
            (0, TLBR) -> label ++ "/"
            (0, TRBL) -> "\\" ++ label
            (1, TLBR) -> "/" ++ label
            (1, TRBL) -> label ++ "\\"
            _         -> error "bogus map"
  where
    (_, (rmax, cmax)) = bounds maze
    areaNames = M.fromList $
                zip (S.toList . S.fromList $ M.elems areaReps) [0..]

sym :: Int -> [Char]
sym n = if inRange (bounds lut) n then lut ! n else "*"
  where
    syms = [[c] | i <- [32..126], let c = chr i, c `notElem` "*/\\"]
    lut  = listArray (0, length syms - 1) syms


showSoln :: Maze -> Solution -> String
showSoln maze soln = unlines ls
  where
    ls = [ "count of closed areas        = " ++ show (solnClosedCount soln)
         , "size of maximum closed area  = " ++ show (solnMaxClosedArea soln)
         , "\nvisualization:\n"
         , viz soln maze
         ]


testMaze :: Maze
testMaze = readMaze testMazeSpec


testMazeSpec :: String
testMazeSpec = unlines $
       [ "\\//\\\\/"
       , "\\///\\\\"
       , "//\\\\/\\"
       , "\\/\\///"
       ]
