# jqwik Setup

This document details how to setup jqwik on Eclipse.

This document is designed for macOS but should work on any OS.

## macOS specific JDK setup

These instructions outline how to add JDK 8u321 to your Eclipse installation and make it the default JDK. Follow similar instructions if you are using Windows.

1. Install JDK 8u321 from the [GitHub page](./java)
2. Open Eclipse, go to **Preferences**, go to **Java > Installed JREs**.
3. Click **Add**. Click **Next**.
4. Click on **Directory** (top right button).
5. Press *Cmd+Shift+G* to get a popup, and navigate to `/Library/Java/JavaVirtualMachines/`.
6. Go inside the folder called `jdk1.8.0_321.jdk`. Go inside `Contents`. Click on `Home`.
7. Click on **Open** at the bottom of the dialog. The popup that appeared will disappear.
8. In the current menu, change the JRE name to "JDK 1.8.0 321". Then click **Finish**.
9. Make sure the one you just added is check-marked so it is the default JDK.
10. Click **Apply and Close**.
11. Close Eclipse.

## jqwik

1.  Open Eclipse.
2.  Using the menu, create a new Maven project. Navigate to **New > Other > Maven Project**.
3.  Select the **Create a simple project** checkbox.
4.  Click **Next**.
5.  In *Group ID*, type pretty much anything. It doesn’t really matter what you type as long as it’s `<something>.<something>`. This follows reverse domain name notation.
6.  In *Artifact ID*, type a name that you’d like the Java project to be called, *e.g.* pbtfun.
7.  Click **Finish**.
8.  In the *Package Explorer*, find `pom.xml` under the project you made. Double click to open.
9.  Paste the following in before the last line:
```
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.source>1.8</maven.compiler.source>
    <maven.compiler.target>${maven.compiler.source}</maven.compiler.target>
    <jqwik.version>1.6.3</jqwik.version>
    <assertj.version>3.22.0</assertj.version>
</properties>

<dependencies>
    <dependency>
        <groupId>net.jqwik</groupId>
        <artifactId>jqwik</artifactId>
        <version>${jqwik.version}</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>${assertj.version}</version>
        <scope>test</scope>
    </dependency>
</dependencies>

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
            </configuration>
        </plugin>
    </plugins>
</build>
```
  

10.  Right click on the project, click **Maven > Update Project**. Click **OK**.
11.  Right click on the project, click **New**, click **JUnit Test Case**.
12.  At the top select **New Junit Jupiter Test**. Put in a name under “Name”. **Please note, the name you choose must end in "Test"**.
13.  There’s going to be a popup about JUnit 5, click OK. At this point, the environment is completely setup.

#### Running code with jqwik

14.  Add these imports at the top of the .java file you created:
```
import net.jqwik.api.*;
import org.assertj.core.api.*;
```
15.  Replace the code in the class definition with this:
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
16.  Finally, to run a test, click on the function header, e.g. *absoluteValueOfAllNumbersIsPositive*, and then press **Run** (the green play button that you normally press to run things in Eclipse).
17. You should expect to see errors for both property tests.

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