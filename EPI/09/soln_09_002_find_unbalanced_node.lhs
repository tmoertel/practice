Solution to "Find k-unbalanced node problem", 9.2 in EPI.

The problem, paraphrased from problem 9.2 of _Elements
of Programming _Interviews_, v. 1.3.1, is as follows:

    Let a tree node be considered "k-balanced" iff the number of left
    children differs from the number of right children by at most k.
    Given a tree, find a node within it that is not k-balanced but its
    children are.  If such a node exists, return its label; otherwise,
    return Nothing.

Discussion.

First, this solution is a Literate Haskell program, living in the
following module:

> {-# LANGUAGE BangPatterns #-}
>
> module Soln where

Now, let us define a binary tree as either

    Empty

or given by a root node

    Node x l r

where x is the node's label and l and r are the tree's left and right
subtrees, respectively.  In Haskell, one way to define such a tree is
as the (least) fixed point of the following term functor:

> data TreeF a x = Empty | Node a x x deriving Show

In this definition, 'a' is the type of node labels and 'x' is the type
of the underlying carrier.

We can interpret 'TreeF a' as an endofunctor in Hask (the category of
Haskell types) that lifts some underlying carrier type to binary-tree
terms over that carrier.  Here is the corresponding functor instance:

> instance Functor (TreeF a) where
>   fmap _ Empty        = Empty
>   fmap f (Node x l r) = Node x (f l) (f r)

To create actual binary trees from the terms, we must allow the terms
to recursively carry other terms.  To do this, we introduce the
standard 'Fix' newtype, which lets us find the (least) fixed point of
some underlying functor 'f':

> newtype Fix f = Fix { unFix :: f (Fix f) }

Now we can define our data type of binary trees as the fixed point of
tree-functor terms:

> type Tree a = Fix (TreeF a)

Now let's create some binary trees.  We'll start by defining smart
constructors to reduce the syntactic 'Fix' overhead of creating trees:

> empty :: Tree a
> empty = Fix Empty
>
> node :: a -> Tree a -> Tree a -> Tree a
> node x l r = Fix $ Node x l r

Now, let's make a tree containing a single node labeled with 1:

> oneTree = node 1 empty empty

And here's a two-node tree.  Its root is labeled 0, its left subtree
is empty, and its right subtree is the single-node tree we defined
earlier:

> unbalTree = node 0 empty oneTree

Note that this tree's root node is not 0-balanced: its left subtree is
empty, but its right subtree contains 1 node.  Later, we will test
whether our solution correctly identifies node 0 as 0-unabalanced.

Now, back to the original problem.

With this representation of binary trees established, we can now
return to finding a k-unbalanced node whose children are k-balanced.
To simplify the problem, let's break it into three pieces.

First, as a warm-up, we'll solve a simpler problem: computing the size
of a tree by counting its nodes.  We'll use integers for node counts:

> type NodeCount = Int

And we'll create a function to convert a term into its size:

> termSize (Empty)                       = 0
> termSize (Node _ !leftSize !rightSize) = 1 + leftSize + rightSize

Basically, an 'Empty' term has a size of 0 and a 'Node' term has a
size of 1 plus the sum of the sizes of its left and right subtrees.
Note that the size of a term can be computed in constant time.

The algebraically inclined reader will note that 'termSize' represents
an F-algebra having the carrier type 'NodeCount'.  An F-algebra
reduces some term functor 'f' over an underlying carrier type 'a' into
a single summary value of the carrier type:

> type Algebra f a = f a -> a

Thus 'termSize' is an F-algebra from tree terms to node counts:

> termSize :: Algebra (TreeF a) NodeCount

Applying this algebra from the bottom up, we can compute the size of
an arbitrary tree in linear time -- constant time per node.

But this bottom-up pattern doesn't just work for trees. We can capture
it for all recursive data types with the concept of a catamorphism.
Basically, a catamorphism applies an F-algebra to a recursive data
structure to crush the structure into a single summary value.  The
concept works for all recursive data types that we can represent as
fixed points of term functors.  For these types, 'Fix' is a
structure-preserving initial algebra.  (We'll see why this algebra is
important in a moment.)  For binary trees, for example, we take 'Fix'
"at" the 'TreeF a' type:

> treeInitialAlg :: Algebra (TreeF a) (Tree a)
> treeInitialAlg = Fix

Because this algebra is initial (in the category of F-algebras), there
is a unique homomorphism from it to each F-algebra 'alg' having the
same term functor.  This unique homomorphism is the F-algebra's
corresponding catamorphism, 'cata alg'.  For all such F-algebras, it
has the same formulation:

> cata :: Functor f => Algebra f a -> Fix f -> a
> cata alg = alg . fmap (cata alg) . unFix

In other words, this one formula lets us crush *any* recursive data
structure (derived from a term functor) into a single value.  All we
need is a suitable algebra, and the rest follows automatically.

This machinery is all very abstract, but its use is straightforward.
To return to our task, for example, the function we seek to compute
the size of an arbitrary tree is merely the catamorphism for the
'termSize' algebra:

> treeSize :: Tree a -> NodeCount
> treeSize = cata termSize

A few trial runs:

    >>> treeSize empty
    0

    >>> treeSize oneTree
    1

    >>> treeSize unbalTree
    2

Now let us move on to our second warm-up.  We will augment our
'termSize' algebra to also determine whether a term is k-balanced.
We'll do this by computing a "balance summary," which will combine a
boolean value indicating k-balancedness with a node count:

> type BalanceSummary = (Bool, NodeCount)
>
> termBalance :: Int -> Algebra (TreeF a) BalanceSummary
> termBalance _ Empty          = (True, 0)
> termBalance k term@(Node{})  = (isBal, size) where
>   !isBal = abs (leftSize - rightSize) <= k
>   !size  = termSize sizeTerm
>   sizeTerm@(Node _ leftSize rightSize) = fmap snd term

Let's take our new algebra for a spin with k = 0:

    >>> cata (termBalance 0) empty
    (True,0)

    >>> cata (termBalance 0) oneTree
    (True,1)

    >>> cata (termBalance 0) unbalTree
    (False,2)

Recall that 'unbalTree' has two nodes and is not 0-balanced.

As our pentultimate step, we will create a slightly more ambitious
algebra to search for k-unbalanced nodes having balanced children.
The result of a search is either negative, indicating that we haven't
(yet) found a node that meets our search criteria, or positive,
indicating that we have.  In the negative case, we will return a
'BalanceSummary'; it will be useful in continuing the search upward
into the tree.  In the positive case, we will return the matching
node's label directly.  Thus a search result over a tree having labels
of type 'a' has the following type:

> data BalanceSearchResult a = Neg !BalanceSummary
>                            | Pos !a

Putting it all together gives us the following search algebra:

> termKunbSearch :: Int -> Algebra (TreeF a) (BalanceSearchResult a)
> termKunbSearch k Empty = Neg (True, 0)  -- trivially balanced
> termKunbSearch k term@(Node x l r)
>   -- if we already found a matching node below, return it directly
>   | Pos _ <- l = l
>   | Pos _ <- r = r
>   -- otherwise, examine this node
>   | otherwise = case (l, r) of
>       (Neg (leftBal, leftSize), Neg (rightBal, rightSize))
>         | not isBal && leftBal && rightBal -> Pos x  -- found match!
>         | otherwise                        -> Neg (isBal, size) where
>             !isBal = abs (leftSize - rightSize) <= k
>             !size  = 1 + leftSize + rightSize

Finally, we can use the catamorphism for this algebra to solve the
original problem:

> findUnbalancedNode :: Int -> Tree label -> Maybe label
> findUnbalancedNode k tree = case cata (termKunbSearch k) tree of
>   Neg _     -> Nothing      -- found no matching node
>   Pos label -> Just label   -- found a match

To test our solution, a few simple cases:

    >>> findUnbalancedNode 0 empty  -- empty tree has no unbalanced nodes
    Nothing

    >>> findUnbalancedNode 0 unbalTree  -- the root node is 0-unbalanced
    Just 0

    >>> findUnbalancedNode 1 unbalTree  -- but no node is 1-unbalanced
    Nothing
