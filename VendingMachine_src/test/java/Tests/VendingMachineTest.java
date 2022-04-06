package Tests;

import Main.Action;
import Main.VendingMachine;
import net.jqwik.api.*;
import org.assertj.core.api.*;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;

public class VendingMachineTest {

    @Property
    void changeMustBeLessThanMoneyInserted(@ForAll("inputs") Action[] testCase) {

        // calculate the total amount of money that was inserted by checking all actions
        int totalMoneyInserted = 0;
        for (int i = 0; i < testCase.length; i++) {
            if (testCase[i].getType() == Action.TYPE.INSERT) {
                totalMoneyInserted += testCase[i].getValue();
            }
        }

        VendingMachine sut = new VendingMachine();
        int[] result = sut.allSteps(testCase, false);

        Assertions.assertThat(result[1]).isLessThanOrEqualTo(totalMoneyInserted);

    }

    @Property
    void drinksDispensedMustCorrelateToSELECTIONActionsAndCostPerDrink(@ForAll("inputs") Action[] testCase) {

        int totalMoneyInserted = 0;
        int selectionActions = 0;
        int selectionCost = 0;

        for (int i = 0; i < testCase.length; i++) {
            if (testCase[i].getType() == Action.TYPE.INSERT) {
                totalMoneyInserted += testCase[i].getValue();
            } else if (testCase[i].getType() == Action.TYPE.SELECT) {
                selectionCost += testCase[i].getValue();
                selectionActions += 1;
            }
        }

        VendingMachine sut = new VendingMachine();
        int[] result = sut.allSteps(testCase, false);

        // drinks dispensed is <= number of select actions
        Assertions.assertThat(result[0]).isLessThanOrEqualTo(selectionActions);

        // drinks dispensed times the minimum cost of a drink must be <= the total amount of money inserted
        Assertions.assertThat(result[0] * 200).isLessThanOrEqualTo(totalMoneyInserted);

        // selectionCost must

    }

    @Property
    void balanceIsNeverNegative(@ForAll("inputs") Action[] testCase) {
        VendingMachine sut = new VendingMachine();
        sut.allSteps(testCase, false);
        Assertions.assertThat(sut.getBalance()).isNotNegative();
    }

    @Property
    void printTester(@ForAll("inputs") Action[] testCase) {
        // print out the list of Actions in a pretty form
        System.out.print("[");
        for (int i = 0; i < testCase.length; i++) {
            System.out.print(testCase[i].toString());
            System.out.print(", ");
        }
        System.out.println("]");
    }

    @Provide
    Arbitrary<Action[]> inputs() {
        Arbitrary<Integer> coinValues = Arbitraries.of(5, 10, 25, 100, 200);
        Arbitrary<Integer> selectValues = Arbitraries.integers().greaterOrEqual(20).lessOrEqual(25);
        Arbitrary<Action.TYPE> actionType = Arbitraries.frequency(
                Tuple.of(4, Action.TYPE.INSERT),
                Tuple.of(2, Action.TYPE.SELECT),
                Tuple.of(1, Action.TYPE.RETURN)
        );

        Arbitrary<Action> action = Combinators.combine(coinValues, selectValues, actionType).as((oneCoinValue, oneSelectValue, oneType) -> {
            // based on the action, give it a certain value
            // the coinValues and selectValues are different
            if (oneType == Action.TYPE.INSERT) {
                return new Action(Action.TYPE.INSERT, oneCoinValue);

            } else if (oneType == Action.TYPE.SELECT) {
                return new Action(Action.TYPE.SELECT, oneSelectValue * 10); // 20 to 25 is mapped to 200 to 250

            } else {
                return new Action(Action.TYPE.RETURN, 0);
            }
        });

        // creates an array of size 0 to 100
        return action.array(Action[].class).ofMinSize(0).ofMaxSize(100);
    }

    @Property
    boolean fixedSizedStrings(@ForAll("listsOfEqualSizedStrings")List<String> strings) {
        System.out.println(strings.toString());
        Assume.that(!strings.isEmpty());
        return strings.stream().map(String::length).distinct().count() == 1;
    }

    @Property
    boolean fixedSizedStringpp(@ForAll("badListsOfEqualSizedStrings")List<String> strings) {
        System.out.println(strings.toString());
        Assume.that(!strings.isEmpty());
        return strings.stream().map(String::length).distinct().count() == 1;
    }

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

    @Provide
    Arbitrary<List<String>> badListsOfEqualSizedStrings() {

        // randomly generate a list of ints that the string length could be, between 2 and 5 (inclusive). it does NOT necessarily include all possible values in a given run
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

}
