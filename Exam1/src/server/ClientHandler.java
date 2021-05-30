package server;
import java.net.Socket;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.google.gson.Gson;

import java.io.*;

import classes.*;
import postgresql.DbHelper;

public class ClientHandler implements Runnable{
	private Server server;
	private Socket socket;
	private BufferedReader input = null;
	public PrintWriter out = null;
	private String username;
	public ClientHandler(Server server, Socket clientSock){
		this.server = server;
		this.socket = clientSock;
		try 
		{
			//this.input = new DataInputStream(new BufferedInputStream(socket.getInputStream())); 
			this.input = new BufferedReader(new InputStreamReader (socket.getInputStream()));
			this.out = new PrintWriter(this.socket.getOutputStream(),true); 
		}
		catch(IOException i) 
        { 
            System.out.println(i); 
        } 
		Thread readThread = new Thread(this);
		readThread.start();
	}
	public void run() {
		String message;
		while(true) {
			try {
				message = this.input.readLine();
				System.out.println(message);
				Gson gson = new Gson();
				if(message.contains("\"msg_type\": \"Login\"")) {
					
					LoginMessage user = (LoginMessage)gson.fromJson(message, LoginMessage.class);
					if(DbHelper.checkLoginInfo(user) == "Correct") {
						this.out.println("Correct");
						this.username = user.getUsername();
					}
					else {
						this.out.println("Incorrect");
						this.socket.close();
						break;
					}
				}
				
				else if(message.contains("\"msg_type\": \"Register\"")) {
					
					LoginMessage user = (LoginMessage)gson.fromJson(message, LoginMessage.class);
					if(DbHelper.userExists(user) == "Not Exists") {
						this.out.println("Not Exists");
						this.username = user.getUsername();
					}
					else {
						System.out.println("He");
						this.out.println("Exists");
						this.socket.close();
						break;
					}
				}
				else if(message.contains("\"msgType\": \"Broadcast\"")) {
					BroadcastMessage msg = (BroadcastMessage)gson.fromJson(message, BroadcastMessage.class);
					this.server.sendBroadcast(msg);
					
				}
				else if(message.contains("\"msgType\": \"Unicast\"")) {
					UnicastMessage msg = (UnicastMessage)gson.fromJson(message, UnicastMessage.class);
					this.server.sendUnicast(msg);
				}
				else if(message.equals("Online")) {
					this.server.sendOnlineUsers();
				}
				else if(message.equals("Offline")){
					DbHelper.updateActivity(this.username, message);
					this.socket.close();
					this.server.removeClient(this.username);
					this.server.sendOnlineUsers();
					break;
				}
				else if(message.equals("update_photos")) {
					this.server.sendOnlineUsers();
				}
			} 
			catch (IOException e) {
			e.printStackTrace();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		
		}
	}
	public String getUsername() {
		return this.username;
	}
}
