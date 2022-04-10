# What is the point of using jqwik's data generators? #
We could just use random value generation whenever needed. 

There are a few main benefits when using data generators:
- The results are **reproducible** so you can figure out exactly which values caused the test failure, or simply re-do it after making some changes. jqwik will automatically use the random number seed associated with the last time that the test property failed. You could keep track of these random number seeds yourself but this introduces human error.
- **Shrinking** of test values can be done, which reduces the inputs to a minimum viable set of inputs to cause a test failure. A straightforward test case is a valuable debugging tool.
- Generation of test data is **automatic and diverse**. You only need to specify what data types the inputs can be, and optional information for restricting the generated inputs. If the framework to do this already exists, what is the need for reinventing the wheel?

There is, however, a slight learning curve with jqwik's data generators. It is not complicated, but it is a different paradigm than most people are used to. 

Imagine you are trying to process data from a file. In a "normal" scenario, you might be given a flatfile with names on each line. You would simply loop through each line of the file (i.e. file\[i\]). Basically, you are given a "bag" of data, and you can directly operate on each of the items in the bag. For purposes of illustration, this will be called "individual access."

With jqwik's data generators, you have this same bag of data, except you cannot directly operate on each of the items in the bag. You must do operations on the whole bag. This is similar to the idea of dataflow programming or functional programming. For purposes of illustration, this will be called "group access."

The arrow notation is a way of saying, whatever is in the bag will be given a temporary name so we can refer to it. Once it has a name, we can use it to be specific about our filtering. Let's say we have a bag of integers from 1 to 9. With individual access, each of these integers have "names". 1 is bag\[0\], 2 is bag\[1\], etc. The integer 1 has a unique name within the bag. With group access, anything pulled out of the bag is one kind of thing, but has no name, it is simply "a number". This will make more sense after seeing some examples.

I use the term "bag", but in jqwik, it will actually be called an "Arbitrary", basically meaning an arbitrary set of things (i.e. a bag of things). All these generators are tagged with `@Provide` at the top of the function. The function name is how you refer to a specific generator when you want to test a Property.

There are several important operations to know:

### Map ###
  `bag.map(aThing -> func)`

This takes a function `func` and applies it to every item in `bag`. The difference between this and a normal scenario is that you never access the items directly (i.e. for i = 0; i < length; i++, bag\[i\]).

__Example__: Generate a 5 digit number that is a string.
```java
@Provide 
Arbitrary<String> fiveDigitStrings() {
  return Arbitraries.integers(10000, 99999).map(aNumber -> String.valueOf(aNumber));
}
```


### Filter ###
  `bag.filter(aThing -> bool)`

This takes a boolean filter, and applies the filter to `bag`. `bag` will end up containing only the items that cause `bool` to be true. For example, to filter the bag of all integers to *contain* only even numbers (or *filter out* all odd numbers, however you want to think about it).

__Example__: Keep only even numbers
```java
@Provide 
Arbitrary<Integer> oddNumbers() {
  return Arbitraries.integers().filter(aNumber -> aNumber % 2 != 0);
}
```


### Combine ###
  `Combinators.combine(anArbitrary [, anotherArbitrary+ ] ).as((aThing, [, anotherThing+ ]) -> func);`

In the case of object oriented programming, you might have several attributes connected to an object. How can you generate test data for these? It is **very important** that you use generators for all parts of your data if you want the benefits of shrinking. By combining bags of data, you can end up with a resultant bag of desired test data. Imagine these bags are infinite and if you want to keep being able to draw data, you need to use infinite bags everywhere!

__Example__: Create a Person object, with a `name` of certain length, and `age` of certain size. This can create Person objects with varying properties, *AND* the Person data can be shrunk.
```java
@Provide
Arbitrary<Person> validPeople() {
    Arbitrary<String> names = Arbitraries.strings().withCharRange('a', 'z')
        .ofMinLength(3).ofMaxLength(21);
    Arbitrary<Integer> ages = Arbitraries.integers().between(0, 130);
    return Combinators.combine(names, ages)
        .as((name, age) -> new Person(name, age));
}
```


### Flat Mapping ###

This is a technique in which the use case is not immediately clear for. Sometimes, you want to use a drawn value from a generator (Arbitrary) to create another generator / Arbitrary. An example of this is Just know when you want a feature like this, then you __*should*__ use flat mapping.

__Example__: The generator below creates a list of any size, as long as the length of the strings inside are the same length as every other string in the list.

```java
@Provide
Arbitrary<List<String>> listsOfEqualSizedStrings() {
    Arbitrary<Integer> integers2to5 = Arbitraries.integers().between(2, 5);
    return integers2to5.flatMap(stringSize -> {
        Arbitrary<String> strings = Arbitraries.strings()
                .withCharRange('a', 'z')
                .ofMinLength(stringSize).ofMaxLength(stringSize);
        return strings.list();
    });
}
```

This is output from the above flatMap function. 
```
[nyz, xqd, ixp, jcv, gnj, vcu, xcs, ens, aaa, vsa, vkd, meu, fec, hxt, uhn, aaa, rtf, ugo, kes, mqb, pih, ksk]
[yo]
[dxpgi, tzjcv, gnjwk, uqmhx, whens, aaaaa, vsahd, diglm, gnfec, hxtog, nghoa, fhlju, trkes, mqbwq, habck, zcqzr, uparq, pmwzu, olvrm, pijfx, ctvvv, klaku, vtkio, fnwnk, phxiy, vbotl, vjhxm, gguzl, qlqbm, qbthc]
[]
[th, qv, xf, cq, oo, pv, sz, qj, hp, bm, pt, xf, cl, dj, sy, wy]
[thk, vtm, dvc, ioo, pvd, zrj, qwh, pbm, ptz, fjn, cod, psy, wym, rvv, pku, msl]
[zh, qv, xf, cq, oo, pv, sz, qj, hp, bm, pt, xf, cl, dj, sy, wy]
[rzi, rsy, dqb, zzz, iuo, ciz, pxb, avu, mhs, ljf, zzz, aqy, syp, ihe, rjy, nhp, oag, hko, nif, ynl, pdy, dma, lnb, zjj, wif, znt, vkj, uad, foq, zkc]
[bhr, fpd, fdz, odc, aaa, zsp, kya, wdm, mll, oio, ybv, pgr, elj, ybs, pyv, gvl, olp, fml, lrp, yus, aky, bhk, jaw, aaa, zzz, znt, vkj]
[yqfpd, fdzfi, cwciz, pxbgk, utwdm, mlljf, zzzzz, aqybv, pgrsi, jvrjy, nhpyv, gvlth, pynif, ynlrp, yustd, yslnb, zjjaw, aaaaa]
```

If you are thinking that this could be easily implemented another way, you think just like me! **BIG DISCLAIMER**, the creator of jqwik highly recommends **against** doing it like below. I also highly recommend against it! So, if you begin to create code like below, you should use flatMap instead. 

```java
@Provide
Arbitrary<List<String>> badListsOfEqualSizedStrings() {

    // randomly generate a list of ints that the string length could be, between 2 and 5 (inclusive).
    // it does NOT necessarily include all possible values in a given run
    List<Integer> values = Arbitraries.integers().between(2, 5).list().sample();

    // remove duplicates in values list
    List<Integer> uniqueValues = new ArrayList<>(new HashSet<>(values));
    System.out.println(uniqueValues.toString());

    // generate the various string Arbitraries
    ArrayList<Arbitrary<List<String>>> stringArbs = new ArrayList<>();
    for (int i = 0; i < uniqueValues.size(); i++) {
        stringArbs.add(
          Arbitraries.strings().withCharRange('a', 'z').ofMinLength(uniqueValues.get(i)).ofMaxLength(uniqueValues.get(i)).list()
        );
    }

    // pick from one of the Arbitraries, which each generate strings of different lengths
    return Arbitraries.oneOf((Collection) stringArbs);
}
```

The above function is rather complicated because it needs to be able to generate the same kind of data that flatMap can. By using `sample()` (which gets a single value from an Arbitrary), it can't generate the range of 2 to 5 length. `sample()` is only called once and thus all strings will be a single length.

### Selecting with a Probability ###

If you want to do probability, jqwik has ways to do it! 

Simply use `frequency` and provide the options with a number that is the numerator, and the sum is the denominator. Below, the probabilities are 4/7, 2/7 and 1/7 respectively.
```java
Arbitrary<Action.TYPE> actionType = Arbitraries.frequency(
    Tuple.of(4, Action.TYPE.INSERT),
    Tuple.of(2, Action.TYPE.SELECT),
    Tuple.of(1, Action.TYPE.RETURN)
);
```

__*Disclaimer: Bad Code*__ A not-very-good way of doing probability would be to filter based on a random number. The below code will select an INSERT action, a SELECT action, or a RETURN action 25% of the time. This is bad because jqwik has to calculate and then discard results 75% of the time if it is RETURN, whereas using `frequency` will encode the probability into the generation.
```java
import java.util.Random;
Random random = new Random();
Arbitrary<Action.TYPE> actionType = Arbitraries.of(Action.TYPE.values()).filter(aType -> {
    return (aType == Action.TYPE.INSERT || aType == Action.TYPE.SELECT || (random.nextInt(4) == 0 && aType == Action.TYPE.RETURN));
});
```

### Recursive Structures ###

Sometimes you need to generate JSON or other recursive structures. JSON is recursive because it can contain lists of lists, or dictionaries of dictionaries, lists of dictionaries, etc.

With jqwik, I haven't been able to come up with a way to generate JSON easily. Their "recursive" method is sort of what you expect from a recursive function that you code, it does one thing until it encounters a base case and stops (glorified loop).

*However*, with Hypothesis, generating JSON is much easier, and is done in a way akin to Context Free Grammars.

```python
from hypothesis import given
from hypothesis import strategies as st
from string import printable
from pprint import pprint
json = st.recursive(
        st.none() | st.booleans() | st.floats() | st.text(printable),
        lambda children: st.lists(children) | st.dictionaries(st.text(printable), children)
)
pprint(json.example())
```

The output looks like this:
```
{'de(l': None,
 'nK': {'(Rt)': None,
        '+hoZh1YU]gy8': True,
        '8z]EIFA06^li^': 'LFE{Q',
        '9,': 'l{cA=/'}}
```

You can also limit the number of elements (text, integers, lists, etc.) by using `max_leaves`.

```python
json = st.recursive(
        st.none() | st.booleans() | st.floats() | st.text(printable),
        lambda children: st.lists(children) | st.dictionaries(st.text(printable), children), max_leaves=8
)
```

```
{'"x9eS+D-+si\'': {}}
```

My general recommendation is to use Java and jqwik with IntelliJ at the beginning, and to avoid Hypothesis (Python). In most cases, Java is superior because variables are statically-typed. The jqwik library shows you what types each function returns. This is helpful tool to get an understanding of the various functionalities of Property-based Testing implemented by jqwik.

