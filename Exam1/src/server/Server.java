package server;
import java.io.*;
import java.net.*;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;

import com.google.gson.Gson;

import postgresql.Database;
import postgresql.DbHelper;
import classes.*; 

public class Server implements Runnable{
	
	private ServerSocket serverSocket;
	public ArrayList<UserSocket> clientList;
	private Thread mainThread;
	public Database db;
	public Server(int port) throws SQLException {
		try {
			this.serverSocket = new ServerSocket(port);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.clientList = new ArrayList<UserSocket>();
		System.out.println("Server is listening on port " + port);
		this.mainThread = new Thread(this);
		this.mainThread.start();
	}
	public void run() {
		while(this.mainThread != null) {
			try {
				Socket clientSock = this.serverSocket.accept();
				synchronized(clientList) {
				ClientHandler clientHandler = new ClientHandler(this, clientSock);
				Thread.sleep(1000);
				if(clientHandler.getUsername() != null) {
					this.clientList.add(new UserSocket(clientHandler.getUsername(), clientHandler));
					DbHelper.updateActivity(clientHandler.getUsername(), "Online");
					this.sendOnlineUsers();
					}
				}
			}
			catch(InterruptedException e) {
			}
			catch(IOException e) {
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	public void sendBroadcast(BroadcastMessage msg) {
		Gson gson = new Gson();
		synchronized(clientList) {
			for(int i=0; i<this.clientList.size(); i++)
			{
				UserSocket socket = this.clientList.get(i);
				if(!(socket.getUsername().equals(msg.getSender()))) {
					System.out.println(socket.getUsername() + " " + msg.getSender());
					ClientHandler clientHandler = socket.getHandler();
					String broadcastJson = gson.toJson(msg);
					clientHandler.out.println(broadcastJson);
				}
			
			}
		}
	}
	
	public void sendUnicast(UnicastMessage msg) {
		boolean isFound = false;
		Gson gson = new Gson();
		synchronized(clientList) {
			for(int i = 0; i<this.clientList.size() && !isFound; i++) {
				UserSocket socket = this.clientList.get(i);
				if(socket.getUsername().equals(msg.get_receiver())) {
					ClientHandler clientHandler = socket.getHandler();
					String unicastJson = gson.toJson(msg);
					clientHandler.out.println(unicastJson);
					isFound = true;
				}
			}
		}
	}
	
	public void removeClient(String username) {
		boolean isFound = false;
		synchronized(clientList) {
			for(int i=0; i<this.clientList.size() && !isFound; i++) {
				UserSocket socket = this.clientList.get(i);
				if(socket.getUsername() == username) {
					this.clientList.remove(i);
					isFound = true;
				}
			}
		}
	}
	
	public void sendOnlineUsers() throws SQLException {
		Gson gson = new Gson();
		for(int i=0; i<this.clientList.size(); i++)
		{
			UserSocket socket = this.clientList.get(i);
			System.out.println(socket.getUsername());
			ArrayList<String> users = DbHelper.fetchOnlineUsers(socket.getUsername());
			HashMap<String, Object> usersList = new HashMap<String, Object>();
			usersList.put("msgType", "Users");
			usersList.put("data", users);
			String jsonUsersList = gson.toJson(usersList);
			socket.getHandler().out.println(jsonUsersList);
		}
		
	}
	 
	
}
