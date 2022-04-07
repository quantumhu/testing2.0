package Main;

public class VendingMachine {

    private enum State {
        IDLE,
        COININSERT
    }

    private State currentState = null;
    private int balance = 0;

    public VendingMachine() {
        this.currentState = State.IDLE;
    }

    public int getBalance() {
        return this.balance;
    }

    public int[] oneStep(Action currentAction, boolean showInput) {

        int drinks = 0;
        int change = 0;

        switch (this.currentState) {
            case IDLE:
                if (currentAction.getType() == Action.TYPE.INSERT) {
                    this.balance += currentAction.getValue();
                    this.currentState = State.COININSERT;
                    if (showInput)
                        System.out.println("Inserted a " + Integer.toString(currentAction.getValue()) + " coin");
                }
                break;
            case COININSERT:
                if (currentAction.getType() == Action.TYPE.INSERT) {
                    this.balance += currentAction.getValue();
                    if (showInput)
                        System.out.println("Inserted a " + Integer.toString(currentAction.getValue()) + " coin");
                }

                if (currentAction.getType() == Action.TYPE.SELECT) {

                    int cost = currentAction.getValue();

                    // introduce bug here
                    if (this.balance >= 200) {

                        this.balance -= cost;
                        if (showInput) System.out.println("Made a selection");

                        drinks++;
                        if (showInput) System.out.println("Dispensed a drink @ " + cost + "!");

                    } else {
                        if (showInput)
                            System.out.println("Not enough balance to purchase: have " + this.balance + ", need " + cost);
                    }

                }

                if (currentAction.getType() == Action.TYPE.RETURN) {
                    if (this.balance > 0) {
                        change += this.balance;
                        this.balance = 0;
                        if (showInput) System.out.println("Return change");
                    } else {
                        if (showInput) System.out.println("No change to return");
                    }
                    this.currentState = State.IDLE;
                }
        }

        return new int[]{drinks, change};

    }

    public int[] allSteps(Action[] actions, boolean showInput) {

        int current = 0;
        int end = actions.length - 1;
        Action currentAction = null;

        int drinks = 0;
        int change = 0;

        try {
            // given a list of actions, execute all the actions in order FIFO
            while (current <= end) {

                currentAction = actions[current];
                int[] result = this.oneStep(currentAction, showInput);
                drinks += result[0];
                change += result[1];

                current++;

            }
        } catch (Exception e) {
            System.out.println(e);
        }

        return new int[]{drinks, change};
    }

}
