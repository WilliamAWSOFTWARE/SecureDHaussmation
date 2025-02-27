const mysql = require('mysql2/promise'); 

const connection = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'Seguridad2025',
  database: 'gestion_urbanizacion',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = connection;

