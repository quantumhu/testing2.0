package Tests;

import Main.Action;
import Main.VendingMachine;
import io.cucumber.java.bs.A;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.assertj.core.api.Assertions;

public class VendingMachineBDTTest {
    VendingMachine sut = new VendingMachine();
    int cost = 0;
    int drinks = 0;
    int change = 0;

    // Scenario: Buying a toonie drink
    @Given("the cost of a drink is ${int}")
    public void the_cost_of_a_drink_is_$(Integer int1) {
        cost = int1;
    }

    @Given("I inserted a toonie")
    public void i_inserted_a_toonie() {
        sut.oneStep(new Action(Action.TYPE.INSERT, 200), false);
    }

    @When("I select a ${int} drink")
    public void i_select_a_$_drink(Integer int1) {
        int[] result = sut.oneStep(new Action(Action.TYPE.SELECT, int1), false);
        drinks = result[0];
        change = result[1];
    }

    @Then("I should have a drink")
    public void i_should_have_a_drink() {
        Assertions.assertThat(drinks).isEqualTo(1);
    }

    @Then("no change to return")
    public void no_change_to_return() {
        Assertions.assertThat(change).isEqualTo(0);
    }

    // Scenario: Change
    @When("I insert a ${int} coin")
    public void i_insert_a_$_coin(Integer int1) {
        sut.oneStep(new Action(Action.TYPE.INSERT, int1), false);
    }

    @When("I press the return change button")
    public void i_press_the_return_change_button() {
        int[] result = sut.oneStep(new Action(Action.TYPE.RETURN, 0), false);
        change = result[1];
    }

    @Then("I should have ${int} in change")
    public void i_should_have_$_in_change(Integer int1) {
        Assertions.assertThat(change).isEqualTo(int1);
    }

}
