# IntelliJ Setup
This document is an supporting document to [Java Testing 2.0 Setup](https://github.com/quantumhu/testing2.0/blob/main/java_setup.md#java-testing-20-setup) and details how to setup Cucumber and jqwik on **IntelliJ**.
The steps are similar to [Java Testing 2.0 Setup](https://github.com/quantumhu/testing2.0/blob/main/java_setup.md#java-testing-20-setup) setup for Eclipse.
*This document is designed for macOS but should work on any OS.*
## jqwik + Cucumber pre-setup
1. Open IntelliJ
2. Click on **Projects** on the menu on the left. Click **New Project > Maven**. Unchecked check-box  *Create from archetype* if it is checked.
3. Clcik **Next**.
4. In *GroupID* and enter a name that has format `<something>.<something>`. In *ArtifactID*, type any name.
5. Chick **Finish**.
6. In the *Project Menu*, find `pom.xml` under the project you made. Double click to open.
7. Insert the following lines between `<properties>` and `</properties>`:
```
<project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
<jqwik.version>1.6.3</jqwik.version>
<assertj.version>3.22.0</assertj.version>
<cucumber.version>7.0.0</cucumber.version>
```
8. Paste the following after `</properties>`:
```
<dependencies>
    <dependency>
        <groupId>net.jqwik</groupId>
        <artifactId>jqwik</artifactId>
        <version>${jqwik.version}</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.8.2</version>
    </dependency>
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>${assertj.version}</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-java</artifactId>
        <version>${cucumber.version}</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.cucumber</groupId>
        <artifactId>cucumber-junit</artifactId>
        <version>${cucumber.version}</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

   ***if you want to add dependencies step by step, see appendix down below in the same section.***

9. Paste the following in after the last `</dependencies>`:
```
<build>
    <plugins>
        <plugin>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.8.1</version>
            <configuration>
                <compilerArgs>
                    <arg>-parameters</arg>
                </compilerArgs>
            </configuration>
        </plugin>
        <plugin>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
            <configuration>
                <includes>
                    <include>**/*Tests.java</include>
                    <include>**/*Examples.java</include>
                    <include>**/*Properties.java</include>
                </includes>
                <properties>
                    <configurationParameters>
                        cucumber.junit-platform.naming-strategy=long
                    </configurationParameters>
                </properties>
            </configuration>
        </plugin>
    </plugins>
</build>
```

10. To apply new changes in the build script, click on icon **Load Maven Changes** in the top-right corner of the editor.

### Appendix
In **pom.xml**, press `⌘ N`, select **Dependency**. In the pop-up window, use the *Search For Artifact* to search and add the following dependencies. 
- jqwik
- junit-jupiter (with version 5.8.2)
- assertj-core
- cucumber-java (replace version code line with `<version>${cucumber.version}</version>`)
- cucumber-junit (replace version code line with `<version>${cucumber.version}</version>`)

## Running Code with  Cucumber-Java
1. In the project file directory, right click on `src/test` to create a new directory called `resources`. Now you will have a new created directory `src/test/resources`.
2. Right click on the `resources` folder and click **Mark directory as > Test Resources Root**.
3. In the project file directory, right click on `src/test/java` and click **New>Package**. Name the new package the name you want.
4. Right click on the new package, select **New > Java Class** to create a class called `TestRunner`, and paste in the following code:
```
import org.junit.runner.RunWith;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
		features="src/test/java/resources")
public class TestRunner {
}
```
5. Right click on the `src/test/java/resources` folder and click **New > File**. Name this file however you want but end it in `.feature` *(extension)*. A pop-up window might show up to ask if the extension is wanted. Press **OK**.
6. Double click the new .feature file you created to open the `.feature` file. Paste the following code in:
```
Feature: Is it Friday yet?
  Everybody wants to know when it's Friday

  Scenario: Sunday isn't Friday
    Given today is Sunday
    When I ask whether it's Friday yet
    Then I should be told "Nope"
```
7.  Right click the  `src/test/java/<your new created package name>`  folder and create a new class called  `MondayTester`. The actual name doesn't matter much in the long run. Paste the following in:
```
import static org.junit.Assert.*;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

class IsItFriday {
    static String isItFriday(String today) {
        return "Nope";
    }
}

public class MondayTester {
    private String today;
    private String actualAnswer;

    @Given("today is Sunday")
    public void today_is_Sunday() {
        today = "Sunday";
    }

    @When("I ask whether it's Friday yet")
    public void i_ask_whether_it_s_Friday_yet() {
        actualAnswer = IsItFriday.isItFriday(today);
    }

    @Then("I should be told {string}")
    public void i_should_be_told(String expectedAnswer) {
        assertEquals(expectedAnswer, actualAnswer);
    }
}
```
8. Run the Cucumber test code by running the `TestRunner` class. A console should appear at the bottom with all tests passed *(three green checking marks)*.

## Running code with jqwik
1. Right click the  `src/test/java/<your new created package name>`  folder and create a new Java class. Name it however you want but **the name must end with "Test"**.
2. Add imports at the top of the java class file:
```
import net.jqwik.api.*;
import org.assertj.core.api.*;
```
3. Paste the following code in the class:
```
@Property
boolean absoluteValueOfAllNumbersIsPositive(@ForAll int anInteger) {
    return Math.abs(anInteger) >= 0;
}

@Property
void lengthOfConcatenatedStringIsGreaterThanLengthOfEach(
    @ForAll String string1, @ForAll String string2
) {
    String conc = string1 + string2;
    Assertions.assertThat(conc.length()).isGreaterThan(string1.length());
    Assertions.assertThat(conc.length()).isGreaterThan(string2.length());
}
```
4. Run the test by clicking on the green play button showing on the left side of the function header, e.g. *absoluteValueOfAllNumbersIsPositive*.
5. You should expect to see errors for both property tests.
```
timestamp = 2022-02-06T21:15:45.034, CaseTest:absoluteValueOfAllNumbersIsPositive =
  org.opentest4j.AssertionFailedError:
    Property [CaseTest:absoluteValueOfAllNumbersIsPositive] failed with sample {0=-2147483648}
```
```
timestamp = 2022-02-06T21:16:29.984, CaseTest:lengthOfConcatenatedStringIsGreaterThanLengthOfEach =
  java.lang.AssertionError:
    Expecting actual:
      1
    to be greater than:
      1
```
