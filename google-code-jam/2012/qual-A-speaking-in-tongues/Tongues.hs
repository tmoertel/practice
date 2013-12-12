{-

Solution to Google Code Jam problem "Speaking In Tongues"
http://code.google.com/codejam/contest/1460488/dashboard

Tom Moertel <tom@moertel.com>
Thu Dec 12 15:48:52 EST 2013


Discussion.

The trick here is that the problem description actually gives you,
hidden in plain sight within the examples, the translation table
between "Googlerese" and English.  Only one character's translation is
absent, and this we can find by mapping the missing character on the
input side of the table to the missing character on the output side.
The translation table complete, applying it to the input lines
solves the problem handily.

-}

module Main where

import           Control.Arrow ((***))
import qualified Data.Map as M
import           Data.Maybe (fromMaybe)
import qualified Data.Set as S

type TranslationTable = M.Map Char Char

main :: IO ()
main = interact $ unlines . zipWith showN [1..] . map decode . tail . lines

showN :: Int -> String -> String
showN n ans = "Case #" ++ show n ++ ": " ++ ans

decode :: String -> String
decode = map decodeChar

decodeChar :: Char -> Char
decodeChar c = fromMaybe (error $ "No match for " ++ [c]) $
               M.lookup c translations

translations :: TranslationTable
translations = addMissingPair $ M.fromList (zip googrtext plaintext)

addMissingPair :: TranslationTable -> TranslationTable
addMissingPair table = M.insert k v table where
  [(k, v)] = uncurry zip . (missing *** missing) . unzip . M.toList $ table

missing :: String -> String
missing = S.toList . (letters S.\\) . S.fromList

letters :: S.Set Char
letters = S.fromAscList ['a'..'z']

-- The problem description helpfully provides the following
-- translations, from which we can deduce most of the translation
-- table.  Only one letter's mapping is missing.
googrtext, plaintext :: String
googrtext = concat [
    "yeq"
  , "ejp mysljylc kd kxveddknmc re jsicpdrysi"
  , "rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd"
  , "de kr kd eoya kw aej tysr re ujdr lkgc jv"
  ]

plaintext = concat [
    "aoz"
  , "our language is impossible to understand"
  , "there are twenty six factorial possibilities"
  , "so it is okay if you want to just give up"
  ]
