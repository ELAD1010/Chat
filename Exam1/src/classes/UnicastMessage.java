package classes;

public class UnicastMessage extends Message{
	private String receiver;
	private String data;
	
	public UnicastMessage(String msgType, String sender, String receiver, String data) {
		super(msgType, sender);
		this.receiver = receiver;
		this.data = data;
	}
	
    public String get_receiver() {
        return this.receiver;
    }

    public String get_data() {
        return this.data;
    }


}
