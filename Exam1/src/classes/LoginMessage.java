package classes;


public class LoginMessage extends Message{
	private String username;
	private String password;
	
	public LoginMessage(String msgType, String sender, String username, String password) {
		super(msgType, sender);
		this.username = username;
		this.password = password;
	}
	
	
	public String getUsername() {
		return username;
	}

	public String getPassword() {
		return password;
	}


	@Override
	public String toString() {
		return this.username + this.password;
	}

}

