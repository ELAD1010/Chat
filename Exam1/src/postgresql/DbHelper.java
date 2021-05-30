package postgresql;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

import classes.LoginMessage;


public class DbHelper {
	
	public static void insert(LoginMessage user) throws SQLException {
		final String sqlQuery = "INSERT INTO \"Users\" (username,password,is_online) VALUES (?,?, true)";
		Connection conn = Database.getInstance().getConnection();
		 try {
			 PreparedStatement pstmt = conn.prepareStatement(sqlQuery, Statement.RETURN_GENERATED_KEYS);
			 pstmt.setString(1, user.getUsername());
	         pstmt.setString(2, user.getPassword());
	         int affectedRows = pstmt.executeUpdate();
	     }
		 finally {
			 System.out.println("Insert Successful");
		 }
	}
	
	public static String userExists(LoginMessage user) throws SQLException {
		Connection conn = Database.getInstance().getConnection();
		PreparedStatement statement1= conn.prepareStatement("SELECT * from public.\"Users\" where username = ?");
		statement1.setString(1, user.getUsername());
		ResultSet rs1 = statement1.executeQuery();
		if(!rs1.next()) {
			insert(user);
			return "Not Exists";
		}
		else {
			return "Exist";
		}
		
		
		
	}
	
	public static String checkLoginInfo(LoginMessage user) throws SQLException {
		Connection conn = Database.getInstance().getConnection();
		PreparedStatement statement2 = conn.prepareStatement("SELECT * from public.\"Users\" where username = ? and password = ?");
		statement2.setString(1, user.getUsername());
		statement2.setString(2, user.getPassword());
		ResultSet rs2 = statement2.executeQuery();
		if(rs2.next()) {
			return "Correct";
		}
		else {
			return "Incorrect";
		}
		
	}
	
	public static void updateActivity(String username, String activity) throws SQLException {
		Connection conn = Database.getInstance().getConnection();
		boolean isOnline;
		if(activity.equals("Online")) {
			isOnline = true;
		}
		else {
			isOnline = false;
		}
		PreparedStatement statement1= conn.prepareStatement("Update public.\"Users\" set is_online = ? where username = ?");
		statement1.setBoolean(1, isOnline);
		statement1.setString(2, username);
		statement1.execute();
	}
	
	public static ArrayList<String> fetchOnlineUsers(String username) throws SQLException{
		Connection conn = Database.getInstance().getConnection();
		ArrayList<String> usersList = new ArrayList<String>();
		PreparedStatement statement1= conn.prepareStatement("SELECT username FROM public.\"Users\" where is_online = ? and username != ?");
		statement1.setBoolean(1, true);
		statement1.setString(2, username);
		ResultSet rs1 = statement1.executeQuery();
		while(rs1.next()) {
			usersList.add(rs1.getString("username"));
		}
		return usersList;
	}

}
