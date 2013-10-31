module Soln where

newtype Fix f = Fix { unFix :: f (Fix f) }

data TreeF a b = Empty | Node a b b deriving Show

instance Functor (TreeF a) where
  fmap _ Empty        = Empty
  fmap f (Node x l r) = Node x (f l) (f r)

-- tree with node labels of type a
type Tree a = Fix (TreeF a)

-- some sample trees
emptyTree = Fix Empty
oneTree   = Fix $ Node 1 (Fix Empty) (Fix Empty)
unbalTree = Fix $ Node 0 (Fix Empty) oneTree

-- catamorphism crushes a recursive data struct into a val using an algebra
cata f = f . fmap (cata f) . unFix

-- Now we construct an algebra that solves the following problem:
-- Let a tree node be considered "k balanced" iff the number of left
-- children differs from the number of right children by at most k.
-- Given a tree, find a node within it that is not k balanced but
-- its children are.  If such a node exists, return its label;
-- otherwise, return Nothing.
type BalanceSummary = (Bool, Int)
type KunbCarrier a = Either BalanceSummary a

kunbAlg :: Int -> TreeF a (KunbCarrier a) -> KunbCarrier a
kunbAlg k = go where
  go Empty = Left (True, 0)  -- empty trees are balanced (trivially)
  go (Node x l r)
     -- if we already found an unbalanced node below, return it
     | Right _ <- l = l
     | Right _ <- r = r
     -- otherwise, examine this node
     | otherwise = case (l, r) of
         (Left (lp, lc), Left (rp, rc))
           | not np && lp && rp -> Right x  -- this node meets all criteria!
           | otherwise          -> Left (np, 1 + lc + rc)
           where np = abs (lc - rc) <= k

findUnbalancedNode :: Int -> Tree label -> Maybe label
findUnbalancedNode k tree = case cata (kunbAlg k) tree of
  Left _      -> Nothing
  Right label -> Just label



{- scratch space -}


-- generic algebra for tree functor
alg :: t -> (a -> b -> b -> t) -> TreeF a b -> t
alg c _ Empty        = c
alg _ f (Node x l r) = f x l r

treeMapAlg :: (a -> a') -> TreeF a (Tree a') -> Tree a'
treeMapAlg _ Empty        = Fix Empty
treeMapAlg f (Node x l r) = Fix $ Node (f x) l r

treeMap :: (a -> a') -> Tree a -> Tree a'
treeMap f = cata (treeMapAlg f)

treeTriAlg :: (a -> a) -> TreeF a (Tree a) -> Tree a
treeTriAlg _ Empty        = Fix Empty
treeTriAlg f (Node x l r) = Fix $ Node x (h l) (h r) where h = treeMap f

treeTri :: (a -> a) -> Tree a -> Tree a
treeTri f = cata (treeTriAlg f)

depths :: Tree a -> Tree Int
depths = treeTri succ . treeMap (const 0)

pprint :: Show a => Tree a -> String
pprint = cata f where
  f Empty        = "*"
  f (Node x l r) = "(" ++ show x ++ " " ++ l ++ " " ++ r ++ ")"
