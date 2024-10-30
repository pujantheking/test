const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const db = new sqlite3.Database(path.join(__dirname, 'ecommerce.db'), (err) => {
  if (err) {
      console.error('Database connection error:', err);
  } else {
      console.log('Connected to database');
  }
});
// Create table if it doesn't exist
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    email TEXT,
    address TEXT,
    city TEXT,
    zipCode TEXT,
    phone TEXT,
    consumerId TEXT,
    txnId TEXT,
    amount REAL,
    productName TEXT,
    status TEXT
  )
`);


const express = require('express');
const cors = require('cors');  
const crypto = require('crypto');
const bodyParser = require('body-parser');

const app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Use CORS middleware
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));


app.get('/test', (req, res) => {
  res.json({
      status: 'ok',
      message: 'API is working',
      timestamp: new Date().toISOString(),
      path: req.path,
      method: req.method,
      headers: req.headers
  });
});


const MERCHANT_ID = "L1043733"; // Your Merchant ID
const SALT = "5981514647TMLRTF"; // Replace with actual salt from Worldline

// Token generation route
app.post('/api/generate-token/zeny-enterprice', (req, res) => {
    const {
        amount, 
        consumerId, 
        txnId, 
        accountNo = "", 
        consumerMobileNo = "", 
        consumerEmailId = "", 
        debitStartDate = "", 
        debitEndDate = "", 
        maxAmount = "", 
        amountType = "", 
        frequency = "", 
        cardNumber = "", 
        expMonth = "", 
        expYear = "", 
        cvvCode = ""
    } = req.body;

    // Check for required parameters
    if (!amount || !consumerId || !txnId) {
        return res.status(400).json({ error: 'Missing required parameters' });
    }

    // Create the string to hash using pipe-separated format
    const stringToHash = `${MERCHANT_ID}|${txnId}|${amount}|${accountNo}|${consumerId}|${consumerMobileNo}|${consumerEmailId}|${debitStartDate}|${debitEndDate}|${maxAmount}|${amountType}|${frequency}|${cardNumber}|${expMonth}|${expYear}|${cvvCode}|${SALT}`;

    console.log("String to Hash (utf-8):", Buffer.from(stringToHash, 'utf-8').toString()); // Log the string for verification

    // Generate the hash using SHA-256
    const hash = crypto.createHash('sha256').update(stringToHash, 'utf-8').digest('hex');


    // Return the generated token (hash) to the client
    res.json({ token: hash });
});

app.post('/api/store-order-details/zeny-enterprice', (req, res) => {
    const { firstName, lastName, email, address, city, zipCode, phone, productName, amount, orderId, consumerId, txnId } = req.body;
  
    const sql = `INSERT INTO users (firstName, lastName, email, address, city, zipCode, phone, productName, amount, status, consumerId, txnId) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?, ?)`;
  
    db.run(sql, [firstName, lastName, email, address, city, zipCode, phone, productName, amount, consumerId, txnId], function (err) {
      if (err) {
        console.error("Error inserting order data:", err.message);
        return res.status(500).json({ success: false, error: 'Order storage failed' });
      }
      res.json({ success: true, message: 'Order details stored successfully' });
    });
  });
  

app.post('/api/payment-response/zeny-enterprice', (req, res) => {
    const { msg } = req.body;

    // Split the `msg` string by '|' to get each piece of data
    const [
        statusCode, 
        statusMessage, 
        random,
        txnId, 
        merchantId, 
        random2, 
        consumerId, 
        amount, 
        txnDate, 
        ...otherDetails
    ] = msg.split('|');


    if (statusCode === "0300") {
        console.log("Payment Successful!");

        // Store or update user data based on consumerId and txnId
        const userData = {
            consumerId,
            amount,
            txnId,
            status: "Success",
            date: txnDate
        };
        console.log("userdata :",userData)


        db.run(
            `UPDATE users SET status = ? WHERE txnId = ?`, 
            [userData.status, userData.txnId], 
            function(err) {
                if (err) {
                    console.error("Database update error:", err.message);
                    return res.status(500).json({ success: false, error: "Database update failed" });
                }
                res.redirect("https://zenyenterprise.com/front-end/order-confirmation.html");
            }
        );
    } else {
        console.log("Payment failed with status code:", statusCode);
        res.json({ success: false, message: "Payment failed." });
    }
});
// Add the route to fetch all users
app.get('/api/users/zeny-enterprice', (req, res) => {
    const query = `
      SELECT *
      FROM users;
    `;
  
    db.all(query, (error, results) => {
      if (error) {
        console.error('Error fetching users:', error);
        res.status(500).send('An error occurred while fetching users');
        return;
      }
      res.json({ success: true, users: results });
    });
  });
  


// Starting the
app.listen(8080, '0.0.0.0', () => {  // Changed to localhost
  console.log('Server running on port 3000');
});

