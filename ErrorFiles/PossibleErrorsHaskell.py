def getExampleErrorMessagesHaskell01():
    msg = """TemplateTest.hs: Template.hs:(29,1)-(31,39): Non-exhaustive patterns in function insert


Template.hs:25:7: error:
    * Couldn't match expected type `Move -> Bool'
                  with actual type `Move'
    * The operator `beat' takes two arguments,
      but its type `Move -> Move' has only one
      In the expression: x `beat` y
      In a stmt of a pattern guard for
                     an equation for `outcome':
        x `beat` y

Template.hs:26:7: error:
    * Couldn't match expected type `Move -> Bool'
                  with actual type `Move'
    * The operator `lose' takes two arguments,
      but its type `Move -> Move' has only one
      In the expression: x `lose` y
      In a stmt of a pattern guard for
                     an equation for `outcome':
        x `lose` y

Template.hs:25:7: error:
    * Couldn't match expected type `Move -> Bool'
                  with actual type `Move'
    * The operator `beat' takes two arguments,
      but its type `Move -> Move' has only one
      In the expression: x `beat` y
      In a stmt of a pattern guard for
                     an equation for `outcome':
        x `beat` y

Template.hs:26:7: error:
    * Couldn't match expected type `Move -> Bool'
                  with actual type `Move'
    * The operator `lose' takes two arguments,
      but its type `Move -> Move' has only one
      In the expression: x `lose` y
      In a stmt of a pattern guard for
                     an equation for `outcome':
        x `lose` y

TemplateTest.hs:145:28: error:
    Variable not in scope: flatten :: [a3] -> a3

TemplateTest.hs:151:21: error:
    Variable not in scope: flatten :: [t1] -> [t0]

TemplateTest.hs:159:31: error:
    Variable not in scope: flatten :: [[a2]] -> [a2]

TemplateTest.hs:166:37: error:
    Variable not in scope: flatten :: [[a1]] -> [a0]

TemplateTest.hs:166:52: error:
    Variable not in scope: flatten :: [[a1]] -> [a0]

TemplateTest.hs:172:21: error:
    Variable not in scope: flatten :: [[Integer]] -> [Integer]

TemplateTest.hs:145:28: error:
    Variable not in scope: flatten :: [a3] -> a3

TemplateTest.hs:151:21: error:
    Variable not in scope: flatten :: [t1] -> [t0]

TemplateTest.hs:159:31: error:
    Variable not in scope: flatten :: [[a2]] -> [a2]

TemplateTest.hs:166:37: error:
    Variable not in scope: flatten :: [[a1]] -> [a0]

TemplateTest.hs:166:52: error:
    Variable not in scope: flatten :: [[a1]] -> [a0]

TemplateTest.hs:172:21: error:
    Variable not in scope: flatten :: [[Integer]] -> [Integer]

Template.hs:8:14:
    Couldn't match expected type `[b]' with actual type `t0 a -> [t1]'
    Relevant bindings include
      y :: [a] (bound at Template.hs:8:9)
      x :: a -> b (bound at Template.hs:8:7)
      mapLC :: (a -> b) -> [a] -> [b] (bound at Template.hs:8:1)
    Probable cause: `foldr' is applied to too few arguments
    In the expression: foldr x []
    In an equation for `mapLC': mapLC x y = foldr x []

Template.hs:8:20:
    Couldn't match type `b' with `[b] -> [b]'
      `b' is a rigid type variable bound by
          the type signature for mapLC :: (a -> b) -> [a] -> [b]
          at Template.hs:7:10
    Expected type: a -> [b] -> [b]
      Actual type: a -> b
    Relevant bindings include
      x :: a -> b (bound at Template.hs:8:7)
      mapLC :: (a -> b) -> [a] -> [b] (bound at Template.hs:8:1)
    In the first argument of `foldr', namely `x'
    In the expression: foldr x [] y

Template.hs:13:1:
    Equations for `filterLC' have different numbers of arguments
      Template.hs:13:1-16
      Template.hs:(14,1)-(16,39)

Template.hs:20:32:
    Not in scope: data constructor `Eq'
    Perhaps you meant `EQ' (imported from Prelude)

Template.hs:20:43:
    Not in scope: data constructor `Eq'
    Perhaps you meant `EQ' (imported from Prelude)

Template.hs:21:30:
    Not in scope: data constructor `Eq'
    Perhaps you meant `EQ' (imported from Prelude)

Template.hs:21:41:
    Not in scope: data constructor `Eq'
    Perhaps you meant `EQ' (imported from Prelude)

Template.hs:20:32:
    Couldn't match expected type `Exp -> Exp -> Bool'
                with actual type `Ordering'
    The function `EQ' is applied to two arguments,
    but its type `Ordering' has none
    In the first argument of `(&&)', namely `EQ x x1'
    In the expression: EQ x x1 && EQ y y1

Template.hs:20:43:
    Couldn't match expected type `Exp -> Exp -> Bool'
                with actual type `Ordering'
    The function `EQ' is applied to two arguments,
    but its type `Ordering' has none
    In the second argument of `(&&)', namely `EQ y y1'
    In the expression: EQ x x1 && EQ y y1

Template.hs:21:30:
    Couldn't match expected type `Exp -> Exp -> Bool'
                with actual type `Ordering'
    The function `EQ' is applied to two arguments,
    but its type `Ordering' has none
    In the first argument of `(&&)', namely `EQ x x1'
    In the expression: EQ x x1 && EQ y y1

Template.hs:21:41:
    Couldn't match expected type `Exp -> Exp -> Bool'
                with actual type `Ordering'
    The function `EQ' is applied to two arguments,
    but its type `Ordering' has none
    In the second argument of `(&&)', namely `EQ y y1'
    In the expression: EQ x x1 && EQ y y1

Template.hs:34:42:
    No instance for (Num String) arising from a use of `+\'
    In the expression: "And " + show x + " " + show y
    In an equation for `show\':
        show (And x y) = "And " + show x + " " + show y
    In the instance declaration for `Show Exp\'

Template.hs:34:30:
    Couldn\'t match type `[Char]\' with `Char\'
    Expected type: Char
      Actual type: String
    In the first argument of `(:)\', namely `show x\'
    In the second argument of `(++)\', namely `show x : " " ++ show y\'
TemplateTest.hs: Template.hs:(34,3)-(35,51): Non-exhaustive patterns in function show

TemplateTest.hs: Template.hs:(34,3)-(35,50): Non-exhaustive patterns in function show


Template.hs:51:3: Warning:
    Pattern match(es) are overlapped
    In an equation for `eval': eval _ = ...

Template.hs:51:3: Warning:
    Pattern match(es) are overlapped
    In an equation for `eval': eval _ = ...

Template.hs:19:15: Not in scope: `a'

Template.hs:20:15:
    Couldn't match expected type `String -> String'
                with actual type `[Char -> Char]'
    Possible cause: `map' is applied to too many arguments
    In the expression: map shift x
    In an equation for `encode': encode x = map shift x

Template.hs:20:25:
    Couldn't match expected type `[Int]' with actual type `Int'
    In the second argument of `map', namely `x'
    In the expression: map shift x
    """
    return msg
def getExampleErrorMessagesHaskell02():
    msg = """Template.hs:50:1:
    The type signature for `stringToGender'
      lacks an accompanying binding

TemplateTest.hs:14:1:
    Can't make a derived instance of `Bounded Move':
      `Move' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
        or
      `Move' must have precisely one constructor
    In the stand-alone deriving instance for `Bounded Move'

TemplateTest.hs:15:1:
    Can't make a derived instance of `Enum Move':
      `Move' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
    In the stand-alone deriving instance for `Enum Move'

TemplateTest.hs:20:1:
    Can't make a derived instance of `Bounded Result':
      `Result' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
        or
      `Result' must have precisely one constructor
    In the stand-alone deriving instance for `Bounded Result'

TemplateTest.hs:21:1:
    Can't make a derived instance of `Enum Result':
      `Result' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
    In the stand-alone deriving instance for `Enum Result'

TemplateTest.hs:14:1:
    Can't make a derived instance of `Bounded Move':
      `Move' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
        or
      `Move' must have precisely one constructor
    In the stand-alone deriving instance for `Bounded Move'

TemplateTest.hs:15:1:
    Can't make a derived instance of `Enum Move':
      `Move' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
    In the stand-alone deriving instance for `Enum Move'

TemplateTest.hs:21:1:
    Can't make a derived instance of `Enum Result':
      `Result' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
    In the stand-alone deriving instance for `Enum Result'

Template.hs:20:18:
    Couldn\'t match expected type `Move\' with actual type `[Char]\'
    In the expression: "Paper"
    In an equation for `beat\':
        beat (GetMove x)
          | x == "Rock" = "Paper"
          | x == "Paper" = "Scissors"
          | x == "Scissors" = "Rock"

Template.hs:21:19:
    Couldn\'t match expected type `Move\' with actual type `[Char]\'
    In the expression: "Scissors"
    In an equation for `beat\':
        beat (GetMove x)
          | x == "Rock" = "Paper"
          | x == "Paper" = "Scissors"
          | x == "Scissors" = "Rock"

Template.hs:22:22:
    Couldn\'t match expected type `Move\' with actual type `[Char]\'
    In the expression: "Rock"
    In an equation for `beat\':
        beat (GetMove x)
          | x == "Rock" = "Paper"
          | x == "Paper" = "Scissors"
          | x == "Scissors" = "Rock"

Template.hs:26:18:
    Couldn\'t match expected type `Move\' with actual type `[Char]\'
    In the expression: "Scissors"
    In an equation for `lose\':
        lose (GetMove x)
          | x == "Rock" = "Scissors"
          | x == "Paper" = "Rock"
          | x == "Scissors" = "Paper"

Template.hs:27:19:
    Couldn\'t match expected type `Move\' with actual type `[Char]\'
    In the expression: "Rock"
    In an equation for `lose\':
        lose (GetMove x)
          | x == "Rock" = "Scissors"
          | x == "Paper" = "Rock"
          | x == "Scissors" = "Paper"

Template.hs:28:22:
    Couldn\'t match expected type `Move\' with actual type `[Char]\'
    In the expression: "Paper"
    In an equation for `lose\':
        lose (GetMove x)
          | x == "Rock" = "Scissors"
          | x == "Paper" = "Rock"
          | x == "Scissors" = "Paper"

TemplateTest.hs:15:1:
    Can't make a derived instance of `Enum Move':
      `Move' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
    In the stand-alone deriving instance for `Enum Move'

TemplateTest.hs:21:1:
    Can't make a derived instance of `Enum Result':
      `Result' must be an enumeration type
      (an enumeration consists of one or more nullary, non-GADT constructors)
    In the stand-alone deriving instance for `Enum Result'

Template.hs:15:1:
    parse error (possibly incorrect indentation or mismatched brackets)

Template.hs:15:24:
    Couldn't match expected type `Bool' with actual type `MyBool'
    In the expression: MyTrue
    In an equation for `==': (==) MyTrue MyTrue = MyTrue

Template.hs:16:26:
    Couldn't match expected type `Bool' with actual type `MyBool'
    In the expression: MyTrue
    In an equation for `==': (==) MyFalse MyFalse = MyTrue

Template.hs:17:14:
    Couldn't match expected type `Bool' with actual type `MyBool'
    In the expression: MyFalse
    In an equation for `==': (==) _ _ = MyFalse

Template.hs:20:3:
    Equations for `==' have different numbers of arguments
      Template.hs:20:3-47
      Template.hs:21:3-49
    In the instance declaration for `Eq Exp'

Template.hs:34:3:
    Equations for `show' have different numbers of arguments
      Template.hs:34:3-29
      Template.hs:35:3-47
    In the instance declaration for `Show Exp'

Template.hs:50:3:
    Equations for `eval' have different numbers of arguments
      Template.hs:50:3-37
      Template.hs:52:3-23
    In the instance declaration for `Evaluatable Exp'

Template.hs:15:24:
    Couldn't match expected type `Bool' with actual type `MyBool'
    In the expression: MyTrue
    In an equation for `==': (==) MyTrue MyTrue = MyTrue

Template.hs:16:26:
    Couldn't match expected type `Bool' with actual type `MyBool'
    In the expression: MyTrue
    In an equation for `==': (==) MyFalse MyFalse = MyTrue

Template.hs:17:14:
    Couldn't match expected type `Bool' with actual type `MyBool'
    In the expression: MyFalse
    In an equation for `==': (==) _ _ = MyFalse

Template.hs:23:14:
    Couldn't match expected type `Bool' with actual type `MyBool'
    In the expression: MyFalse
    In an equation for `==': (==) _ _ = MyFalse

Template.hs:5:5:
    Not in scope: `replicateM_'
    Perhaps you meant `replicate' (imported from Prelude)

Template.hs:11:5:
    Not in scope: `replicateM_'
    Perhaps you meant `replicate' (imported from Prelude)

Template.hs:23:11: Not in scope: `join'

Template.hs:23:18: Not in scope: `liftM'

Template.hs:24:5:
    No instance for (Read a0) arising from a use of `readLn'
    The type variable `a0' is ambiguous
    Note: there are several potential instances:
      instance (GHC.Arr.Ix a, Read a, Read b) => Read (GHC.Arr.Array a b)
        -- Defined in `GHC.Read'
      instance Read a => Read (Maybe a) -- Defined in `GHC.Read'
      instance (Integral a, Read a) => Read (GHC.Real.Ratio a)
        -- Defined in `GHC.Read'
      ...plus 25 others
    In the first argument of `(>>=)', namely `readLn'
    In the expression:
      readLn
      >>=
        \\ s
          -> case s of {
               [] -> return ()
               _ -> do { ... } }
    In an equation for `prog2':
        prog2
          = readLn
            >>=
              \\ s
                -> case s of {
                     [] -> return ()
                     _ -> ... }

Template.hs:28:13:
    No instance for (Show a0) arising from a use of `print'
    The type variable `a0' is ambiguous
    Relevant bindings include s :: [a0] (bound at Template.hs:24:17)
    Note: there are several potential instances:
      instance (GHC.Arr.Ix a, Show a, Show b) => Show (GHC.Arr.Array a b)
        -- Defined in `GHC.Arr'
      instance Show a => Show (Maybe a) -- Defined in `GHC.Show'
      instance (Integral a, Show a) => Show (GHC.Real.Ratio a)
        -- Defined in `GHC.Real'
      ...plus 26 others
    In a stmt of a 'do' block: print (reverse s)
    In the expression:
      do { print (reverse s);
           prog2 }
    In a case alternative:
        _ -> do { print (reverse s);
                  prog2 }

Template.hs:24:29: parse error on input `\\'

Template.hs:40:5: parse error on input `end'"""

