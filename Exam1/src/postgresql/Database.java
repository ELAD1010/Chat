package postgresql;

import classes.LoginMessage;

import java.sql.Array;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

public class Database {
	
	private final String url = "jdbc:postgresql://localhost/postgres";
	private final String username = "postgres";
	private final String password = "Eladt2911";
	private Connection connection;
	private static Database instance;
	
	
	private Database() throws SQLException {
        try {
            Class.forName("org.postgresql.Driver");
            this.connection = DriverManager.getConnection(url, username, password);
        } catch (ClassNotFoundException ex) {
            System.out.println("Database Connection Creation Failed : " + ex.getMessage());
        }
    }
	
	public Connection getConnection() {
        return connection;
    }
	
	/*
	 public Connection connect() throws SQLException {
	        return DriverManager.getConnection(url, username, password);
	    }
	    */
	public static Database getInstance() throws SQLException {
        if (instance == null) {
            instance = new Database();
        } else if (instance.getConnection().isClosed()) {
            instance = new Database();
        }

        return instance;
    }
	
}

