package tests;

import net.jqwik.api.*;
import org.assertj.core.api.*;

import java.util.*;

public class DandCTest {

    @Property
    void testing(@ForAll("strGenerator") String testStr) {
        System.out.println(testStr);
        // run the test code here
        DivideAndConquer.find_single(testStr, 0, testStr.length() - 1);
    }

    @Provide
    Arbitrary<String> strGenerator() {
        return Arbitraries.randomValue(random -> generateValidString(random));
    }

    private String generateValidString(Random random) {
        String testStr = "";

        ArrayList<String> characters = new ArrayList<>(Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"));
        Collections.shuffle(characters);

        // define the length of the string, it could include no characters or all characters
        int strLen = random.nextInt(26);

        // one of the letters will be singular, randomly select it
        char singular = (char) (random.nextInt(26) + 'a');

        for (int i = 0; i <= strLen; i++) {
            char c = characters.get(i).charAt(0);
            if (c != singular) {
                testStr = testStr + c + c;
            } else {
                testStr = testStr + c;
            }
        }

        return testStr;
    }

    @Property
    void evenLengthStringsShouldAlwaysReturnNull(@ForAll("strGenerator") String testStr) {

        if (testStr.length() % 2 == 0) {
            Integer value = DivideAndConquer.error_find_single(testStr, 0, testStr.length() - 1);
            Assertions.assertThat(value).isEqualTo(null);
        }
    }

    @Property
    void OddLengthStringsShouldAlwaysReturnInteger(@ForAll("strGenerator") String testStr) {

        if (testStr.length() % 2 == 1) {
            Integer value = DivideAndConquer.error_find_single(testStr, 0, testStr.length() - 1);
            Assertions.assertThat(value).isGreaterThanOrEqualTo(0).isLessThanOrEqualTo(testStr.length() - 1);
        }
    }

    @Property
    void OneIndexAfterSingleLetterIntegerShouldBeADifferentStringOrEndOfString(@ForAll("strGenerator") String testStr) {

        if (testStr.length() % 2 == 1) {
            Integer index = DivideAndConquer.error_find_single(testStr, 0, testStr.length() - 1);

            if (index == 0) { // beginning of string
                Assertions.assertThat(index - 1).isEqualTo(-1);
            } else if (index == testStr.length() - 1) { // end of string
                Assertions.assertThat(index + 1).isEqualTo(testStr.length());
            } else {
                System.out.println("index: " + testStr.charAt(index) + "; index+1: " + testStr.charAt(index + 1));
                Assertions.assertThat(testStr.charAt(index)).isNotEqualTo(testStr.charAt(index + 1));
            }
        }
    }
}


