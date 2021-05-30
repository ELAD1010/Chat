package classes;

public class Message {
	protected String msgType;
	protected String sender;
	
	public Message(String msgType, String sender){
		this.msgType = msgType;
		this.sender = sender;
	}
	
	public String getMsgType() {
		return this.msgType;
	}
	
	public String getSender() {
		return this.sender;
	}
	

}
