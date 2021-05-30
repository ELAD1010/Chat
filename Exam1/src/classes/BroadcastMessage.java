package classes;

public class BroadcastMessage extends Message{
	private String receiver;
	private String data;
	
	public BroadcastMessage(String msgType, String sender, String receiver, String data) {
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

    public String show_msg(String username){
        if (this.sender == username) {
            return "Me: " + this.data;
        }
        else {
            return this.sender + ": " + this.data;
        }
    }

}
