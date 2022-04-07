package Main;

public class Action {
    private TYPE type;
    private int value;

    public enum TYPE {
        INSERT,
        SELECT,
        RETURN;
    }

    public Action(TYPE type, int value) {
        this.type = type;
        this.value = value;
    }

    public TYPE getType() {
        return this.type;
    }

    public int getValue() {
        return this.value;
    }

    @Override
    public String toString() {
        return this.type.toString() + this.getValue();
    }
}