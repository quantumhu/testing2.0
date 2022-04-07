package Tests;

import org.junit.runner.RunWith;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;

@RunWith(Cucumber.class)
@CucumberOptions(
    features="src/test/java/Features",
    plugin = { "pretty" })
public class BDTTestRunner {
}