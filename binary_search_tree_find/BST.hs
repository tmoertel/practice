{- Tom Moertel <tom@moertel.org> 2012-01-24 -}

module BST where

data BST a = Empty | Node a (BST a) (BST a) deriving (Eq, Show)

t0 = Empty
t1 = Node 1 Empty Empty
t3 = Node 2 (Node 1 Empty Empty) (Node 3 Empty Empty)

traverse
  :: ((b -> b) -> (b -> b) -> (b -> b) -> b -> b)
     -> (a -> b -> b)
     -> b
     -> BST a
     -> b
traverse app f z tree = go tree z
  where
    go Empty        z = z
    go (Node v l r) z = app (f v) (go l) (go r) z

preorder   = traverse $ \n l r -> r . l . n
inorder    = traverse $ \n l r -> r . n . l
postorder  = traverse $ \n l r -> n . r . l

flatten traversal = reverse . traversal (:) []

size = preorder (\_ z -> z + 1) 0

treemin z = traverse appl min z
  where
    appl n l r = l . n

treemax z = traverse appr max z
  where
    appr n l r = r . n

test1 = flatten inorder t3          -- [1,2,3]
test2 = size t3                     -- 3
test3 = treemin maxBound t3 :: Int  -- 1
test4 = treemax minBound t3 :: Int  -- 3
