package server;
import java.net.Socket;

public class UserSocket {
	private String username;
	private ClientHandler handler;
	
	public UserSocket(String uname, ClientHandler handler) {
		this.username = uname;
		this.handler = handler;
	}

	public String getUsername() {
		return username;
	}

	public ClientHandler getHandler() {
		return handler;
	}
	
	

}
